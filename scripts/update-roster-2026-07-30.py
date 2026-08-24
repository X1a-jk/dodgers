#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update Dodgers roster snapshot from mlb.com 40-man roster (2026-07-30).

MLB API is currently unreachable, so this script uses the roster data extracted
from https://www.mlb.com/dodgers/roster/40-man and transaction notes from
https://www.mlb.com/dodgers/roster/transactions.
"""

from datetime import datetime
from pathlib import Path

ROSTER_DIR = Path(r"D:\baseball\roster")
LATEST_ROSTER = ROSTER_DIR / "dodgers-roster.md"
DAILY_FILE = ROSTER_DIR / "2026-07-30.md"

STATUS_MAP = {
    "A": "活跃",
    "RM": "小联盟",
    "D10": "IL-10",
    "D15": "IL-15",
    "D60": "IL-60",
}

# Roster data extracted from mlb.com/dodgers/roster/40-man on 2026-07-30.
# Format: (name, jersey, status_code, note)
ROSTER_DATA = {
    "Pitchers": [
        ("Ben Casparius", "78", "D60", ""),
        ("Jake Cousins", "", "D60", ""),
        ("Edwin Díaz", "3", "A", ""),
        ("Jack Dreyer", "86", "A", ""),
        ("Carlos Duran", "", "RM", ""),
        ("Paul Gervase", "65", "RM", ""),
        ("Tyler Glasnow", "31", "D60", ""),
        ("Brusdar Graterol", "48", "D60", ""),
        ("Seth Halvorsen", "", "RM", ""),
        ("Edgardo Henriquez", "60", "A", ""),
        ("Kyle Hurt", "63", "RM", ""),
        ("Will Klein", "61", "A", ""),
        ("Landon Knack", "96", "RM", ""),
        ("Ronan Kopp", "83", "RM", ""),
        ("Eric Lauer", "33", "A", ""),
        ("Chayce McDermott", "62", "RM", ""),
        ("Bobby Miller", "28", "D60", ""),
        ("Wyatt Mills", "58", "RM", ""),
        ("Evan Phillips", "59", "A", ""),
        ("River Ryan", "77", "RM", ""),
        ("Roki Sasaki", "11", "A", ""),
        ("Tanner Scott", "66", "A", ""),
        ("Emmet Sheehan", "80", "A", ""),
        ("Blake Snell", "7", "D60", ""),
        ("Brock Stewart", "41", "A", ""),
        ("Gavin Stone", "35", "D60", ""),
        ("Blake Treinen", "49", "D15", ""),
        ("Alex Vesia", "51", "A", ""),
        ("Justin Wrobleski", "70", "A", ""),
        ("Yoshinobu Yamamoto", "18", "A", ""),
    ],
    "Two-Way": [
        ("Shohei Ohtani", "17", "A", ""),
    ],
    "Catchers": [
        ("Eliezer Alfonzo", "64", "A", ""),
        ("Dalton Rushing", "68", "A", ""),
        ("Will Smith", "16", "D60", ""),
    ],
    "Infielders": [
        ("Mookie Betts", "50", "A", ""),
        ("Alex Freeland", "76", "RM", ""),
        ("Freddie Freeman", "5", "A", ""),
        ("Enrique Hernández", "8", "A", ""),
        ("Hyeseong Kim", "6", "RM", ""),
        ("Max Muncy", "13", "A", ""),
        ("Miguel Rojas", "72", "A", ""),
    ],
    "Outfielders": [
        ("Alex Call", "12", "A", ""),
        ("Tommy Edman", "25", "A", ""),
        ("Teoscar Hernández", "37", "A", ""),
        ("Andy Pages", "44", "A", ""),
        ("Alek Thomas", "5", "RM", ""),
        ("Kyle Tucker", "23", "A", ""),
        ("Ryan Ward", "67", "RM", ""),
    ],
}


def format_group(title, players):
    lines = [f"## {title}", ""]
    lines.append("| 球员 | 背号 | 状态 | 备注 |")
    lines.append("|------|------|------|------|")
    for name, jersey, code, note in players:
        status_cn = STATUS_MAP.get(code, code)
        lines.append(f"| {name} | {jersey} | {status_cn} | {note} |")
    lines.append("")
    return "\n".join(lines)


def generate_roster_md(date_str):
    lines = [f"# 道奇队40人名单快照 — {date_str}", ""]
    for title, players in ROSTER_DATA.items():
        cn_title = {
            "Pitchers": "投手 (Pitchers)",
            "Two-Way": "双向球员 (Two-Way)",
            "Catchers": "捕手 (Catchers)",
            "Infielders": "内野手 (Infielders)",
            "Outfielders": "外野手 (Outfielders)",
        }[title]
        lines.append(format_group(cn_title, players))

    # Injury summary
    all_players = [p for group in ROSTER_DATA.values() for p in group]
    il10 = [p for p in all_players if p[2] == "D10"]
    il15 = [p for p in all_players if p[2] == "D15"]
    il60 = [p for p in all_players if p[2] == "D60"]

    lines.append("---")
    lines.append("")
    lines.append("## 伤病名单汇总")
    lines.append("")
    if il10:
        names = ", ".join([p[0] for p in il10])
        lines.append(f"- **IL-10**: {names}")
    if il15:
        names = ", ".join([p[0] for p in il15])
        lines.append(f"- **IL-15**: {names}")
    if il60:
        names = ", ".join([p[0] for p in il60])
        lines.append(f"- **IL-60**: {names}")
    if not il10 and not il15 and not il60:
        lines.append("- 无伤病名单球员")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*最新快照：{date_str}*")
    lines.append("")
    return "\n".join(lines)


DAILY_REPORT = """⚾ 道奇队日报 - 2026-07-30

📊 昨晚赛果

Seattle Mariners 2, 道奇 4

逐局比分:
  Final    1 2 3 4 5 6 7 8 9  R   H   E  
  Mariners 0 0 0 0 0 0 0 1 1  2   5   0  
  道奇  1 0 1 1 0 1 0 0 0  4   11  1

关键得分：
• 1局下 — Andy Pages 阳春本垒打（赛季第18轰），比分 1-0
• 3局下 — Freddie Freeman 三垒方向安打，大谷翔平 得分，比分 2-0
• 4局下 — Andy Pages 游击方向安打，Mookie Betts 得分，比分 3-0
• 6局下 — 大谷翔平 中外野二垒安打，Dalton Rushing 得分，比分 4-0
• 8局上 — Cole Young 中外野安打，Weston Wilson 得分，比分 4-1
• 9局上 — Josh Naylor 右外野二垒安打，Dominic Canzone 得分，比分 4-2

🔮 今日预告

道奇 vs 水手
🕐 10:10 (北京时间)
🏟️ UNIQLO Field at Dodger Stadium

先发投手:
  道奇: Roki Sasaki (4-5, 4.71 ERA)

🏥 伤病更新
✅ 无新增伤病

👥 人员变动
• Charlie Barnes (LHP) 被指定让渡（DFA），已不在 40-man roster 中
• Edwin Díaz (RHP) 从 60-day IL 激活，回归活跃名单
"""


def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    roster_md = generate_roster_md(date_str)

    ROSTER_DIR.mkdir(parents=True, exist_ok=True)

    full_md = roster_md + "\n\n---\n\n## 比赛日报\n\n" + DAILY_REPORT

    LATEST_ROSTER.write_text(full_md, encoding="utf-8")
    print(f"[UPDATED] {LATEST_ROSTER}")

    DAILY_FILE.write_text(full_md, encoding="utf-8")
    print(f"[SAVED] {DAILY_FILE}")


if __name__ == "__main__":
    main()
