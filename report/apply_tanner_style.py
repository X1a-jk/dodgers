#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Apply Tanner-Scott-style HTML layout to the 5 regenerated scouting reports.
Uses overall_grades.png as hero image, drops report_cover and season_comparison images,
and places charts in their corresponding sections.
"""
import os
from generate_five_reports import build_players


def grade_class(grade):
    if grade.startswith("A"):
        return "grade-a"
    if grade.startswith("B"):
        return "grade-b"
    if grade.startswith("C"):
        return "grade-c"
    return "grade-d"


def make_tanner_html(slug, info, current, hist, custom, is_pitcher=True):
    display = custom.get("display_name", slug.replace("-", " ").title())
    nickname = custom.get("nickname", "")
    title = f"{display} 球探报告"
    position_line = f"Los Angeles Dodgers #{info.get('primary_number','')} | {info.get('position_name','')} | {'活跃' if info.get('active', True) else '伤病名单'}"
    hero_img = f"{slug}_overall_grades.png"

    # basic info grid
    basic_items = [
        ("全名", display),
        ("出生日期", info.get("birth_date", "-")),
        ("年龄", f"{info.get('age','-')}岁"),
        ("出生地", custom.get("birthplace", "-")),
        ("身高/体重", f"{info.get('height','-')} / {info.get('weight','-')} lbs"),
        ("投球/击球" if is_pitcher else "击球/投球", f"{info.get('throws','-')}{'投' if is_pitcher else '打'} / {info.get('bats','-')}{'打' if is_pitcher else '投'}"),
        ("位置", info.get("position_name", "-")),
        ("MLB首秀", info.get("mlb_debut_date", "-")),
        ("背号", f"#{info.get('primary_number','-')}"),
    ]
    if nickname:
        basic_items.append(("绰号", nickname))
    info_grid_html = "\n".join(
        f"""<div class="info-item"><div class="label">{label}</div><div class="value">{value}</div></div>"""
        for label, value in basic_items
    )

    # summary paragraphs (split by blank lines in custom['summary'])
    summary_paras = "\n".join(
        f"<p style='margin-bottom: 15px;'>{p.strip()}</p>"
        for p in custom.get("summary", "").split("\n\n") if p.strip()
    )

    # career highlights
    highlights = custom.get("career_highlights", [])
    if not highlights:
        # fallback: derive from background
        highlights = [
            {"year": "MLB 生涯", "title": "职业生涯概述", "text": custom.get("background", "")[:200] + "..."}
        ]
    highlights_html = "\n".join(
        f"""<div class="career-highlight"><h4>🌟 {h['year']} - {h['title']}</h4><p>{h['text']}</p></div>"""
        for h in highlights
    )

    # 2026 stat cards
    if is_pitcher:
        stat_cards = [
            ("出赛", current.get("games_played", "-")),
            ("先发", current.get("games_started", "-")),
            ("胜", current.get("wins", "-")),
            ("败", current.get("losses", "-")),
            ("ERA", current.get("era", "-")),
            ("IP", current.get("innings_pitched", "-")),
            ("K", current.get("strikeouts", "-")),
            ("BB", current.get("walks", "-")),
            ("WHIP", current.get("whip", "-")),
            ("K/9", current.get("strikeouts_per_9", "-")),
            ("BB/9", current.get("walks_per_9", "-")),
            ("SV", current.get("saves", "-")),
        ]
    else:
        stat_cards = [
            ("出赛", current.get("games_played", "-")),
            ("打数", current.get("at_bats", "-")),
            ("得分", current.get("runs", "-")),
            ("安打", current.get("hits", "-")),
            ("本垒打", current.get("home_runs", "-")),
            ("打点", current.get("rbi", "-")),
            ("盗垒", current.get("stolen_bases", "-")),
            ("保送", current.get("walks", "-")),
            ("三振", current.get("strikeouts", "-")),
            ("AVG", current.get("avg", "-")),
            ("OBP", current.get("obp", "-")),
            ("OPS", current.get("ops", "-")),
        ]
    stats_grid_html = "\n".join(
        f"""<div class="stat-card"><span class="stat-value" style="color: #4fc3f7;">{val}</span><div class="stat-label">{label}</div></div>"""
        for label, val in stat_cards
    )

    # season comparison table (use existing rows from custom build)
    # We'll rebuild table from current + hist
    if is_pitcher:
        comp_header_cells = ["赛季", "球队", "G", "GS", "W", "L", "ERA", "IP", "K", "BB", "WHIP", "SV"]
        comp_rows = []
        for r in hist[-5:]:
            st = r["stats"]
            comp_rows.append(
                f"<td>{r['season']}</td><td>{r['team']}</td><td>{st.get('gamesPlayed','-')}</td><td>{st.get('gamesStarted','-')}</td>"
                f"<td>{st.get('wins','-')}</td><td>{st.get('losses','-')}</td><td>{st.get('era','-')}</td><td>{st.get('inningsPitched','-')}</td>"
                f"<td>{st.get('strikeOuts','-')}</td><td>{st.get('baseOnBalls','-')}</td><td>{st.get('whip','-')}</td><td>{st.get('saves','-')}</td>"
            )
        comp_rows.append(
            f"<td class='warning'>2026</td><td>Los Angeles Dodgers</td><td>{current.get('games_played','-')}</td><td>{current.get('games_started','-')}</td>"
            f"<td>{current.get('wins','-')}</td><td>{current.get('losses','-')}</td><td>{current.get('era','-')}</td><td>{current.get('innings_pitched','-')}</td>"
            f"<td>{current.get('strikeouts','-')}</td><td>{current.get('walks','-')}</td><td>{current.get('whip','-')}</td><td>{current.get('saves','-')}</td>"
        )
    else:
        comp_header_cells = ["赛季", "球队", "G", "AB", "AVG", "OBP", "SLG", "OPS", "HR", "RBI", "SB"]
        comp_rows = []
        for r in hist[-5:]:
            st = r["stats"]
            comp_rows.append(
                f"<td>{r['season']}</td><td>{r['team']}</td><td>{st.get('gamesPlayed','-')}</td><td>{st.get('atBats','-')}</td>"
                f"<td>{st.get('avg','-')}</td><td>{st.get('obp','-')}</td><td>{st.get('slg','-')}</td><td>{st.get('ops','-')}</td>"
                f"<td>{st.get('homeRuns','-')}</td><td>{st.get('rbi','-')}</td><td>{st.get('stolenBases','-')}</td>"
            )
        comp_rows.append(
            f"<td class='warning'>2026</td><td>Los Angeles Dodgers</td><td>{current.get('games_played','-')}</td><td>{current.get('at_bats','-')}</td>"
            f"<td>{current.get('avg','-')}</td><td>{current.get('obp','-')}</td><td>{current.get('slg','-')}</td><td>{current.get('ops','-')}</td>"
            f"<td>{current.get('home_runs','-')}</td><td>{current.get('rbi','-')}</td><td>{current.get('stolen_bases','-')}</td>"
        )
    comp_header_html = "".join(f"<th>{c}</th>" for c in comp_header_cells)
    comp_rows_html = "\n".join(f"<tr>{row}</tr>" for row in comp_rows)

    # pitch arsenal or hitting tools
    if is_pitcher:
        has_velo = custom.get("has_velo_chart", False)
        velo_img_html = ""
        if has_velo:
            velo_img_html = f"""<div style="text-align: center; margin: 20px 0;"><img src="{slug}_pitch_velocities.png" alt="投球武器库速度" style="width: 100%; max-width: 900px; border-radius: 10px;"><p style="text-align: center; color: #90a4ae; font-size: 0.95em; margin-top: 10px;">⚾ 各球种球速区间（蓝=最低球速，橙=最高球速，红线=平均值）。球速差与位移差越大，打者越难锁定单一球路。</p></div>"""
        pitch_cards = "\n".join(
            f"""<div class="pitch-card"><h3>{a['name']} ({a['en']})</h3><p><span class="velocity">{a['velo']}</span></p><p>{a['desc']}</p></div>"""
            for a in custom.get("arsenal", [])
        )
        weapons_html = f"""<div class="section"><h2>🎯 投球武器库</h2>{velo_img_html}<div class="pitch-arsenal">{pitch_cards}</div></div>"""
    else:
        tool_cards = "\n".join(
            f"""<div class="pitch-card"><h3>{t['name']}</h3><p><span class="velocity">评分：{t['grade']}</span></p><p>{t['desc']}</p></div>"""
            for t in custom.get("tools", [])
        )
        weapons_html = f"""<div class="section"><h2>🎯 打击能力分析</h2><div class="pitch-arsenal">{tool_cards}</div></div>"""

    # scouting analysis paragraphs / headings
    def fmt_analysis(text):
        out = []
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("### "):
                out.append(f"<h3 style='color: #4fc3f7; margin: 20px 0 15px 0;'>{s[4:]}</h3>")
            elif s:
                out.append(f"<p>{s}</p>")
        return "\n".join(out)
    analysis_paras = fmt_analysis(custom.get("analysis", ""))

    # defense section for hitters
    defense_html = ""
    if not is_pitcher and custom.get("defense"):
        defense_paras = fmt_analysis(custom.get("defense", ""))
        defense_html = f"""<div class="section"><h2>🛡️ 守备与多功能性</h2>{defense_paras}</div>"""

    # pros / cons
    pros_html = "\n".join(f"<li>{p}</li>" for p in custom.get("pros", []))
    cons_html = "\n".join(f"<li>{c}</li>" for c in custom.get("cons", []))

    # grades
    grades = custom.get("grades", [])
    grade_cards = "\n".join(
        f"""<div class="stat-card"><span class="stat-value" style="color: #4fc3f7;">{g['score']}</span><div class="stat-label">{g['tool']}</div><span class="grade {grade_class(g['grade'])}">{g['grade']}</span></div>"""
        for g in grades
    )
    overall = custom.get("overall", {})

    # future / background
    future_paras = fmt_analysis(custom.get("future", ""))
    background_paras = fmt_analysis(custom.get("background", ""))

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color: #e0e0e0; line-height: 1.6; min-height: 100vh;
}}
.container {{ max-width: 1000px; margin: 0 auto; padding: 20px; }}
.header {{
  text-align: center; padding: 40px 0;
  background: linear-gradient(90deg, #005A9C 0%, #1a5490 50%, #005A9C 100%);
  border-radius: 15px; margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}}
.header h1 {{ font-size: 3em; color: #fff; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); margin-bottom: 10px; }}
.header .subtitle {{ font-size: 1.2em; color: #e0e0e0; font-style: italic; }}
.player-card {{
  background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 30px; margin-bottom: 30px;
  backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex; gap: 30px; flex-wrap: wrap;
}}
.player-info {{ flex: 1; min-width: 250px; }}
.player-info h2 {{ color: #4fc3f7; margin-bottom: 15px; font-size: 1.8em; }}
.info-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }}
.info-item {{ background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 8px; }}
.info-item .label {{ font-size: 0.9em; color: #90a4ae; text-transform: uppercase; letter-spacing: 1px; }}
.info-item .value {{ font-size: 1.2em; color: #fff; font-weight: bold; }}
.section {{
  background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 30px;
  margin-bottom: 30px; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1);
}}
.section h2 {{
  color: #4fc3f7; margin-bottom: 20px; font-size: 1.8em;
  border-bottom: 2px solid #4fc3f7; padding-bottom: 10px;
}}
.stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin-top: 20px; }}
.stat-card {{
  background: linear-gradient(135deg, rgba(0, 90, 156, 0.3) 0%, rgba(26, 84, 144, 0.3) 100%);
  border-radius: 10px; padding: 20px; text-align: center;
  border: 1px solid rgba(79, 195, 247, 0.3); transition: transform 0.3s ease;
}}
.stat-card:hover {{ transform: translateY(-5px); }}
.stat-card .stat-value {{ font-size: 2.5em; font-weight: bold; color: #4fc3f7; display: block; }}
.stat-card .stat-label {{ font-size: 0.9em; color: #90a4ae; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px; display: block; }}
.comparison-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
.comparison-table th, .comparison-table td {{ padding: 12px; text-align: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }}
.comparison-table th {{ background: rgba(0, 90, 156, 0.3); color: #4fc3f7; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }}
.comparison-table tr:hover {{ background: rgba(255, 255, 255, 0.05); }}
.pitch-arsenal {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }}
.pitch-card {{
  background: linear-gradient(135deg, rgba(0, 90, 156, 0.2) 0%, rgba(26, 84, 144, 0.2) 100%);
  border-radius: 10px; padding: 20px; border-left: 4px solid #4fc3f7;
}}
.pitch-card h3 {{ color: #4fc3f7; margin-bottom: 10px; }}
.pitch-card .velocity {{ font-size: 1.5em; color: #fff; font-weight: bold; }}
.pros-cons {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }}
.pros, .cons {{ background: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 20px; }}
.pros h3 {{ color: #4caf50; margin-bottom: 15px; }}
.cons h3 {{ color: #f44336; margin-bottom: 15px; }}
.pros ul, .cons ul {{ list-style: none; }}
.pros li, .cons li {{ padding: 8px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }}
.pros li::before {{ content: "✓ "; color: #4caf50; font-weight: bold; }}
.cons li::before {{ content: "✗ "; color: #f44336; font-weight: bold; }}
.grade {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 0.9em; margin-top: 8px; }}
.grade-a {{ background: rgba(76, 175, 80, 0.3); color: #4caf50; }}
.grade-b {{ background: rgba(79, 195, 247, 0.3); color: #4fc3f7; }}
.grade-c {{ background: rgba(255, 152, 0, 0.3); color: #ff9800; }}
.grade-d {{ background: rgba(244, 67, 54, 0.3); color: #f44336; }}
.highlight {{ color: #4fc3f7; font-weight: bold; }}
.warning {{ color: #ff9800; font-weight: bold; }}
.success {{ color: #4caf50; font-weight: bold; }}
.danger {{ color: #f44336; font-weight: bold; }}
.career-highlight {{ background: rgba(255, 215, 0, 0.1); border: 1px solid rgba(255, 215, 0, 0.3); border-radius: 10px; padding: 15px; margin: 15px 0; }}
.career-highlight h4 {{ color: #FFD700; margin-bottom: 10px; }}
.footer {{ text-align: center; padding: 20px; color: #90a4ae; font-size: 0.9em; }}
img {{ max-width: 100%; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
</style>
</head>
<body>
<div class="container">

<div class="header">
  <h1>⚾ {display}</h1>
  <p class="subtitle">{position_line}</p>
</div>

<div class="section" style="text-align: center; padding: 0; background: none; border: none; backdrop-filter: none; box-shadow: none;">
  <img src="{slug}_report_cover.png" alt="报告封面" style="width: 100%; max-width: 750px;">
</div>

<div class="player-card">
  <div class="player-info">
    <h2>基本信息</h2>
    <div class="info-grid">
      {info_grid_html}
    </div>
  </div>
  <div class="player-info">
    <h2>球探总评</h2>
    {summary_paras}
  </div>
</div>

<div class="section">
  <h2>🏆 职业生涯亮点</h2>
  {highlights_html}
</div>

<div class="section">
  <h2>📊 2026赛季{'投球' if is_pitcher else '打击'}数据</h2>
  <div class="stats-grid">
    {stats_grid_html}
  </div>
</div>

<div class="section">
  <h2>📊 赛季对比</h2>
  <h3 style="margin-top: 20px; color: #4fc3f7;">{'投球数据对比' if is_pitcher else '打击数据对比'}</h3>
  <table class="comparison-table">
    <thead><tr>{comp_header_html}</tr></thead>
    <tbody>{comp_rows_html}</tbody>
  </table>
</div>

{weapons_html}

{defense_html}

<div class="section">
  <h2>🔍 球探分析</h2>
  {analysis_paras}
</div>

<div class="section">
  <h2>✅ 优势 vs ❌ 劣势</h2>
  <div class="pros-cons">
    <div class="pros">
      <h3>优势 (Strengths)</h3>
      <ul>{pros_html}</ul>
    </div>
    <div class="cons">
      <h3>劣势 (Weaknesses)</h3>
      <ul>{cons_html}</ul>
    </div>
  </div>
</div>

<div class="section">
  <h2>📊 综合评分</h2>
  <div style="text-align: center; margin: 20px 0;">
    <img src="{slug}_overall_grades.png" alt="综合评分雷达图" style="max-width: 600px;">
  </div>
  <div class="stats-grid">
    {grade_cards}
  </div>
  <div style="margin-top: 30px; text-align: center;">
    <h3 style="color: #4fc3f7; margin-bottom: 15px;">总体潜力评分</h3>
    <div style="font-size: 4em; color: #4caf50; font-weight: bold;">{overall.get('score','-')}</div>
    <p style="color: #90a4ae; margin-top: 10px;">{overall.get('label','')}</p>
    <p style="margin-top: 15px;"><span class="grade {grade_class(overall.get('grade',''))}" style="font-size: 1.2em;">{overall.get('grade','-')} 级</span></p>
  </div>
</div>

<div class="section">
  <h2>🔮 未来展望</h2>
  {future_paras}
</div>

<div class="section">
  <h2>📖 背景故事</h2>
  {background_paras}
</div>

<div class="footer">
  <p>数据来源：MLB.com | Baseball Savant | MLB Stats API</p>
  <p>报告生成时间：2026-08-20 | 数据截止日期：2026-08-20</p>
  <p>⚾ 洛杉矶道奇队球探报告</p>
</div>

</div>
</body>
</html>"""
    return html


def main():
    players = build_players()
    for slug, info, current, hist, custom, is_pitcher in players:
        dir_path = f"D:/baseball/report/{slug}"
        html = make_tanner_html(slug, info, current, hist, custom, is_pitcher)
        html_path = os.path.join(dir_path, f"{slug}-scouting-report.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Tanner-style HTML: {html_path} ({len(html)} chars)")

if __name__ == "__main__":
    main()
