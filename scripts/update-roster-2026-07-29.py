#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update Dodgers roster snapshot and daily report for 2026-07-29."""

import json
import sys
from datetime import datetime
from pathlib import Path

import statsapi

ROSTER_DIR = Path(r"D:\baseball\roster")
DAILY_FILE = ROSTER_DIR / "2026-07-29.md"
LATEST_ROSTER = ROSTER_DIR / "dodgers-roster.md"

# Position mapping
POS_MAP = {
    "P": "投手",
    "C": "捕手",
    "1B": "一垒手",
    "2B": "二垒手",
    "3B": "三垒手",
    "SS": "游击手",
    "LF": "左外野",
    "CF": "中外野",
    "RF": "右外野",
    "TWP": "双向球员",
    "DH": "指定打击",
}

STATUS_MAP = {
    "A": "活跃",
    "RM": "小联盟",
    "D10": "IL-10",
    "D15": "IL-15",
    "D60": "IL-60",
}


def fetch_roster():
    data = statsapi.get("team_roster", {"teamId": 119, "rosterType": "40Man", "season": 2026})
    return data.get("roster", [])


def group_players(roster):
    groups = {
        "Pitchers": [],
        "Catchers": [],
        "Infielders": [],
        "Outfielders": [],
        "Two-Way": [],
    }
    for p in roster:
        pos_type = p.get("position", {}).get("type", "")
        pos_abbr = p.get("position", {}).get("abbreviation", "")
        if pos_abbr == "TWP":
            groups["Two-Way"].append(p)
        elif pos_type == "Pitcher":
            groups["Pitchers"].append(p)
        elif pos_type == "Catcher":
            groups["Catchers"].append(p)
        elif pos_type == "Infielder":
            groups["Infielders"].append(p)
        elif pos_type == "Outfielder":
            groups["Outfielders"].append(p)
        else:
            groups["Infielders"].append(p)
    return groups


def format_group(title, players, headers=None):
    if not players:
        return ""
    lines = [f"## {title}", ""]
    lines.append("| 球员 | 背号 | 状态 | 备注 |")
    lines.append("|------|------|------|------|")
    for p in players:
        name = p.get("person", {}).get("fullName", "")
        jersey = p.get("jerseyNumber", "—")
        status = p.get("status", {}).get("description", "")
        code = p.get("status", {}).get("code", "")
        status_cn = STATUS_MAP.get(code, status)
        note = p.get("note", "")
        lines.append(f"| {name} | {jersey} | {status_cn} | {note} |")
    lines.append("")
    return "\n".join(lines)


def generate_roster_md(roster, date_str):
    groups = group_players(roster)
    lines = [
        f"# 道奇队40人名单快照 — {date_str}",
        "",
    ]
    lines.append(format_group("投手 (Pitchers)", groups["Pitchers"]))
    lines.append(format_group("双向球员 (Two-Way)", groups["Two-Way"]))
    lines.append(format_group("捕手 (Catchers)", groups["Catchers"]))
    lines.append(format_group("内野手 (Infielders)", groups["Infielders"]))
    lines.append(format_group("外野手 (Outfielders)", groups["Outfielders"]))

    # Injury summary
    il10 = [p for p in roster if p.get("status", {}).get("code") == "D10"]
    il15 = [p for p in roster if p.get("status", {}).get("code") == "D15"]
    il60 = [p for p in roster if p.get("status", {}).get("code") == "D60"]

    lines.append("---")
    lines.append("")
    lines.append("## 伤病名单汇总")
    lines.append("")
    if il10:
        names = ", ".join([p.get("person", {}).get("fullName", "") for p in il10])
        lines.append(f"- **IL-10**: {names}")
    if il15:
        names = ", ".join([p.get("person", {}).get("fullName", "") for p in il15])
        lines.append(f"- **IL-15**: {names}")
    if il60:
        names = ", ".join([p.get("person", {}).get("fullName", "") for p in il60])
        lines.append(f"- **IL-60**: {names}")
    if not il10 and not il15 and not il60:
        lines.append("- 无伤病名单球员")
    lines.append("")
    lines.append(f"---")
    lines.append("")
    lines.append(f"*最新快照：{date_str}*")
    lines.append("")
    return "\n".join(lines)


DAILY_REPORT = """⚾ 道奇队日报 — 2026-07-29

📊 昨晚赛果
Seattle Mariners 7, 道奇 6

逐局比分：
```
         1 2 3 4 5 6 7 8 9  R  H  E
Mariners 0 1 0 3 0 1 0 2 0  7 10  2
Dodgers  1 0 1 2 1 0 0 0 1  6 13  0
```

胜负投手：W: Ferrer (4-1) / L: Stewart, B (0-1) / S: Muñoz, A (19)

关键得分：
• 1局下 — 大谷翔平 阳春本垒打（赛季第23轰），道奇 1-0
• 2局上 — Cal Raleigh 阳春本垒打（赛季第11轰），1-1
• 3局下 — Freddie Freeman 双杀打，Dalton Rushing 得分，道奇 2-1
• 4局上 — Julio Rodríguez 阳春本垒打（赛季第16轰），2-2
• 4局上 — Rob Refsnyder 两分本垒打（赛季第4轰），水手 4-2
• 4局下 — Tommy Edman 中外野二垒安打，Mookie Betts 得分，水手 4-3
• 4局下 — 大谷翔平 中外野安打，Tommy Edman 得分，4-4
• 5局下 — Max Muncy 阳春本垒打（赛季第21轰），道奇 5-4
• 6局上 — Dominic Canzone 阳春本垒打（赛季第17轰），5-5
• 8局上 — Dominic Canzone 两分本垒打（赛季第18轰），水手 7-5
• 9局下 — 大谷翔平 右外野二垒安打，Dalton Rushing 得分，水手 7-6

🔮 今日预告
道奇 vs 水手
🕐 10:10（北京时间，7月30日）
🏟️ UNIQLO Field at Dodger Stadium

先发投手：
  道奇: Eric Lauer (5-5, 4.83 ERA)
  水手: Emerson Hancock (6-4, 3.16 ERA)

🏥 伤病更新
当前伤病名单（无新增）：
• IL-15: Blake Treinen (P) — Right elbow inflammation
• IL-60: Ben Casparius (P), Blake Snell (P), Bobby Miller (P), Brusdar Graterol (P), Edwin Díaz (P), Gavin Stone (P), Jake Cousins (P), Tyler Glasnow (P), Will Smith (C)

👥 人员变动
发现变动：
• Enrique Hernández (1B) 从 IL-10 激活，回归活跃名单
• Alex Freeland (2B) 从活跃名单下放至小联盟
"""


def main():
    roster = fetch_roster()
    date_str = datetime.now().strftime("%Y-%m-%d")
    roster_md = generate_roster_md(roster, date_str)

    # Ensure directory exists
    ROSTER_DIR.mkdir(parents=True, exist_ok=True)

    # Write latest roster file
    LATEST_ROSTER.write_text(roster_md + "\n\n---\n\n## 比赛日报\n\n" + DAILY_REPORT, encoding="utf-8")
    print(f"[UPDATED] {LATEST_ROSTER}")

    # Write daily file (roster + daily report)
    DAILY_FILE.write_text(roster_md + "\n\n---\n\n## 比赛日报\n\n" + DAILY_REPORT, encoding="utf-8")
    print(f"[SAVED] {DAILY_FILE}")


if __name__ == "__main__":
    main()
