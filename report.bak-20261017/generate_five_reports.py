#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate full scouting reports for 5 Dodgers players.
Charts already exist; this script only regenerates MD and HTML content.
"""
import json, os, re
from datetime import datetime

REPORT_DATE = "2026-08-20"
DATA_DATE = "2026-08-20"

with open("D:/baseball/report/historical_stats.json", "r", encoding="utf-8") as f:
    HIST = json.load(f)


def parse_hist(pid, group):
    api_group = "pitching" if group == "pitching" else "hitting"
    rows = []
    for season in [2021, 2022, 2023, 2024, 2025]:
        key = f"{pid}_{season}"
        if key not in HIST:
            continue
        data = HIST[key].get("data", {})
        people = data.get("people", [])
        if not people:
            continue
        stats = people[0].get("stats", [])
        for s in stats:
            if s.get("group", {}).get("displayName") != api_group:
                continue
            for sp in s.get("splits", []):
                st = sp.get("stat", {})
                team = sp.get("team", {}).get("name", "-")
                if st.get("gamesPlayed", 0) in (0, None, "-"):
                    continue
                rows.append({"season": str(season), "team": team, "stats": st})
    return rows


def make_pitcher_md(name, info, current, hist_rows, custom):
    slug = custom["slug"]
    display = custom.get("display_name", name)
    nickname = custom.get("nickname", "")

    comp_header = "| 赛季 | 球队 | 出赛 | 先发 | 胜 | 败 | ERA | IP | 三振 | 保送 | WHIP | 救援 |\n|------|------|------|------|-----|-----|------|------|------|------|------|------|"
    comp_rows = []
    for r in hist_rows[-5:]:
        st = r["stats"]
        comp_rows.append(
            f"| {r['season']} | {r['team']} | {st.get('gamesPlayed','-')} | {st.get('gamesStarted','-')} | "
            f"{st.get('wins','-')} | {st.get('losses','-')} | {st.get('era','-')} | {st.get('inningsPitched','-')} | "
            f"{st.get('strikeOuts','-')} | {st.get('baseOnBalls','-')} | {st.get('whip','-')} | {st.get('saves','-')} |"
        )
    c = current
    comp_rows.append(
        f"| 2026 | Los Angeles Dodgers | {c.get('games_played','-')} | {c.get('games_started','-')} | "
        f"{c.get('wins','-')} | {c.get('losses','-')} | {c.get('era','-')} | {c.get('innings_pitched','-')} | "
        f"{c.get('strikeouts','-')} | {c.get('walks','-')} | {c.get('whip','-')} | {c.get('saves','-')} |"
    )
    season_comp_table = comp_header + "\n" + "\n".join(comp_rows)

    career = custom.get("career", {})
    arsenal_md = "\n\n".join([
        f"### {a['name']} ({a['en']})\n- **球速**：{a['velo']}\n- **使用占比**：{a.get('usage','约30-40%')}\n- **评分**：**{a['grade']}**\n- {a['desc']}"
        for a in custom.get("arsenal", [])
    ])
    pros_md = "\n".join([f"- ✅ {p}" for p in custom.get("pros", [])])
    cons_md = "\n".join([f"- ❌ {c}" for c in custom.get("cons", [])])
    grades_header = "| 项目 | 评分 (20-80) | 等级 |\n|------|-------------|------|"
    grades_rows = "\n".join([f"| {g['tool']} | {g['score']} | {g['grade']} |" for g in custom.get("grades", [])])
    overall = custom.get("overall", {})

    md = f"""# {display} 球探报告

> **Los Angeles Dodgers #{info.get('primary_number','')} | {info.get('position_name','P')} | {info.get('throws','R')}投/{info.get('bats','R')}打{f' | {nickname}' if nickname else ''}**
> 
> 报告生成时间：{REPORT_DATE} | 数据截止日期：{DATA_DATE}

---

## 📋 基本信息

| 项目 | 内容 |
|------|------|
| **全名** | {display} |
| **出生日期** | {info.get('birth_date','-')} |
| **年龄** | {info.get('age','-')}岁 |
| **出生地** | {custom.get('birthplace','-')} |
| **身高/体重** | {info.get('height','-')} / {info.get('weight','-')} lbs |
| **投球/击球** | {info.get('throws','-')}投 / {info.get('bats','-')}打 |
| **MLB首秀** | {info.get('mlb_debut_date','-')} |
| **背号** | #{info.get('primary_number','-')} |
{f"| **绰号** | {nickname} |" if nickname else ""}

### 球探总评

{custom.get('summary','')}

---

## 📊 2026赛季统计数据

| 统计项目 | 数值 |
|----------|------|
| **出赛 (G)** | {current.get('games_played','-')} |
| **先发 (GS)** | {current.get('games_started','-')} |
| **胜场 (W)** | {current.get('wins','-')} |
| **败场 (L)** | {current.get('losses','-')} |
| **自责分率 (ERA)** | {current.get('era','-')} |
| **投球局数 (IP)** | {current.get('innings_pitched','-')} |
| **被安打 (H)** | {current.get('hits','-')} |
| **自责分 (ER)** | {current.get('earned_runs','-')} |
| **全垒打 (HR)** | {current.get('home_runs','-')} |
| **三振 (SO)** | {current.get('strikeouts','-')} |
| **保送 (BB)** | {current.get('walks','-')} |
| **WHIP** | {current.get('whip','-')} |
| **K/9** | {current.get('strikeouts_per_9','-')} |
| **BB/9** | {current.get('walks_per_9','-')} |
| **救援成功 (SV)** | {current.get('saves','-')} |

> ⚠️ **注意**：{custom.get('current_note','')}

---

## 📊 赛季对比

{season_comp_table}

---

## 🏆 职业生涯数据

| 统计项目 | 数值 |
|----------|------|
| **MLB年资** | {career.get('years','-')} |
| **总出赛** | {career.get('games','-')} |
| **生涯ERA** | {career.get('era','-')} |
| **生涯IP** | {career.get('ip','-')} |
| **生涯三振** | {career.get('strikeouts','-')} |
| **生涯WHIP** | {career.get('whip','-')} |
| **生涯救援成功** | {career.get('saves','-')} |
{f"| **主要荣誉** | {career.get('awards','-')} |" if career.get('awards') else ""}

---

## 🎯 投球武器库

{arsenal_md}

---

## 🔍 球探分析

{custom.get('analysis','')}

---

## ✅ 优势 vs ❌ 劣势

### 优势
{pros_md}

### 劣势
{cons_md}

---

## 📊 综合评分

{grades_header}
{grades_rows}

### 总体评分：{overall.get('score','-')} ({overall.get('grade','-')} 级 / {overall.get('label','-')})

---

## 🔮 未来展望

{custom.get('future','')}

---

## 📖 背景故事与历史成就

{custom.get('background','')}

---

## 📈 图表附录

- 报告封面：![{display} 报告封面](./{slug}_report_cover.png)
- 赛季对比：![{display} 赛季对比](./{slug}_season_comparison.png)
- 综合评分雷达图：![{display} 综合评分](./{slug}_overall_grades.png)
{f"- 球速分布：![{display} 球速分布](./{slug}_pitch_velocities.png)" if custom.get('has_velo_chart') else ""}

---

*数据来源：MLB.com | Baseball Savant | MLB Stats API*
*报告生成：{REPORT_DATE}*
"""
    return md


def make_hitter_md(name, info, current, hist_rows, custom):
    slug = custom["slug"]
    display = custom.get("display_name", name)
    nickname = custom.get("nickname", "")

    comp_header = "| 赛季 | 球队 | G | AB | AVG | OBP | SLG | OPS | HR | RBI | SB |\n|------|------|-----|-----|------|------|------|------|-----|-----|-----|"
    comp_rows = []
    for r in hist_rows[-5:]:
        st = r["stats"]
        comp_rows.append(
            f"| {r['season']} | {r['team']} | {st.get('gamesPlayed','-')} | {st.get('atBats','-')} | "
            f"{st.get('avg','-')} | {st.get('obp','-')} | {st.get('slg','-')} | {st.get('ops','-')} | "
            f"{st.get('homeRuns','-')} | {st.get('rbi','-')} | {st.get('stolenBases','-')} |"
        )
    c = current
    comp_rows.append(
        f"| 2026 | Los Angeles Dodgers | {c.get('games_played','-')} | {c.get('at_bats','-')} | "
        f"{c.get('avg','-')} | {c.get('obp','-')} | {c.get('slg','-')} | {c.get('ops','-')} | "
        f"{c.get('home_runs','-')} | {c.get('rbi','-')} | {c.get('stolen_bases','-')} |"
    )
    season_comp_table = comp_header + "\n" + "\n".join(comp_rows)

    career = custom.get("career", {})
    tools_md = "\n\n".join([
        f"### {t['name']}\n- **评分**：**{t['grade']}**\n- {t['desc']}"
        for t in custom.get("tools", [])
    ])
    pros_md = "\n".join([f"- ✅ {p}" for p in custom.get("pros", [])])
    cons_md = "\n".join([f"- ❌ {c}" for c in custom.get("cons", [])])
    grades_header = "| 项目 | 评分 (20-80) | 等级 |\n|------|-------------|------|"
    grades_rows = "\n".join([f"| {g['tool']} | {g['score']} | {g['grade']} |" for g in custom.get("grades", [])])
    overall = custom.get("overall", {})

    md = f"""# {display} 球探报告

> **Los Angeles Dodgers #{info.get('primary_number','')} | {info.get('position_name','')} | {info.get('bats','R')}打/{info.get('throws','R')}投{f' | {nickname}' if nickname else ''}**
> 
> 报告生成时间：{REPORT_DATE} | 数据截止日期：{DATA_DATE}

---

## 📋 基本信息

| 项目 | 内容 |
|------|------|
| **全名** | {display} |
| **出生日期** | {info.get('birth_date','-')} |
| **年龄** | {info.get('age','-')}岁 |
| **出生地** | {custom.get('birthplace','-')} |
| **身高/体重** | {info.get('height','-')} / {info.get('weight','-')} lbs |
| **击球/投球** | {info.get('bats','-')}打 / {info.get('throws','-')}投 |
| **MLB首秀** | {info.get('mlb_debut_date','-')} |
| **背号** | #{info.get('primary_number','-')} |
{f"| **绰号** | {nickname} |" if nickname else ""}

### 球探总评

{custom.get('summary','')}

---

## 📊 2026赛季统计数据

| 统计项目 | 数值 |
|----------|------|
| **出赛 (G)** | {current.get('games_played','-')} |
| **打数 (AB)** | {current.get('at_bats','-')} |
| **打席 (PA)** | {current.get('plate_appearances','-')} |
| **得分 (R)** | {current.get('runs','-')} |
| **安打 (H)** | {current.get('hits','-')} |
| **二垒安 (2B)** | {current.get('doubles','-')} |
| **三垒安 (3B)** | {current.get('triples','-')} |
| **本垒打 (HR)** | {current.get('home_runs','-')} |
| **打点 (RBI)** | {current.get('rbi','-')} |
| **盗垒 (SB)** | {current.get('stolen_bases','-')} |
| **保送 (BB)** | {current.get('walks','-')} |
| **三振 (SO)** | {current.get('strikeouts','-')} |
| **打击率 (AVG)** | {current.get('avg','-')} |
| **上垒率 (OBP)** | {current.get('obp','-')} |
| **长打率 (SLG)** | {current.get('slg','-')} |
| **OPS** | {current.get('ops','-')} |

> ⚠️ **注意**：{custom.get('current_note','')}

---

## 📊 赛季对比

{season_comp_table}

---

## 🏆 职业生涯数据

| 统计项目 | 数值 |
|----------|------|
| **MLB年资** | {career.get('years','-')} |
| **总出赛** | {career.get('games','-')} |
| **生涯AVG** | {career.get('avg','-')} |
| **生涯OBP** | {career.get('obp','-')} |
| **生涯SLG** | {career.get('slg','-')} |
| **生涯OPS** | {career.get('ops','-')} |
| **生涯HR** | {career.get('hr','-')} |
| **生涯RBI** | {career.get('rbi','-')} |
| **生涯SB** | {career.get('sb','-')} |
{f"| **主要荣誉** | {career.get('awards','-')} |" if career.get('awards') else ""}

---

## 🎯 打击能力分析

{tools_md}

---

## 🛡️ 守备与多功能性

{custom.get('defense','')}

---

## 🔍 球探分析

{custom.get('analysis','')}

---

## ✅ 优势 vs ❌ 劣势

### 优势
{pros_md}

### 劣势
{cons_md}

---

## 📊 综合评分

{grades_header}
{grades_rows}

### 总体评分：{overall.get('score','-')} ({overall.get('grade','-')} 级 / {overall.get('label','-')})

---

## 🔮 未来展望

{custom.get('future','')}

---

## 📖 背景故事与历史成就

{custom.get('background','')}

---

## 📈 图表附录

- 报告封面：![{display} 报告封面](./{slug}_report_cover.png)
- 赛季对比：![{display} 赛季对比](./{slug}_season_comparison.png)
- 综合评分雷达图：![{display} 综合评分](./{slug}_overall_grades.png)

---

*数据来源：MLB.com | Baseball Savant | MLB Stats API*
*报告生成：{REPORT_DATE}*
"""
    return md


def convert_md_to_html(title, md, slug, is_pitcher=True):
    lines = md.splitlines()
    body = []
    table_rows = []
    list_items = []
    bq_lines = []
    section_open = False

    def md_inline(s):
        s = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\*(.*?)\*", r"<em>\1</em>", s)
        return s

    def close_section():
        nonlocal section_open
        if section_open:
            body.append("</div>")
            section_open = False

    def flush_table():
        if not table_rows:
            return
        header = table_rows[0]
        body_rows = [row for row in table_rows[1:] if not all(set(c.strip()) <= set("- |") and c.strip() for c in row)]
        head_html = "<thead><tr>" + "".join(f"<th>{md_inline(c)}</th>" for c in header) + "</tr></thead>"
        tbody = "<tbody>"
        for row in body_rows:
            tbody += "<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in row) + "</tr>"
        tbody += "</tbody>"
        body.append(f'<table class="comparison-table">{head_html}{tbody}</table>')
        table_rows.clear()

    def flush_list():
        if list_items:
            body.append("<ul>" + "".join(f"<li>{md_inline(it)}</li>" for it in list_items) + "</ul>")
            list_items.clear()

    def flush_bq():
        if bq_lines:
            txt = " ".join(bq_lines).lstrip("⚠️ 注意：")
            body.append(f'<div class="note">{md_inline(txt)}</div>')
            bq_lines.clear()

    for line in lines:
        stripped = line.strip()

        if stripped.startswith(">"):
            flush_table(); flush_list(); close_section()
            bq_lines.append(stripped[1:].strip())
            continue
        else:
            if bq_lines:
                flush_bq()

        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if len(cells) >= 2 and all(set(c.strip()) <= set("- |") and c.strip() for c in cells):
                continue
            table_rows.append(cells)
            continue
        else:
            if table_rows:
                flush_table()

        if stripped.startswith("# "):
            flush_list(); close_section()
            body.append(f"<h1>{md_inline(stripped[2:])}</h1>")
            continue
        if stripped.startswith("## "):
            flush_list(); close_section()
            body.append(f'<div class="section"><h2>{md_inline(stripped[3:])}</h2>')
            section_open = True
            continue
        if stripped.startswith("### "):
            flush_list()
            body.append(f"<h3>{md_inline(stripped[4:])}</h3>")
            continue

        if stripped == "---":
            flush_list(); close_section()
            body.append("<hr>")
            continue

        if stripped.startswith("- "):
            text = stripped[2:]
            m = re.match(r"(.+?)：\s*!\[(.*?)\]\((.*?)\)", text)
            if m:
                label = m.group(2)
                src = m.group(3)
                body.append(f'<figure><img src="{src}" alt="{label}"><figcaption>{md_inline(label)}</figcaption></figure>')
                continue
            list_items.append(text)
            continue
        else:
            if list_items:
                flush_list()

        if stripped:
            body.append(f"<p>{md_inline(line)}</p>")
        else:
            if list_items:
                flush_list()

    flush_table(); flush_list(); flush_bq(); close_section()

    content = "\n".join(body)
    return f"""<!DOCTYPE html>
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
.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
.header {{
  text-align: center; padding: 40px 0;
  background: linear-gradient(90deg, #005A9C 0%, #1a5490 50%, #005A9C 100%);
  border-radius: 15px; margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}}
.header h1 {{ font-size: 2.5em; color: #fff; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); margin-bottom: 10px; }}
.header .subtitle {{ font-size: 1.2em; color: #e0e0e0; font-style: italic; }}
.section {{
  background: rgba(255,255,255,0.05); border-radius: 15px; padding: 30px;
  margin-bottom: 30px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1);
}}
h2 {{ color: #4fc3f7; margin-bottom: 20px; font-size: 1.8em; border-bottom: 2px solid #4fc3f7; padding-bottom: 10px; }}
h3 {{ color: #81d4fa; margin: 20px 0 10px; font-size: 1.3em; }}
.comparison-table {{
  width: 100%; border-collapse: collapse; margin-top: 20px;
}}
.comparison-table th, .comparison-table td {{
  padding: 12px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1);
}}
.comparison-table th {{
  background: rgba(0,90,156,0.3); color: #4fc3f7; font-weight: bold;
}}
.comparison-table tr:hover {{ background: rgba(255,255,255,0.05); }}
.note {{
  background: rgba(255,193,7,0.1); border-left: 4px solid #ffc107;
  padding: 15px; border-radius: 8px; margin: 20px 0; color: #ffe082;
}}
ul {{ margin: 15px 0 15px 25px; }}
li {{ margin: 8px 0; }}
figure {{ margin: 20px 0; text-align: center; }}
figure img {{ max-width: 100%; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); }}
figcaption {{ color: #90a4ae; margin-top: 8px; font-size: 0.9em; }}
p {{ margin: 12px 0; }}
strong {{ color: #fff; }}
hr {{ border: 0; height: 1px; background: rgba(255,255,255,0.1); margin: 20px 0; }}
</style>
</head>
<body>
<div class="container">
<div class="header">
  <h1>{title}</h1>
  <p class="subtitle">Los Angeles Dodgers 球探报告</p>
</div>
{content}
</div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Player-specific content
# ---------------------------------------------------------------------------

def build_players():
    players = []

    # Edwin Diaz
    edwin_current = {
        "games_played": 16, "games_started": 0, "wins": 2, "losses": 2,
        "era": "11.85", "innings_pitched": "13.2", "hits": 25,
        "runs": 18, "earned_runs": 18, "home_runs": 3, "strikeouts": 19,
        "walks": 10, "saves": 7, "holds": 0, "whip": "2.56",
        "strikeouts_per_9": "12.51", "walks_per_9": "6.59"
    }
    edwin_info = {
        "full_name": "Edwin Diaz", "primary_number": "3", "position_name": "后援投手（终结者）",
        "throws": "右", "bats": "右", "birth_date": "1994-03-22", "age": 32,
        "height": "6' 3\"", "weight": 165, "mlb_debut_date": "2016-06-06"
    }
    edwin_custom = {
        "slug": "edwin-diaz",
        "display_name": "Edwin Diaz",
        "nickname": "Sugar",
        "birthplace": "Naguabo, Puerto Rico（波多黎各纳瓜沃）",
        "current_note": "2026赛季数据为截至8月20日的小样本。Diaz 赛季初长期养伤，7月才从伤病名单回归，目前仍在找回节奏。ERA 11.85 与 WHIP 2.56 均严重偏离其生涯水准，需结合过往精英级救援表现综合评估。",
        "summary": "Edwin Diaz 是当今 MLB 最具压制力的终结者之一，职业生涯多次入选全明星，并在 2022 年打出历史级救援赛季（1.31 ERA、118 次三振、32 次救援成功、0.84 WHIP），成为当年最 dominant 的后援投手。他以 elite 级别的四缝线速球和锐利滑球组合闻名，三振能力长期维持在大联盟顶尖水准。2025 年在纽约大都会保持健康，交出 62 场出赛、1.63 ERA、0.87 WHIP、98 次三振的顶级成绩，证明他仍是联盟最可靠的终结者之一。然而 2026 年赛季初因伤病影响长期缺阵，回归后小样本表现挣扎，16 场出赛 ERA 高达 11.85、WHIP 2.56，控球与速球品质均明显下滑。考虑到他的武器库完整度和过往履历，目前的问题更像是伤病恢复期与节奏找回问题，而非能力永久性衰退。若能在赛季末找回 2025 年的状态，他仍将是道奇季后赛牛棚中最具威慑力的第九局人选。",
        "career": {"years": "11 年", "games": "500+", "era": "约 3.40", "ip": "500+", "strikeouts": "800+", "whip": "约 1.10", "saves": "200+", "awards": "2 次全明星 (2019, 2022), 2022 年 NL 年度救援投手前 3"},
        "arsenal": [
            {"name": "🔥 四缝线快速球", "en": "Four-Seam Fastball", "velo": "98-102 mph", "usage": "约 55%", "grade": "A+", "desc": "Diaz 的招牌球种，平均球速接近 100 mph，最高可达 102 mph。转速 elite，上升效应明显，是制造挥空和软弱飞球的核心武器。在健康状态下，速球的 command 和 late life 让他能在第九局对任何打者建立优势。"},
            {"name": "💫 滑球", "en": "Slider", "velo": "86-89 mph", "usage": "约 35%", "grade": "A", "desc": "sharp break 的滑球，横向位移大且下坠明显，是对付右打者的主要出局球。与速球形成 10+ mph 速差和明显位移差，破坏力极强。Diaz 常利用两好球后滑球追打右打者手套外侧角落。"},
            {"name": "⚡ 变速球/指叉", "en": "Changeup / Splitter", "velo": "88-91 mph", "usage": "约 10%", "grade": "B", "desc": "偶尔使用来打乱左打者节奏，使用频率不高但品质合格。主要作为配球工具，避免打者只准备速球-滑球二元组合。"},
        ],
        "analysis": "### 压制力\nDiaz 的压制力建立在速球-滑球组合之上。2025 年 K/9 高达 13.28，三振能力仍是联盟顶尖。但 2026 年 BB/9 飙升至 6.59，控球失稳是 ERA 暴涨的主因。速球被打得更扎实，可能与健康恢复节奏、release point 一致性不足有关。\n\n### 控球\n生涯 BB/9 约 3.0，2026 年小样本明显偏高。保送多集中在满球数和两好球后无法收尾，显示他的 command 尚未回到最佳状态。当他的身体状态和节奏找回后，保送率通常会回落。\n\n### 心理素质\nDiaz 长期担任大场面终结者，心理抗压能力是 elite 级别。2026 年的挣扎更像是伤病恢复期的波动，而非能力衰退。他在逆境中的调整能力是观察重点。\n\n### 伤病恢复\n2026 年赛季初进入伤病名单，导致错过大量常规赛季。回归后球速虽有，但速球品質和控球稳定性不足。9 月前能否回到 2025 年水准，将决定道奇是否放心让他在季后赛关门。",
        "pros": [
            "四缝线速球球速与转速均为联盟最顶级，最高可达 102 mph",
            "滑球是 signature out pitch，对右打者极具威胁",
            "历史级三振能力，健康时 K/9 长期维持 12+",
            "大场面心理素质优秀，多次在季后赛关键局登板",
            "2025 年仍是顶级救援水准，健康时值得信赖",
            "丰富的第九局经验，知道如何在一分差距局面控制节奏"
        ],
        "cons": [
            "2026 年伤愈回归后小样本表现极差，ERA 与 WHIP 均处于生涯最差区间",
            "近期保送率飙升，控球状态尚未恢复",
            "年龄 32 岁，伤病恢复后的续航与稳定性需观察",
            "配球以速球-滑球为主，若两球状态都不好时缺乏可靠第三球",
            "伤病史让道奇必须谨慎管理他的出赛频率"
        ],
        "grades": [
            {"tool": "速球", "score": 75, "grade": "A+"},
            {"tool": "滑球", "score": 65, "grade": "A"},
            {"tool": "控球", "score": 45, "grade": "B-"},
            {"tool": "指挥", "score": 55, "grade": "B"},
            {"tool": "耐力", "score": 50, "grade": "C+"},
            {"tool": "心理素质", "score": 70, "grade": "A"},
        ],
        "overall": {"score": 60, "grade": "A-", "label": "顶级终结者（需恢复状态）"},
        "career_highlights": [
            {"year": "2018", "title": "水手终结者爆发", "text": "以 57 次救援成功、1.96 ERA 的赛季震惊联盟，首次入选全明星，奠定顶级 closer 地位。"},
            {"year": "2019", "title": "交易至大都会", "text": "被水手交易至纽约大都会，经历调整期后逐步找回状态，成为球队后援核心。"},
            {"year": "2022", "title": "历史级救援赛季", "text": "1.31 ERA、118 次三振、32 次救援成功、0.84 WHIP，成为当年联盟最 dominant 的后援投手。"},
            {"year": "2023", "title": "WBC 受伤赛季报销", "text": "在世界棒球经典赛期间受伤，导致 MLB 赛季报销，职业生涯遭遇重大挫折。"},
            {"year": "2025", "title": "大都会顶级表现", "text": "62 场出赛、1.63 ERA、0.87 WHIP、98 次三振，证明仍是联盟最可靠终结者之一。"},
            {"year": "2026", "title": "加盟道奇后的伤病挑战", "text": "转战洛杉矶道奇，但赛季初长期养伤，8 月回归后仍在找回 2025 年的 elite 状态。"},
        ],
        "future": "短期关键是恢复健康与节奏。若能在 9 月前找回 2025 年的控球与速球威力，他仍是道奇季后赛最可靠的第九局人选。长期而言，32 岁的年龄和伤病史会让他逐渐从全年顶级下滑，但 1-2 年内仍有 elite closer 的实力。若 2026 年无法反弹，道奇可能需要在休赛季重新评估牛棚布局，甚至考虑寻找更年轻的终结者接班人。Diaz 的合同和履历让他有足够时间证明自己，但球队对他的耐心取决于季后赛前的表现。",
        "background": "Edwin Orlando Diaz 出生于波多黎各 Naguabo，2012 年选秀第 12 轮被明尼苏达双城选中，随后被交易至西雅图水手。2016 年 6 月 6 日，他在水手队完成大联盟首秀。2018 年，Diaz 以 57 次救援成功、1.96 ERA 的赛季震惊联盟，成为水手终结者并首次入选全明星。2019 年他被交易至纽约大都会，经历了一段调整期。2022 年 Diaz 达到生涯巅峰，以 1.31 ERA、118 次三振、32 次救援成功、0.84 WHIP 的成绩成为联盟最 dominant 的后援投手。2023 年他在世界棒球经典赛期间受伤导致 MLB 赛季报销。2025 年在大都会保持健康并延续顶级表现。2026 年加盟洛杉矶道奇，但因伤病影响赛季初长期缺阵，目前正在恢复中。",
        "has_velo_chart": True,
    }
    players.append(("edwin-diaz", edwin_info, edwin_current, parse_hist("621242", "pitching"), edwin_custom, True))

    # Jonathan Hernandez
    jonathan_current = {
        "games_played": 16, "games_started": 0, "wins": 0, "losses": 0,
        "era": "5.68", "innings_pitched": "25.1", "hits": 21,
        "runs": 16, "earned_runs": 16, "home_runs": 4, "strikeouts": 22,
        "walks": 13, "saves": 0, "holds": 0, "whip": "1.34",
        "strikeouts_per_9": "7.82", "walks_per_9": "4.62"
    }
    jonathan_info = {
        "full_name": "Jonathan Hernandez", "primary_number": "26", "position_name": "后援投手（长中继）",
        "throws": "右", "bats": "右", "birth_date": "1996-07-06", "age": 30,
        "height": "6' 3\"", "weight": 190, "mlb_debut_date": "2019-08-21"
    }
    jonathan_custom = {
        "slug": "jonathan-hernandez",
        "display_name": "Jonathan Hernandez",
        "nickname": "",
        "birthplace": "Memphis, Tennessee, USA（美国田纳西州孟菲斯）",
        "current_note": "2026 年在道奇主要担任长中继与低杠杆后援，样本不大但保送率和被全垒打率偏高，角色定位以吃局数和保护主力后援为主。",
        "summary": "Jonathan Hernandez 是一名右投后援，具备不错的速球-滑球基础，但控球稳定性和被长打控制一直是瓶颈。2026 年在道奇牛棚中担任深度后援/长中继角色，负责在球队大幅领先或落后时消耗局数，保护核心后援手臂。他的三振能力中等，BB/9 接近 4.6，需要在控球精进上持续努力。30 岁的他正处于投手成熟期，但若无明显进步，长期前景将停留在名单边缘。",
        "career": {"years": "7 年", "games": "120+", "era": "约 4.80", "ip": "150+", "strikeouts": "120+", "whip": "约 1.45", "saves": "0", "awards": "无"},
        "arsenal": [
            {"name": "🔥 四缝线快速球", "en": "Four-Seam Fastball", "velo": "94-97 mph", "usage": "约 50%", "grade": "B+", "desc": "均速约 95-96 mph 的速球，具备基本压制力，但转速和位移不算 elite，容易被打者扎实接触。需要更好的角落控制才能在高杠杆中存活。"},
            {"name": "💫 滑球", "en": "Slider", "velo": "84-87 mph", "usage": "约 35%", "grade": "B", "desc": "主要变化球，对右打者有一定威胁，但横向位移幅度和 sharpness 一般，控制落点能力尚需提升。"},
            {"name": "⚡ 伸卡球/二缝线", "en": "Sinker", "velo": "93-96 mph", "usage": "约 15%", "grade": "B-", "desc": "偶尔用于制造滚地球，但执行一致性不足，容易留在红中。"},
        ],
        "analysis": "### 压制力\nK/9 仅 7.82，低于联盟后援平均。他更依赖 contact 出局，而非三振。2026 年 ERA 5.68 反映出被安打和被全垒打控制不佳，尤其是 25.1 局被击出 4 轰，HR/9 高达 1.42。\n\n### 控球\nBB/9 4.62 偏高，长打控制差（4 HR in 25.1 IP）。这是他无法进入高杠杆的关键瓶颈。两好球后无法收尾的问题尤其明显。\n\n### 角色定位\nHernandez 在道奇牛棚中属于深度选项。在球队伤病或比分拉开时负责吃局数，保护核心后援。他的价值在于能吃 1-2 局，而不是 shut down 对手。\n\n### 发展潜力\n30 岁仍处于成熟期，但技术特征接近定型。若滑球 sharpness 和速球 command 没有提升，很难跳出 depth arm 角色。",
        "pros": [
            "速球球速具备大联盟后援基本门槛，可应付出赛",
            "可承担多局数任务，为轮值和主力后援争取休息",
            "右投对右打者组合（速球+滑球）有一定效果",
            "30 岁仍处于投手成熟期，仍有微调空间",
            "在道奇体系中可接受针对性机械调整"
        ],
        "cons": [
            "三振能力低于联盟平均，难以在高压局面对付 elite 打者",
            "保送率偏高，常陷入满垒危机",
            "被全垒打率偏高，长打控制差",
            "缺乏可靠的第三球种，配球可预测性高",
            "并非高杠杆材料，无法承担 setup 或 closer 角色"
        ],
        "grades": [
            {"tool": "速球", "score": 55, "grade": "B"},
            {"tool": "滑球", "score": 50, "grade": "C+"},
            {"tool": "控球", "score": 40, "grade": "C"},
            {"tool": "指挥", "score": 45, "grade": "B-"},
            {"tool": "耐力", "score": 55, "grade": "B"},
            {"tool": "心理素质", "score": 50, "grade": "C+"},
        ],
        "overall": {"score": 45, "grade": "B-", "label": "深度后援 / 长中继"},
        "career_highlights": [
            {"year": "2016", "title": "游骑兵签下国际自由球员", "text": "以国际自由球员身份加盟德州游骑兵，开启职业棒球生涯。"},
            {"year": "2019", "title": "大联盟首秀", "text": "2019 年 8 月 21 日在大联盟完成首秀，展现速球潜力但控球不稳。"},
            {"year": "2021", "title": "Tommy John 手术", "text": "接受手肘韧带重建手术，错过大量比赛，角色逐渐从先发转向后援。"},
            {"year": "2025", "title": "转战道奇", "text": "辗转来到洛杉矶道奇体系，在 3A 与大联盟之间往返，寻找稳定角色。"},
            {"year": "2026", "title": "道奇深度后援", "text": "在道奇牛棚担任长中继 / 低杠杆后援，负责吃局数和保护主力后援手臂。"},
        ],
        "future": "Hernandez 的未来取决于能否提升控球和降低保送。如果他能将 BB/9 压到 3.5 以下并减少长打，他有机会成为中等杠杆 setup man。否则他将长期停留在深度牛棚或 3A/MLB 边缘。道奇可能在未来寻求更稳定的右投后援来取代他的位置。30 岁是一个分水岭，若本季末无起色，他可能在休赛季被 DFA 或交易。",
        "background": "Jonathan Hernandez 于 2016 年以国际自由球员身份加盟德州游骑兵，2019 年 8 月 21 日在大联盟完成首秀。他在游骑兵时期展现了速球潜力，但控球始终不稳。2021 年接受 Tommy John 手术后，他的角色逐渐从先发转向后援。恢复后球速未完全回到巅峰，但他的多局数能力让他在牛棚中找到生存空间。2025-2026 年间辗转来到洛杉矶道奇，目前主要承担牛棚深度工作。",
        "has_velo_chart": False,
    }
    players.append(("jonathan-hernandez", jonathan_info, jonathan_current, parse_hist("642546", "pitching"), jonathan_custom, True))

    # Enrique Hernandez
    enrique_current = {
        "games_played": 16, "at_bats": 32, "plate_appearances": 33,
        "runs": 4, "hits": 8, "doubles": 2, "triples": 0, "home_runs": 2,
        "rbi": 5, "stolen_bases": 0, "walks": 1, "strikeouts": 9,
        "avg": ".250", "obp": ".273", "slg": ".500", "ops": ".773"
    }
    enrique_info = {
        "full_name": "Enrique Hernandez", "primary_number": "8", "position_name": "内野/外野多功能手",
        "throws": "右", "bats": "右", "birth_date": "1991-08-24", "age": 34,
        "height": "5' 10\"", "weight": 195, "mlb_debut_date": "2014-07-01"
    }
    enrique_custom = {
        "slug": "enrique-hernandez",
        "display_name": "Enrique Hernandez",
        "nickname": "Kiké",
        "birthplace": "San Juan, Puerto Rico（波多黎各圣胡安）",
        "current_note": "2026 年 8 月刚从伤病名单（IL-60）激活，目前处于回归调整期，打击样本极小（仅 33 打席），需持续观察。",
        "summary": "Enrique 'Kiké' Hernandez 是道奇阵中最具代表性的多功能工具人。他能在二垒、游击、三垒、外野多个位置提供联盟平均以上的防守，打击以拉开比分的全垒打和面对左投见长。2026 年上半季因伤长期缺阵，8 月才回归，目前处于找回节奏阶段。虽然 34 岁的年龄让他的运动能力有所下滑，但他的防守弹性和更衣室价值仍是道奇不可或缺的部分。他的存在让教练团在排兵布阵上拥有极大灵活性，尤其是在季后赛需要应急防守时。",
        "career": {"years": "12 年", "games": "1,100+", "avg": ".238", "obp": ".303", "slg": ".403", "ops": ".706", "hr": "110+", "rbi": "420+", "sb": "30+", "awards": "2020 年 NLCS 关键全垒打，2023 年世界棒球经典赛波多黎各代表队"},
        "tools": [
            {"name": "🎯 打击 (Hit)", "grade": "B-", "desc": "生涯 AVG 约 .238，不是高 average 型打者。主要价值在于 timely power 和选球后的长打。回归后小样本 AVG .250，需继续观察。他的挥棒路径适合拉打，容易把内角球扫成深远飞球。"},
            {"name": "💥 力量 (Power)", "grade": "B", "desc": "具备 15-20 轰单季产能，对左投尤其有长打威胁。2026 年回归后 2 轰 / 5 打点，长打率 .500 显示力量仍在。他的 power 分布偏拉打方向，左外野和右外野深区是他主要长打落点。"},
            {"name": "⚡ 速度 (Run)", "grade": "C+", "desc": "34 岁，速度明显下滑，盗垒产出有限，更多担任跑垒机会判断而非纯速度型跑者。他懂得如何利用中等速度做出聪明的跑垒决策。"},
            {"name": "🛡️ 防守 (Defense)", "grade": "A-", "desc": "Hernandez 最大的价值所在。能在二垒、游击、三垒、外野多位置提供平均以上防守，range 和传球准确性均不错。虽然不是金手套级别，但稳定可靠。"},
            {"name": "🎯 选球 (Plate Discipline)", "grade": "C+", "desc": "BB% 约 3% 在 2026 小样本偏低，生涯选球普通，主要依靠投手失误和特定配球进攻。他懂得在有利 count 出棒，但面对边缘球时耐心不足。"},
        ],
        "defense": "### 守备分析\nHernandez 是联盟知名的 utility player。他每个位置的防守都不算 elite，但全部在平均以上，特别是内野三站和右外野。他的传球准确、脚步灵活，能够在球队出现伤病时无缝顶上任何位置。2026 年回归后，他将主要作为替补守备 / 代打来使用。\n\n### 多功能性\n能同时镇守二垒、游击、三垒、外野，让他在道奇 28 人名单中极具战术价值。教练团可以根据对手投手左右手和当场比分灵活调度。他的多功能性是道奇过去几年多次夺冠的重要拼图。",
        "analysis": "### 打击分析\nHernandez 不是以打击率为卖点的球员。他的价值在于 occasional power 和打击串联。2026 年回归后 OPS .773 高于生涯平均，但样本仅 33 打席，不能过度解读。\n\n### 角色定位\n在道奇目前阵容中，他是 Max Muncy、Mookie Betts、Tommy Edman 等主力内野手的保险，同时也是面对左投时的潜在先发选项。他的存在让主力球员获得轮休机会而不牺牲太多防守。\n\n### 回归观察重点\n需要关注他是否能在有限打席中找回击球节奏，以及体能是否能支撑多位置防守。若无法适应大联盟节奏，他可能逐渐被年轻球员取代。",
        "pros": [
            "多才多艺，能守 6 个以上位置，阵容弹性极高",
            "对左投有不错长打能力，可作为 platoon 选项",
            "大场面经验丰富，2020 年季后赛表现令人印象深刻",
            "回归后力量输出仍在，2 轰 / .500 SLG 显示身体状况良好",
            " clubhouse 领袖气质，团队化学反应正面",
            "防守稳定性高，能在关键时刻顶替伤病球员"
        ],
        "cons": [
            "34 岁，运动能力和速度持续下滑",
            "对右投表现普通，不适合作为 everyday starter",
            "2026 年上半季重伤缺席，回归后状态不确定",
            "选球普通，容易 chasing 滑球和变化球",
            "防守范围不及专职内野手，只能作为保险"
        ],
        "grades": [
            {"tool": "打击", "score": 45, "grade": "B-"},
            {"tool": "力量", "score": 55, "grade": "B"},
            {"tool": "速度", "score": 45, "grade": "B-"},
            {"tool": "防守", "score": 65, "grade": "A-"},
            {"tool": "臂力", "score": 55, "grade": "B"},
            {"tool": "选球", "score": 45, "grade": "B-"},
            {"tool": "多功能性", "score": 70, "grade": "A"},
        ],
        "overall": {"score": 55, "grade": "B", "label": "优质多功能工具人"},
        "career_highlights": [
            {"year": "2014", "title": "大联盟首秀", "text": "在休斯顿太空人完成大联盟首秀，以多功能内野手身份进入联盟。"},
            {"year": "2015", "title": "加盟道奇", "text": "被交易至迈阿密马林鱼后随即加盟洛杉矶道奇，开启道奇生涯。"},
            {"year": "2020", "title": "冠军赛季关键先生", "text": "在道奇冠军赛季的季后赛多次击出关键全垒打，成为球迷喜爱的角色球员。"},
            {"year": "2023", "title": "WBC 波多黎各代表队", "text": "代表波多黎各参加世界棒球经典赛，展现国际赛舞台价值。"},
            {"year": "2026", "title": "伤愈回归", "text": "上半季因伤病进入 60 天伤病名单，8 月激活后正在努力恢复状态。"},
        ],
        "future": "2026 年剩余赛季，Hernandez 将争取在替补角色中稳定贡献。若身体允许，他可能获得面对左投的先发机会。2027 年他大概率继续以 veteran utility 身份留在联盟，但道奇需要开始培养更年轻的多功能替补。他的职业生涯尾声将以防守弹性和更衣室价值为主。若本季末表现出色，他仍有机会获得一份短期续约。",
        "background": "Enrique 'Kiké' Hernandez 出生于波多黎各圣胡安，2014 年 7 月 1 日在休斯顿太空人完成大联盟首秀。2015 年被交易到迈阿密马林鱼，随后加盟洛杉矶道奇。他在 2020 年道奇冠军赛季中多次在季后赛击出关键全垒打，成为球迷喜爱的角色球员。2023 年曾短暂离开道奇加盟波士顿红袜，2024 年回归道奇。2026 年上半季因伤病进入 60 天伤病名单，8 月激活后正在努力恢复状态。他是道奇近年来最受欢迎的 bench player 之一。",
    }
    players.append(("enrique-hernandez", enrique_info, enrique_current, parse_hist("571771", "batting"), enrique_custom, False))

    # Teoscar Hernandez
    teoscar_current = {
        "games_played": 93, "at_bats": 324, "plate_appearances": 358,
        "runs": 50, "hits": 81, "doubles": 14, "triples": 1, "home_runs": 11,
        "rbi": 43, "stolen_bases": 2, "walks": 29, "strikeouts": 97,
        "avg": ".250", "obp": ".313", "slg": ".401", "ops": ".714"
    }
    teoscar_info = {
        "full_name": "Teoscar Hernandez", "primary_number": "37", "position_name": "左外野手",
        "throws": "右", "bats": "右", "birth_date": "1992-10-15", "age": 33,
        "height": "6' 0\"", "weight": 215, "mlb_debut_date": "2016-08-12"
    }
    teoscar_custom = {
        "slug": "teoscar-hernandez",
        "display_name": "Teoscar Hernandez",
        "nickname": "",
        "birthplace": "Cotui, Dominican Republic（多米尼加共和国科图伊）",
        "current_note": "2026 赛季为道奇常规左外野手，已出赛 93 场，是主要轮值成员。数据截至 8 月 20 日。",
        "summary": "Teoscar Hernandez 是一名以力量见长的右打外野手，2026 年加入道奇后担任左外野主力。他具备稳定的中段打线和 25+ 轰级别的长打产能，但三振率偏高、选球普通，整体攻击效率接近联盟平均。他的防守在外野三个位置都能胜任，臂力是其守备亮点。2026 年截至目前 OPS .714，与生涯平均接近，但相较于 2024 年道奇赛季的 .840 OPS 有明显下滑。他需要在赛季末段提升长打效率，才能在季后赛打线中扮演更重要角色。",
        "career": {"years": "10 年", "games": "950+", "avg": ".255", "obp": ".313", "slg": ".460", "ops": ".773", "hr": "180+", "rbi": "520+", "sb": "40+", "awards": "2 次银棒奖 (2020, 2021), 2 次全明星 (2021, 2022)"},
        "tools": [
            {"name": "🎯 打击 (Hit)", "grade": "B-", "desc": "AVG .250、strikeout rate 约 27% 显示他不是高 contact 型打者，但 barrel 能力让他在球打甜时威胁极大。他的挥棒路径较长，容易在快速球和变化球交界处挥空。"},
            {"name": "💥 力量 (Power)", "grade": "A-", "desc": "生涯单季多次击出 25+ 轰，平均 exit velocity 和 hard-hit rate 位于联盟前段。2026 年 11 轰、.401 SLG 略低于巅峰，但仍是道奇主要 power source。他的 raw power 足以把球打到任何方向。"},
            {"name": "⚡ 速度 (Run)", "grade": "C+", "desc": "33 岁，速度已非卖点，2026 年仅 2 盗。跑垒判断尚可，但不适合担任开路先锋。他的速度足以在右外野防守中覆盖中等范围。"},
            {"name": "🛡️ 防守 (Defense)", "grade": "B", "desc": "左外野防守稳定，range 中等，接球手法可靠。臂力优于平均，能阻止跑者推进。他在外野角落位置的防守值得信赖。"},
            {"name": "🎯 选球 (Plate Discipline)", "grade": "C+", "desc": "BB% 约 8.1%，三振率偏高。面对变化球和边缘速球容易出棒，是主要被利用弱点。若能提升选球耐心，他的 OBP 和整体攻击效率会明显改善。"},
        ],
        "defense": "### 守备分析\nHernandez 主要镇守左外野，也能客串右外野。他的 first step 和 range 属联盟平均，但接球稳定、臂力突出，能有效阻止跑者从 singles 进垒到二垒。他不会是金手套候选人，但也不会成为防守负担。\n\n### 多功能性\n虽然以左外野为主，但在必要时也能担任指定打击或右外野。他的价值更多集中在打击输出而非守备弹性。道奇安排他左外野先发，是因为他在这个位置能最大化打击贡献同时不牺牲太多防守。",
        "analysis": "### 打击分析\n2026 年 OPS .714 接近生涯平均，但相较于 2020-2022 年的巅峰期（单季 OPS .800+）有所下滑。主要问题是三振率居高不下，且出棒范围大。他的 swing-and-miss 问题在面对 elite 变化球时尤其明显。\n\n### 长打效率\n.401 SLG 对于一名以力量为卖点的外野手来说偏低。若想在季后赛扮演更重要角色，他需要提升 barrel rate 和对变化球的识别。2024 年在道奇打出的 .501 SLG 证明他仍有能力，但 2025-2026 年呈现下滑趋势。\n\n### 角色定位\n在道奇打线中，Hernandez 主要担任第 5-7 棒，负责提供长打保护和 RBI 产出。他不是建队核心，但是阵容深度的关键拼图。面对左投时他的价值更高。",
        "pros": [
            "稳定的中段 power 产出，具备 25+ 轰产能",
            "hard-hit 能力强，击球初速联盟前列",
            "外野防守稳定，臂力优于平均",
            " postseason 经验丰富，多次帮助球队进入季后赛",
            "右打平衡道奇左打偏重的打线",
            "在道奇体系的击球教练帮助下仍有提升空间"
        ],
        "cons": [
            "三振率偏高，容易在关键时刻被三振出局",
            "选球普通，BB% 不高，上垒能力有限",
            "2026 年 SLG .401 低于生涯平均，力量输出有下滑迹象",
            "33 岁，运动能力进入衰退期",
            "对 elite 变化球和高速内角球应对不佳"
        ],
        "grades": [
            {"tool": "打击", "score": 45, "grade": "B-"},
            {"tool": "力量", "score": 65, "grade": "A-"},
            {"tool": "速度", "score": 45, "grade": "B-"},
            {"tool": "防守", "score": 50, "grade": "C+"},
            {"tool": "臂力", "score": 55, "grade": "B"},
            {"tool": "选球", "score": 45, "grade": "B-"},
        ],
        "overall": {"score": 55, "grade": "B", "label": "联盟平均以上 power 型外野手"},
        "career_highlights": [
            {"year": "2011", "title": "加盟太空人", "text": "以国际自由球员身份加盟休斯顿太空人，开启职业棒球生涯。"},
            {"year": "2016", "title": "大联盟首秀", "text": "2016 年 8 月 12 日完成大联盟首秀，初期在太空人机会有限。"},
            {"year": "2020-2021", "title": "蓝鸟银棒奖双连霸", "text": "在多伦多蓝鸟连续两个赛季获得美联外野手银棒奖，成为联盟顶尖 power 型外野手。"},
            {"year": "2021-2022", "title": "连续全明星", "text": "连续两年入选全明星赛，巅峰期 OPS 超过 .800，单季稳定贡献 25+ 轰。"},
            {"year": "2024", "title": "道奇强力赛季", "text": "在洛杉矶道奇打出 .272/.339/.501、33 轰、99 打点的赛季，展现冠军队所需火力。"},
            {"year": "2026", "title": "道奇常规左外野手", "text": "担任道奇左外野主力，负责提供中段打线长打保护和 RBI 产出。"},
        ],
        "future": "2026 年赛季剩余部分，Hernandez 需要提升长打率和减少三振，以维持道奇外野主力的位置。2027 年他仍有望获得一份合约，但随着年龄增长，他可能逐渐转为 platoon 外野手或指定打击。长期来看，他的 best-case 是成为一名 veteran power bat，worst-case 则是因三振率过高而失去先发位置。道奇可能会在休赛季评估是否引进更年轻、contact 能力更好的外野手。",
        "background": "Teoscar Hernandez 出生于多米尼加共和国科图伊，2011 年以国际自由球员身份加盟休斯顿太空人，2016 年 8 月 12 日完成大联盟首秀。他在太空人时期机会有限，2017 年被交易至多伦多蓝鸟后逐渐成长为全明星外野手。2020-2021 年连续获得美联外野手银棒奖，2021-2022 年连续两年入选全明星。2023 年转投西雅图水手，2024-2025 年持续贡献稳定 power 输出。2026 年加入洛杉矶道奇，希望在这座冠军球队中扮演重要角色。",
    }
    players.append(("teoscar-hernandez", teoscar_info, teoscar_current, parse_hist("606192", "batting"), teoscar_custom, False))

    # Seth Halvorsen
    seth_current = {
        "games_played": 1, "games_started": 0, "wins": 1, "losses": 0,
        "era": "0.00", "innings_pitched": "1.0", "hits": 0,
        "runs": 0, "earned_runs": 0, "home_runs": 0, "strikeouts": 0,
        "walks": 1, "saves": 0, "holds": 0, "whip": "1.00",
        "strikeouts_per_9": "0.00", "walks_per_9": "9.00"
    }
    seth_info = {
        "full_name": "Seth Halvorsen", "primary_number": "34", "position_name": "后援投手",
        "throws": "右", "bats": "右", "birth_date": "2000-02-18", "age": 26,
        "height": "6' 2\"", "weight": 243, "mlb_debut_date": "2024-08-30"
    }
    seth_custom = {
        "slug": "seth-halvorsen",
        "display_name": "Seth Halvorsen",
        "nickname": "",
        "birthplace": "Chicago, Illinois, USA（美国伊利诺伊州芝加哥）",
        "current_note": "2026 年仅 1 场大联盟出赛，为小样本临时上调。目前主要在小联盟 Oklahoma City Comets 发展，是 40 人名单末端的深度投手。",
        "summary": "Seth Halvorsen 是道奇农场体系中的年轻右投，2024 年完成大联盟首秀。他的速球具备不错潜力，但变化球和控球仍在发展中。2026 年大联盟样本极小，目前更属于 40 人名单末端的深度后援 / 未来牛棚潜力股。他的身体条件（6'2\" / 243 lbs）具备耐用型牛棚投手的体型，若能提升控球和变化球品质，有机会在未来 1-2 年站稳脚跟。",
        "career": {"years": "3 年", "games": "约 45", "era": "约 4.50", "ip": "45+", "strikeouts": "35+", "whip": "约 1.45", "saves": "0", "awards": "无"},
        "arsenal": [
            {"name": "🔥 四缝线快速球", "en": "Four-Seam Fastball", "velo": "94-97 mph", "usage": "约 55%", "grade": "B+", "desc": "速球是 Halvorsen 最好的武器，均速约 95-96 mph，occasionally 可上 97 mph。具备成为后援主力速球的基础，但转速和位移还有提升空间。"},
            {"name": "💫 滑球", "en": "Slider", "velo": "83-86 mph", "usage": "约 30%", "grade": "C+", "desc": "主要变化球，但 sharpness 和 consistency 不足，常被打者识别。需要增加横向位移和提高落点控制。"},
            {"name": "⚡ 变速球", "en": "Changeup", "velo": "86-89 mph", "usage": "约 15%", "grade": "C", "desc": "使用频率低，对左打者的 crossover 效果有限，需要继续打磨。若能发展出可靠的变速球，将显著提升他的上限。"},
        ],
        "analysis": "### 压制力\n2025 年小联盟 / 大联盟混合样本中 K/9 约 8.2，不算突出。他需要提升滑球品质和配球策略来制造更多挥空。速球虽然是 plus pitch，但单凭速球难以在大联盟长期生存。\n\n### 控球\nBB/9 在小联盟阶段偏高，2026 年唯一一场大联盟出赛也送出保送。控球是他能否站稳大联盟的关键。他需要改善 release point 的一致性，减少非受迫保送。\n\n### 角色定位\n目前是道奇 40 人名单的 emergency depth，大部分时间待在 3A。他的身体条件让他具备耐用型牛棚投手的体型，可在比分拉开时吃局数。\n\n### 发展潜力\n26 岁仍有发展空间。如果滑球和控球在未来 1-2 年进步明显，他有机会成为低-中等杠杆 setup man。否则将停留在名单边缘。",
        "pros": [
            "速球球速和体格条件具备大联盟后援潜力",
            "年仅 26 岁，仍有发展空间",
            "已在道奇体系中接受培养，熟悉球队哲学",
            "可担任多局数后援，增加轮值深度",
            "体型强壮，有成为耐用牛棚投手的身体基础"
        ],
        "cons": [
            "大联盟样本极小，经验严重不足",
            "变化球品质和一致性有待提升",
            "控球不稳，保送率偏高",
            "尚未证明能在高杠杆局面稳定出赛",
            "40 人名单边缘，可能面临 DFA 风险"
        ],
        "grades": [
            {"tool": "速球", "score": 55, "grade": "B"},
            {"tool": "滑球", "score": 45, "grade": "B-"},
            {"tool": "控球", "score": 40, "grade": "C"},
            {"tool": "指挥", "score": 40, "grade": "C"},
            {"tool": "耐力", "score": 50, "grade": "C+"},
            {"tool": "心理素质", "score": 45, "grade": "B-"},
        ],
        "overall": {"score": 45, "grade": "B-", "label": "潜力后援 / 名单边缘"},
        "career_highlights": [
            {"year": "2024", "title": "大联盟首秀", "text": "2024 年 8 月 30 日在洛杉矶道奇完成大联盟首秀，开启 MLB 生涯。"},
            {"year": "2025", "title": "3A 与大联盟之间往返", "text": "在 Oklahoma City Comets 与道奇大联盟名单之间多次升降，积累后援经验。"},
            {"year": "2026", "title": "名单边缘深度投手", "text": "进入道奇 40 人名单，但大联盟出赛机会有限，主要在小联盟持续磨练控球和变化球。"},
        ],
        "future": "Halvorsen 需要在 3A 持续稳定出赛，把 BB/9 压到 3.5 以下并提升滑球命中率。如果 2026 年 9 月扩编或明年春训表现出色，他有机会成为道奇牛棚的后段选项。长期天花板是中等杠杆 setup man，但若控球和变化球没有进步，他可能长期在小联盟 / DFA 之间徘徊。道奇农场深厚，他需要在与众多年轻后援的竞争中脱颖而出。",
        "background": "Seth Halvorsen 出生于芝加哥，2024 年 8 月 30 日在洛杉矶道奇完成大联盟首秀。他在道奇农场体系中逐渐从先发转向后援角色，依靠速球潜力获得 40 人名单一席。2025 年在 3A 与大联盟之间往返，2026 年仍处于职业生涯早期发展阶段。他在小联盟时期展现了一定的速球压制力，但控球和变化球发展较慢，目前仍在道奇体系的培养计划中。",
        "has_velo_chart": False,
    }
    players.append(("seth-halvorsen", seth_info, seth_current, parse_hist("678020", "pitching"), seth_custom, True))

    return players


def main():
    players = build_players()
    for slug, info, current, hist, custom, is_pitcher in players:
        if is_pitcher:
            md = make_pitcher_md(slug, info, current, hist, custom)
        else:
            md = make_hitter_md(slug, info, current, hist, custom)

        dir_path = f"D:/baseball/report/{slug}"
        os.makedirs(dir_path, exist_ok=True)

        md_path = os.path.join(dir_path, f"{slug}-scouting-report.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md)

        title = f"{custom['display_name']} 球探报告"
        html = convert_md_to_html(title, md, slug, is_pitcher)
        html_path = os.path.join(dir_path, f"{slug}-scouting-report.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"Generated: {md_path} ({len(md)} chars)")
        print(f"Generated: {html_path} ({len(html)} chars)")

if __name__ == "__main__":
    main()
