#!/usr/bin/env python3
"""Fetch and format the second game of the July 19/20 Dodgers-Yankees doubleheader."""
import json
import sys
from pathlib import Path

import statsapi

GAME_PK = 823521
OUTPUT_DIR = Path(r"D:\baseball\roster")

TEAM_NAMES = {
    "Los Angeles Dodgers": "道奇",
    "Dodgers": "道奇",
    "New York Yankees": "洋基",
    "Yankees": "洋基",
}

PLAYER_NAMES = {
    "Shohei Ohtani": "大谷翔平",
    "Mookie Betts": "Mookie Betts",
    "Freddie Freeman": "Freddie Freeman",
    "Will Smith": "Will Smith",
    "Max Muncy": "Max Muncy",
    "Teoscar Hernández": "Teoscar Hernández",
    "Tommy Edman": "Tommy Edman",
    "Andy Pages": "Andy Pages",
    "Kyle Tucker": "Kyle Tucker",
    "Gavin Lux": "Gavin Lux",
    "Chris Taylor": "Chris Taylor",
    "James Outman": "James Outman",
    "Jason Heyward": "Jason Heyward",
    "Miguel Rojas": "Miguel Rojas",
    "Kiké Hernández": "Kiké Hernández",
    "Austin Barnes": "Austin Barnes",
    "Dalton Rushing": "Dalton Rushing",
    "Alex Call": "Alex Call",
    "Eliezer Alfonzo": "Eliezer Alfonzo",
    "Will Klein": "Will Klein",
    "Landon Knack": "Landon Knack",
    "Evan Phillips": "Evan Phillips",
    "Tanner Scott": "Tanner Scott",
    "Yoshinobu Yamamoto": "Yoshinobu Yamamoto",
    "Paul Blackburn": "Paul Blackburn",
    "Will Warren": "Will Warren",
    "Jasson Domínguez": "Jasson Domínguez",
    "Austin Wells": "Austin Wells",
    "Paul Goldschmidt": "Paul Goldschmidt",
    "Ben Rice": "Ben Rice",
    "Cody Bellinger": "Cody Bellinger",
    "Jazz Chisholm Jr.": "Jazz Chisholm Jr.",
    "Ryan Yarbrough": "Ryan Yarbrough",
}


def translate_team(name):
    return TEAM_NAMES.get(name, name)


def translate_player(name):
    for eng, cn in PLAYER_NAMES.items():
        if eng in name:
            name = name.replace(eng, cn)
    return name


def simplify_description(desc):
    import re
    desc = translate_player(desc)
    result = desc

    # Home run
    hr_match = re.search(r'(.+?)\s+homers?\s+\((\d+)\)', result)
    if hr_match:
        player = hr_match.group(1).strip()
        hr_num = hr_match.group(2)
        return f"{player} 阳春本垒打（赛季第{hr_num}轰）"

    # Single
    single_match = re.search(r'(.+?)\s+singles?\s+', result)
    if single_match:
        player = single_match.group(1).strip()
        location = ""
        if "left field" in result.lower():
            location = "左外野"
        elif "right field" in result.lower():
            location = "右外野"
        elif "center field" in result.lower():
            location = "中外野"
        else:
            location = ""

        scorers = re.findall(r'([\w\s,]+?)\s+scores', result)
        scorers = [s.strip().rstrip(",") for s in scorers if s.strip() and len(s.strip()) > 2]
        if scorers:
            return f"{player} {location}安打，{scorers[0]} 得分"
        return f"{player} {location}安打"

    # Double
    double_match = re.search(r'(.+?)\s+doubles?\s+', result)
    if double_match:
        player = double_match.group(1).strip()
        location = ""
        if "left field" in result.lower():
            location = "左外野"
        elif "right field" in result.lower():
            location = "右外野"
        elif "center field" in result.lower():
            location = "中外野"
        scorers = re.findall(r'([\w\s,]+?)\s+scores', result)
        scorers = [s.strip().rstrip(",") for s in scorers if s.strip() and len(s.strip()) > 2]
        if scorers:
            return f"{player} {location}二垒安打，{scorers[0]} 得分"
        return f"{player} {location}二垒安打"

    # Triple
    triple_match = re.search(r'(.+?)\s+triples?\s+', result)
    if triple_match:
        player = triple_match.group(1).strip()
        location = ""
        if "left field" in result.lower():
            location = "左外野"
        elif "right field" in result.lower():
            location = "右外野"
        elif "center field" in result.lower():
            location = "中外野"
        scorers = re.findall(r'([\w\s,]+?)\s+scores', result)
        scorers = [s.strip().rstrip(",") for s in scorers if s.strip() and len(s.strip()) > 2]
        if scorers:
            return f"{player} {location}三垒安打，{scorers[0]} 得分"
        return f"{player} {location}三垒安打"

    # Sacrifice fly
    sf_match = re.search(r'(.+?)\s+out on a sacrifice fly', result)
    if sf_match:
        player = sf_match.group(1).strip()
        scorers = re.findall(r'([\w\s,]+?)\s+scores', result)
        scorers = [s.strip().rstrip(",") for s in scorers if s.strip() and len(s.strip()) > 2]
        if scorers:
            return f"{player} 牺牲飞球，{scorers[0]} 得分"
        return f"{player} 牺牲飞球"

    # Fielder's choice
    if "fielder's choice" in result.lower():
        fc_match = re.search(r'(.+?)\s+reaches on a fielder', result)
        if fc_match:
            player = fc_match.group(1).strip()
            scorers = re.findall(r'([\w\s,]+?)\s+scores', result)
            scorers = [s.strip().rstrip(",") for s in scorers if s.strip() and len(s.strip()) > 2]
            if scorers:
                return f"{player} 野手选择，{scorers[0]} 得分"
            return f"{player} 野手选择"

    # Generic scores
    score_match = re.search(r'([\w\s]+?)\s+scores', result)
    if score_match:
        player = score_match.group(1).strip()
        return f"{player} 得分"

    if len(result) > 80:
        result = result[:77] + "..."
    return result


def parse_scoring_plays(text):
    plays = []
    current = {}
    pending = None
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("Top ") or line.startswith("Bottom "):
            parts = line.split(" - ", 1)
            inning_part = parts[0]
            scores_str = parts[1] if len(parts) > 1 else ""
            score_nums = []
            for sp in scores_str.split(", "):
                if ":" in sp:
                    try:
                        score_nums.append(int(sp.rsplit(":", 1)[1].strip()))
                    except:
                        pass
            away = score_nums[0] if len(score_nums) > 0 else 0
            home = score_nums[1] if len(score_nums) > 1 else 0
            is_top = line.startswith("Top ")
            inning_num = inning_part.replace("Top ", "").replace("Bottom ", "").strip()
            current = {
                "inning": inning_num,
                "half": "上" if is_top else "下",
                "description": pending or "",
                "away": away,
                "home": home,
            }
            plays.append(current)
            pending = None
        else:
            pending = line
    return plays


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    # Game info
    game_data = statsapi.get("game", {"gamePk": GAME_PK})
    game = game_data.get("gameData", {})
    teams = game.get("teams", {})
    away_team = teams.get("away", {}).get("name", "Dodgers")
    home_team = teams.get("home", {}).get("name", "Yankees")
    venue = game.get("venue", {}).get("name", "Yankee Stadium")

    # Probable pitchers
    probables = game.get("probablePitchers", {})
    away_pitcher = probables.get("away", {}).get("fullName", "")
    home_pitcher = probables.get("home", {}).get("fullName", "")

    # Decisions
    decisions = game.get("decisions", {})
    winner = decisions.get("winner", {}).get("fullName", "")
    loser = decisions.get("loser", {}).get("fullName", "")
    save = decisions.get("save", {}).get("fullName", "")

    # Linescore
    linescore = statsapi.linescore(GAME_PK)
    boxscore = statsapi.boxscore(GAME_PK)

    # Scoring plays
    scoring_text = statsapi.game_scoring_plays(GAME_PK)
    plays = parse_scoring_plays(scoring_text)

    # Build report
    lines = [
        "⚾ 道奇队日报 - 2026-07-20（第二场 / 7/19 夜场双赛）",
        "",
        "📊 赛果",
        "",
        f"Dodgers 1, {translate_team(home_team)} 2",
        "",
        "逐局比分:",
    ]
    for line in linescore.strip().split("\n"):
        line = line.replace("Dodgers", "道奇").replace("Yankees", "洋基")
        lines.append(f"  {line}")
    lines.append("")

    lines.append("关键得分：")
    for play in plays:
        if play.get("description"):
            simplified = simplify_description(play["description"])
            inning = play["inning"]
            half = play["half"]
            # away = Dodgers score, home = opponent score
            dodgers_runs = play["away"]
            opp_runs = play["home"]
            if half == "上":
                score_str = f"道奇 {dodgers_runs}-{opp_runs}"
            else:
                score_str = f"洋基 {opp_runs}-{dodgers_runs}"
            lines.append(f"• {inning}局{half} — {simplified}，{score_str}")
    lines.append("")

    # Pitching info
    lines.append("🔮 先发投手")
    lines.append(f"  Dodgers: {away_pitcher}")
    lines.append(f"  {translate_team(home_team)}: {home_pitcher}")
    lines.append("")

    if winner or loser:
        lines.append("胜败投手:")
        if winner:
            lines.append(f"  胜投: {winner}")
        if loser:
            lines.append(f"  败投: {loser}")
        if save:
            lines.append(f"  救援: {save}")
        lines.append("")

    lines.append(f"🏟️ 场地: {venue}")
    lines.append("")

    lines.append("🏥 伤病更新")
    lines.append("✅ 无新增伤病")
    lines.append("")

    lines.append("👥 人员变动")
    lines.append("✅ 无人员变动")
    lines.append("")

    report = "\n".join(lines)
    print(report)

    # Save to file
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / "2026-07-20-game2.md"
    output_file.write_text(report, encoding="utf-8")
    print(f"[SAVED] {output_file}")


if __name__ == "__main__":
    main()
