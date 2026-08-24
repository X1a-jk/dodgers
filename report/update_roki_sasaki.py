#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update Roki Sasaki scouting report with latest 2026 stats and refreshed analysis,
and regenerate a Tanner-Scott-style HTML for consistency with the other 5 reports.
"""
import os

REPORT_DATE = "2026-08-21"
DATA_DATE = "2026-08-20"

info = {
    "full_name": "Roki Sasaki",
    "display_name": "佐佐木朗希 (Roki Sasaki)",
    "primary_number": "11",
    "position_name": "先发投手",
    "throws": "右",
    "bats": "右",
    "birth_date": "2001-11-03",
    "age": 24,
    "height": "6'2\"",
    "weight": 187,
    "mlb_debut_date": "2025-03-19",
    "birthplace": "日本岩手县陆前高田市",
    "nickname": "令和怪物 (Monster of the Reiwa Era)",
}

current_2026 = {
    "games_played": 22, "games_started": 22, "wins": 5, "losses": 5,
    "era": "4.42", "innings_pitched": "116.0", "hits": 105,
    "runs": 59, "earned_runs": 57, "home_runs": 21, "strikeouts": 114,
    "walks": 46, "whip": "1.30", "strikeouts_per_9": "8.84", "walks_per_9": "3.57"
}

hist_2025 = {
    "season": "2025", "team": "Los Angeles Dodgers",
    "gamesPlayed": 10, "gamesStarted": 8, "wins": 1, "losses": 1,
    "era": "4.46", "inningsPitched": "36.1", "hits": 30,
    "strikeOuts": 28, "baseOnBalls": 22, "whip": "1.43",
    "strikeoutsPer9Inn": "6.94", "walksPer9Inn": "5.45", "homeRuns": 6, "saves": 0
}

custom = {
    "slug": "roki-sasaki",
    "nickname": "令和怪物 (Monster of the Reiwa Era)",
    "birthplace": "日本岩手县陆前高田市",
    "summary": "佐佐木朗希是日本棒球界近年来最具天赋的投手之一，被誉为'令和时代的怪物'。他以惊人的速球和犀利的指叉球闻名，高中时期就曾投出时速101英里的快速球。2022年4月10日，他在日本职棒投出了完全比赛，单场19次三振、连续13次三振均创下纪录。2025年加入洛杉矶道奇后，经历了适应期。进入2026赛季，他已从轮值边缘人成长为稳定的先发投手：截至8月20日，22场先发5胜5负、ERA 4.42、116.0局、114次三振，K/9从2025年的6.94提升至8.84，BB/9从5.45大幅降至3.57，WHIP从1.43降至1.30。虽然仍偶有大比分失分，但整体趋势明显向上，已具备大联盟轮值中坚投手的雏形。",
    "career": {"years": "2年", "games": "32", "era": "约4.44", "ip": "152.1", "strikeouts": "142", "whip": "1.34", "saves": "0", "awards": "NPB 完全比赛 (2022), 日美顶级新秀"},
    "arsenal": [
        {"name": "🔥 四缝线快速球", "en": "Four-Seam Fastball", "velo": "96-101 mph", "usage": "约50%", "grade": "A+", "desc": "佐佐木的招牌球种，高中时期就达到101mph。平均球速约98mph，上旋强烈，具有极佳的上升轨迹，能够制造大量挥空。2026年三振能力回升，速球品质仍是 elite 级别。"},
        {"name": "💫 指叉球", "en": "Split-Finger", "velo": "87-91 mph", "usage": "约30%", "grade": "A+", "desc": "极具破坏力的变化球，下落幅度大，速度落差明显。是佐佐木解决打者的关键武器，对左右打者都能制造挥空。"},
        {"name": "🌪️ 滑球", "en": "Slider", "velo": "84-88 mph", "usage": "约15%", "grade": "B", "desc": "横向位移明显的滑球，对右打者极具威胁。与快速球搭配使用时效果显著，但仍需提升对左打者的压制力。"},
        {"name": "⚡ 曲球", "en": "Curveball", "velo": "78-82 mph", "usage": "约5%", "grade": "C+", "desc": "偶尔使用的变化球，主要用于打乱打者节奏。仍在开发中，若能提升稳定性，将成为重要的第四球种。"},
    ],
    "analysis": "### 投球机制\n佐佐木采用高上肩（Over-the-top）的投球机制，出手点高，能够充分运用身高优势制造下坠角度。投球动作流畅，身体协调性出色，虽然投球动作中有些许复杂度，但整体重复性良好。\n\n### 速球品质\n四缝线快速球是他的致命武器，平均球速约98mph，最高可达101mph以上。球的旋转效率极高，产生强烈的上升效应，使得打者常常挥空或击出高飞球。2026年他的三振能力明显回升，速球仍是主要压制手段。\n\n### 控球进步\n控球是佐佐木过去最大的挑战，但2026年已有显著改善。BB/9从2025年的5.45降至3.57，保送率大幅下降。随着信心提升，他在好球带边缘的command越来越稳定，早期 inning 的控球问题减少。\n\n### 体力与耐力\n作为年轻投手，佐佐木的体能管理仍在开发中，但已有明显进步。2026年每季投球局数从36.1局大幅提升至116局，显示球队对他的信任和身体的成长。若能持续健康，他有望在赛季末接近180局。\n\n### 被长打问题\n目前主要隐患是被全垒打率偏高（2026年21轰/116局，HR/9约1.63）。这反映他偶尔会把速球留在红中，或变化球失投。改善策略执行和球路混合是下一步关键。",
    "pros": [
        "顶级速球，最高可达101mph+",
        "指叉球极具破坏力，三振利器",
        "2026年控球大幅进步，BB/9从5.45降至3.57",
        "三振能力回升，K/9从6.94提升至8.84",
        "投球动作流畅，身体协调性好",
        "心理素质强，大场面不怯场",
        "年轻，潜力巨大，只有24岁",
        "已成长为稳定轮值成员，局数大幅增加",
        "日本职棒完全比赛经验"
    ],
    "cons": [
        "被全垒打率仍偏高（HR/9约1.63）",
        "变化球控制不够稳定，偶尔会失投",
        "面对左打者表现略差",
        "仍偶有大比分失分场次",
        "MLB经验相对较少，仍在学习联盟打者",
        "曲球/变速球作为第四球种尚未成熟"
    ],
    "grades": [
        {"tool": "速球", "score": 75, "grade": "A+"},
        {"tool": "指叉球", "score": 75, "grade": "A+"},
        {"tool": "滑球", "score": 55, "grade": "B"},
        {"tool": "曲球", "score": 45, "grade": "C+"},
        {"tool": "控球", "score": 50, "grade": "B-"},
        {"tool": "指挥", "score": 60, "grade": "B"},
        {"tool": "心理素质", "score": 65, "grade": "A-"},
        {"tool": "耐力", "score": 60, "grade": "B-"},
    ],
    "overall": {"score": 60, "grade": "B+", "label": "未来轮值核心"},
    "future": "佐佐木朗希无疑是道奇队未来轮值的重要一环。2026年的进步证明他正在适应大联盟：控球改善、三振回升、局数增加。只要保持健康并继续降低保送与全垒打，他有望在未来2-3年内成为球队的王牌投手。\n\n### 发展建议\n1. **继续改善控球：** 将BB/9进一步压至3.0以下，提升早期 inning 效率。\n2. **减少被全垒打：** 改善速球位置，避免把球留在红中。\n3. **面对左打者：** 加强对左打者的应对策略，增加变化球和指叉球的使用。\n4. **提升耐力：** 目标2026年突破160局，2027年挑战180局。\n5. **开发第四球种：** 让曲球或变速球成为稳定的配球工具。\n\n### 预期发展轨迹\n- **2026-2027：** 稳定轮值成员，ERA目标3.80-4.30，每季160+局\n- **2028-2029：** 轮值前段投手，ERA目标3.20-3.70，入选全明星\n- **2030+：** 王牌投手候选人，赛扬奖竞争者",
    "background": "佐佐木朗希的名字源自日本特摄剧《百兽战队牙吠连者》中的反派角色'六鬼'（Rokui）。他有两个兄弟，分别是龙树（Ryuki）和怜树（Reiki）。\n\n2011年3月11日，年仅9岁的佐佐木正在陆前高田市立高田小学读三年级。那天，日本发生了里氏9.1级的大地震，随后引发了巨大的海啸。佐佐木在这场灾难中失去了父亲和祖父母。陆前高田市超过1,750名市民在这场灾难中遇难或失踪。\n\n这段经历深深影响了佐佐木。在2025年加盟道奇队的记者会上（当时正值洛杉矶山火肆虐），他说道：'我也曾经历过灾难，遭受过很多痛苦，但我努力不要忘记始终向前看。'\n\n佐佐木在高中时期就被称为'令和时代的怪物'，这个绰号是对前辈松坂大辅（被称为'平成时代的怪物'）的致敬。高中时他的快速球就达到了101mph。\n\n2022年4月10日，他在日本职棒投出了完全比赛，成为日本职棒史上第16位达成此成就的投手，也是自1994年牧原成以来首位。那场比赛他三振19人，包括连续13次三振，创下了日本职棒纪录。\n\n加盟道奇队后，队友米格尔·罗哈斯（Miguel Rojas）将自己的11号球衣让给了他。作为感谢，佐佐木送给罗哈斯三瓶清酒和一套酒具。",
    "career_highlights": [
        {"year": "2022", "title": "NPB 完全比赛", "text": "在罗德海洋投出完全比赛，单场19次三振、连续13次三振，均创下日本职棒纪录。"},
        {"year": "2025", "title": "加盟道奇与大联盟首秀", "text": "转战洛杉矶道奇，3月19日完成大联盟首秀，成为球队备受期待的新秀先发。"},
        {"year": "2025", "title": "适应期", "text": "10场出赛（8场先发），1胜1负、ERA 4.46、36.1局，BB/9偏高（5.45），仍在适应MLB节奏。"},
        {"year": "2026", "title": "站稳轮值", "text": "截至8月20日，22场先发5胜5负、ERA 4.42、116.0局、114K，BB/9降至3.57，K/9提升至8.84。"},
    ],
    "has_velo_chart": True,
}


def make_md():
    c = current_2026
    h = hist_2025
    md = f"""# {info['display_name']} 球探报告

> **Los Angeles Dodgers #{info['primary_number']} | {info['position_name']} | {info['throws']}投/{info['bats']}打 | {info['nickname']}**
> 
> 报告生成时间：{REPORT_DATE} | 数据截止日期：{DATA_DATE}

---

## 📋 基本信息

| 项目 | 内容 |
|------|------|
| **姓名** | {info['display_name']} |
| **出生日期** | {info['birth_date']} |
| **年龄** | {info['age']}岁 |
| **出生地** | {info['birthplace']} |
| **身高/体重** | {info['height']} / {info['weight']} lbs |
| **投球/击球** | {info['throws']}投 / {info['bats']}打 |
| **MLB首秀** | {info['mlb_debut_date']} |
| **背号** | #{info['primary_number']} |
| **绰号** | {info['nickname']} |

### 球探总评

{custom['summary']}

---

## 📊 2026赛季统计数据

| 统计项目 | 数值 |
|----------|------|
| **出赛 (G)** | {c['games_played']} |
| **先发 (GS)** | {c['games_started']} |
| **胜场 (W)** | {c['wins']} |
| **败场 (L)** | {c['losses']} |
| **自责分率 (ERA)** | {c['era']} |
| **投球局数 (IP)** | {c['innings_pitched']} |
| **被安打 (H)** | {c['hits']} |
| **自责分 (ER)** | {c['earned_runs']} |
| **全垒打 (HR)** | {c['home_runs']} |
| **三振 (SO)** | {c['strikeouts']} |
| **保送 (BB)** | {c['walks']} |
| **WHIP** | {c['whip']} |
| **K/9** | {c['strikeouts_per_9']} |
| **BB/9** | {c['walks_per_9']} |

> ⚠️ **注意**：2026年数据截至8月20日。佐佐木本赛季局数与三振能力较2025年均有显著提升，但偶有大比分失分与被全垒打问题仍需改善。

---

## 📊 赛季对比

| 赛季 | 球队 | 出赛 | 先发 | 胜 | 败 | ERA | IP | 三振 | 保送 | WHIP | K/9 | BB/9 |
|------|------|------|------|-----|-----|------|------|------|------|------|------|------|
| {h['season']} | {h['team']} | {h['gamesPlayed']} | {h['gamesStarted']} | {h['wins']} | {h['losses']} | {h['era']} | {h['inningsPitched']} | {h['strikeOuts']} | {h['baseOnBalls']} | {h['whip']} | {h['strikeoutsPer9Inn']} | {h['walksPer9Inn']} |
| 2026 | Los Angeles Dodgers | {c['games_played']} | {c['games_started']} | {c['wins']} | {c['losses']} | {c['era']} | {c['innings_pitched']} | {c['strikeouts']} | {c['walks']} | {c['whip']} | {c['strikeouts_per_9']} | {c['walks_per_9']} |

---

## 🏆 职业生涯数据

| 统计项目 | 数值 |
|----------|------|
| **MLB年资** | {custom['career']['years']} |
| **总出赛** | {custom['career']['games']} |
| **生涯ERA** | {custom['career']['era']} |
| **生涯IP** | {custom['career']['ip']} |
| **生涯三振** | {custom['career']['strikeouts']} |
| **生涯WHIP** | {custom['career']['whip']} |
| **主要荣誉** | {custom['career']['awards']} |

---

## 🎯 投球武器库

"""
    for a in custom["arsenal"]:
        md += f"""### {a['name']} ({a['en']})
- **球速**：{a['velo']}
- **使用占比**：{a['usage']}
- **评分**：**{a['grade']}**
- {a['desc']}

"""

    md += f"""---

## 🔍 球探分析

{custom['analysis']}

---

## ✅ 优势 vs ❌ 劣势

### 优势 (Strengths)
"""
    for p in custom["pros"]:
        md += f"- ✅ {p}\n"

    md += "\n### 劣势 (Weaknesses)\n"
    for c_item in custom["cons"]:
        md += f"- ❌ {c_item}\n"

    md += f"""
---

## 📊 综合评分

| 项目 | 评分 (20-80) | 等级 |
|------|-------------|------|
"""
    for g in custom["grades"]:
        md += f"| {g['tool']} | {g['score']} | {g['grade']} |\n"
    overall = custom["overall"]
    md += f"""\n### 总体评分：{overall['score']} ({overall['grade']} 级 / {overall['label']})

---

## 🔮 未来展望

{custom['future']}

---

## 📖 背景故事

{custom['background']}

---

## 📈 图表附录

- 报告封面：![{info['display_name']} 报告封面](./sasaki_report_cover.png)
- 赛季对比：![{info['display_name']} 赛季对比](./sasaki_season_comparison.png)
- 综合评分雷达图：![{info['display_name']} 综合评分](./sasaki_overall_grades.png)
- 球速分布：![{info['display_name']} 球速分布](./sasaki_pitch_velocities.png)
- 比赛趋势：![{info['display_name']} 比赛趋势](./sasaki_game_trends.png)

---

*数据来源：MLB.com | Baseball Savant | MLB Stats API*
*报告生成：{REPORT_DATE}*
"""
    return md


def grade_class(grade):
    if grade.startswith("A"):
        return "grade-a"
    if grade.startswith("B"):
        return "grade-b"
    if grade.startswith("C"):
        return "grade-c"
    return "grade-d"


def make_tanner_html():
    slug = "roki-sasaki"
    display = info["display_name"]
    position_line = f"Los Angeles Dodgers #{info['primary_number']} | {info['position_name']} | 活跃"

    basic_items = [
        ("全名", display),
        ("出生日期", info["birth_date"]),
        ("年龄", f"{info['age']}岁"),
        ("出生地", info["birthplace"]),
        ("身高/体重", f"{info['height']} / {info['weight']} lbs"),
        ("投球/击球", f"{info['throws']}投 / {info['bats']}打"),
        ("位置", info["position_name"]),
        ("MLB首秀", info["mlb_debut_date"]),
        ("背号", f"#{info['primary_number']}"),
        ("绰号", info["nickname"]),
    ]
    info_grid_html = "\n".join(
        f"""<div class="info-item"><div class="label">{label}</div><div class="value">{value}</div></div>"""
        for label, value in basic_items
    )

    summary_paras = f"<p style='margin-bottom: 15px;'>{custom['summary']}</p>"

    highlights_html = "\n".join(
        f"""<div class="career-highlight"><h4>🌟 {h['year']} - {h['title']}</h4><p>{h['text']}</p></div>"""
        for h in custom["career_highlights"]
    )

    c = current_2026
    stat_cards = [
        ("出赛", c["games_played"]), ("先发", c["games_started"]), ("胜", c["wins"]),
        ("败", c["losses"]), ("ERA", c["era"]), ("IP", c["innings_pitched"]),
        ("K", c["strikeouts"]), ("BB", c["walks"]), ("WHIP", c["whip"]),
        ("K/9", c["strikeouts_per_9"]), ("BB/9", c["walks_per_9"]), ("HR", c["home_runs"]),
    ]
    stats_grid_html = "\n".join(
        f"""<div class="stat-card"><span class="stat-value" style="color: #4fc3f7;">{val}</span><div class="stat-label">{label}</div></div>"""
        for label, val in stat_cards
    )

    h = hist_2025
    comp_header = "<th>赛季</th><th>球队</th><th>G</th><th>GS</th><th>W</th><th>L</th><th>ERA</th><th>IP</th><th>K</th><th>BB</th><th>WHIP</th><th>K/9</th><th>BB/9</th>"
    comp_rows = [
        f"<td>{h['season']}</td><td>{h['team']}</td><td>{h['gamesPlayed']}</td><td>{h['gamesStarted']}</td><td>{h['wins']}</td><td>{h['losses']}</td><td>{h['era']}</td><td>{h['inningsPitched']}</td><td>{h['strikeOuts']}</td><td>{h['baseOnBalls']}</td><td>{h['whip']}</td><td>{h['strikeoutsPer9Inn']}</td><td>{h['walksPer9Inn']}</td>",
        f"<td class='warning'>2026</td><td>Los Angeles Dodgers</td><td>{c['games_played']}</td><td>{c['games_started']}</td><td>{c['wins']}</td><td>{c['losses']}</td><td>{c['era']}</td><td>{c['innings_pitched']}</td><td>{c['strikeouts']}</td><td>{c['walks']}</td><td>{c['whip']}</td><td>{c['strikeouts_per_9']}</td><td>{c['walks_per_9']}</td>",
    ]
    comp_rows_html = "\n".join(f"<tr>{row}</tr>" for row in comp_rows)

    velo_img_html = f"""<div style="text-align: center; margin: 20px 0;"><img src="sasaki_pitch_velocities.png" alt="投球武器库速度" style="width: 100%; max-width: 900px; border-radius: 10px;"><p style="text-align: center; color: #90a4ae; font-size: 0.95em; margin-top: 10px;">⚾ 各球种球速区间（蓝=最低球速，橙=最高球速，红线=平均值）。球速差与位移差越大，打者越难锁定单一球路。</p></div>"""
    pitch_cards = "\n".join(
        f"""<div class="pitch-card"><h3>{a['name']} ({a['en']})</h3><p><span class="velocity">{a['velo']}</span></p><p>{a['desc']}</p></div>"""
        for a in custom["arsenal"]
    )

    def fmt_analysis(text):
        out = []
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("### "):
                out.append(f"<h3 style='color: #4fc3f7; margin: 20px 0 15px 0;'>{s[4:]}</h3>")
            elif s:
                out.append(f"<p>{s}</p>")
        return "\n".join(out)

    analysis_paras = fmt_analysis(custom["analysis"])
    future_paras = fmt_analysis(custom["future"])
    background_paras = fmt_analysis(custom["background"])

    pros_html = "\n".join(f"<li>{p}</li>" for p in custom["pros"])
    cons_html = "\n".join(f"<li>{c}</li>" for c in custom["cons"])

    grade_cards = "\n".join(
        f"""<div class="stat-card"><span class="stat-value" style="color: #4fc3f7;">{g['score']}</span><div class="stat-label">{g['tool']}</div><span class="grade {grade_class(g['grade'])}">{g['grade']}</span></div>"""
        for g in custom["grades"]
    )
    overall = custom["overall"]

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{display} 球探报告</title>
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
  <img src="sasaki_report_cover.png" alt="报告封面" style="width: 100%; max-width: 750px;">
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
  <h2>📊 2026赛季投球数据</h2>
  <div class="stats-grid">
    {stats_grid_html}
  </div>
</div>

<div class="section">
  <h2>📊 赛季对比</h2>
  <h3 style="margin-top: 20px; color: #4fc3f7;">投球数据对比</h3>
  <table class="comparison-table">
    <thead><tr>{comp_header}</tr></thead>
    <tbody>{comp_rows_html}</tbody>
  </table>
</div>

<div class="section">
  <h2>🎯 投球武器库</h2>
  {velo_img_html}
  <div class="pitch-arsenal">
    {pitch_cards}
  </div>
</div>

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
    <img src="sasaki_overall_grades.png" alt="综合评分雷达图" style="max-width: 600px;">
  </div>
  <div class="stats-grid">
    {grade_cards}
  </div>
  <div style="margin-top: 30px; text-align: center;">
    <h3 style="color: #4fc3f7; margin-bottom: 15px;">总体潜力评分</h3>
    <div style="font-size: 4em; color: #4caf50; font-weight: bold;">{overall['score']}</div>
    <p style="color: #90a4ae; margin-top: 10px;">{overall['label']}</p>
    <p style="margin-top: 15px;"><span class="grade {grade_class(overall['grade'])}" style="font-size: 1.2em;">{overall['grade']} 级</span></p>
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
  <p>报告生成时间：{REPORT_DATE} | 数据截止日期：{DATA_DATE}</p>
  <p>⚾ 洛杉矶道奇队球探报告</p>
</div>

</div>
</body>
</html>"""
    return html


def main():
    dir_path = "D:/baseball/report/roki-sasaki"

    md = make_md()
    md_path = os.path.join(dir_path, "roki-sasaki-scouting-report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Updated MD: {md_path} ({len(md)} chars)")

    # backup old html
    html_path = os.path.join(dir_path, "roki-sasaki-scouting-report.html")
    if os.path.exists(html_path):
        bak_path = os.path.join(dir_path, "roki-sasaki-scouting-report.html.bak2")
        import shutil
        shutil.copy2(html_path, bak_path)
        print(f"Backed up old HTML to: {bak_path}")

    html = make_tanner_html()
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Updated HTML: {html_path} ({len(html)} chars)")


if __name__ == "__main__":
    main()
