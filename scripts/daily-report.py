#!/usr/bin/env python3
"""
道奇队日报格式化脚本
调用 mlb-daily-scores skill,输出中文格式的日报
"""

import json
import subprocess
import sys
import re
import statsapi
from datetime import datetime, timedelta
from pathlib import Path

ROSTER_DIR = Path(r"D:\baseball\roster")
LATEST_ROSTER = ROSTER_DIR / "dodgers-roster.md"
MLB_SKILL = Path(r"C:\Users\Junkai XIA\.openclaw\workspace\skills\mlb-daily-scores\fetch_mlb.py")
GROUP_ORDER = ["投手", "双向球员", "捕手", "内野手", "外野手"]
STATUS_MAP = {"A": "活跃", "RM": "小联盟", "D10": "IL-10", "D15": "IL-15", "D60": "IL-60"}
GROUP_MAP = {
    "Pitcher": "投手",
    "Catcher": "捕手",
    "Infielder": "内野手",
    "Outfielder": "外野手",
    "Two-Way Player": "双向球员",
}


def fetch_daily_report() -> dict:
    """调用 mlb-daily-scores skill 获取数据"""
    if not MLB_SKILL.exists():
        print("[ERROR] mlb-daily-scores skill not found")
        return {}

    try:
        result = subprocess.run(
            [sys.executable, str(MLB_SKILL),
             "--team", "Los Angeles Dodgers",
             "--timezone", "Asia/Shanghai"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=120
        )
        # Parse JSON from stdout (ignore stderr)
        data = json.loads(result.stdout)
        return data
    except Exception as e:
        print(f"[ERROR] Failed to fetch daily report: {e}")
        return {}


def parse_scoring_plays(scoring_text: str, team_name: str = "Dodgers") -> list[str]:
    """Parse and translate scoring plays into Chinese key-moment format.

    Input format:
        Shohei Ohtani homers (22) on a fly ball to center field.
        Bottom 1 - Arizona Diamondbacks: 0, Los Angeles Dodgers: 1

    Output format:
        ["1局下 - 大谷翔平 阳春本垒打(赛季第22轰),道奇 1-0", ...]
    """
    if not scoring_text:
        return []

    # Player name translations (common Dodgers + opponents)
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
        "Ketel Marte": "Ketel Marte",
        "Geraldo Perdomo": "Geraldo Perdomo",
        "Corbin Carroll": "Corbin Carroll",
        "Lourdes Gurriel Jr.": "Lourdes Gurriel Jr.",
        "Gabriel Moreno": "Gabriel Moreno",
        "Christian Walker": "Christian Walker",
        "Jake McCarthy": "Jake McCarthy",
        "Eugenio Suárez": "Eugenio Suárez",
        "Alek Thomas": "Alek Thomas",
        "Blaze Alexander": "Blaze Alexander",
        "Pavin Smith": "Pavin Smith",
        "Ildemaro Vargas": "Ildemaro Vargas",
        "Nolan Arenado": "Nolan Arenado",
        "Tim Tawa": "Tim Tawa",
        "Ryan Waldschmidt": "Ryan Waldschmidt",
        "Jorge Barrosa": "Jorge Barrosa",
        "Bryson Stott": "Bryson Stott",
        "Trea Turner": "Trea Turner",
        "Realmuto": "J.T. Realmuto",
        "Gabriel Rincones Jr.": "Gabriel Rincones Jr.",
        "Brandon Marsh": "Brandon Marsh",
        "Nick Castellanos": "Nick Castellanos",
        "Bryce Harper": "Bryce Harper",
        "Kyle Schwarber": "Kyle Schwarber",
        "Alec Bohm": "Alec Bohm",
        "Johan Rojas": "Johan Rojas",
        "Edmundo Sosa": "Edmundo Sosa",
        "Whit Merrifield": "Whit Merrifield",
        "Weston Wilson": "Weston Wilson",
        "Rodolfo Castro": "Rodolfo Castro",
        "Rafael Marchán": "Rafael Marchán",
        "Garrett Stubbs": "Garrett Stubbs",
        "Kody Clemens": "Kody Clemens",
        "Darick Hall": "Darick Hall",
        "Cristian Pache": "Cristian Pache",
        "Cal Stevenson": "Cal Stevenson",
        "Buddy Kennedy": "Buddy Kennedy",
    }

    # Team name translations
    TEAM_NAMES = {
        "Arizona Diamondbacks": "响尾蛇",
        "Diamondbacks": "响尾蛇",
        "D-backs": "响尾蛇",
        "San Diego Padres": "教士",
        "Padres": "教士",
        "Los Angeles Dodgers": "道奇",
        "Dodgers": "道奇",
        "San Francisco Giants": "巨人",
        "Giants": "巨人",
        "Colorado Rockies": "洛矶",
        "Rockies": "洛矶",
        "New York Yankees": "洋基",
        "Yankees": "洋基",
        "New York Mets": "大都会",
        "Mets": "大都会",
        "Atlanta Braves": "勇士",
        "Braves": "勇士",
        "Philadelphia Phillies": "费城人",
        "Phillies": "费城人",
        "Chicago Cubs": "小熊",
        "Cubs": "小熊",
        "Milwaukee Brewers": "酿酒人",
        "Brewers": "酿酒人",
        "Cincinnati Reds": "红人",
        "Reds": "红人",
        "St. Louis Cardinals": "红雀",
        "Cardinals": "红雀",
        "Pittsburgh Pirates": "海盗",
        "Pirates": "海盗",
        "Washington Nationals": "国民",
        "Nationals": "国民",
        "Miami Marlins": "马林鱼",
        "Marlins": "马林鱼",
        "Houston Astros": "太空人",
        "Astros": "太空人",
        "Texas Rangers": "游骑兵",
        "Rangers": "游骑兵",
        "Seattle Mariners": "水手",
        "Mariners": "水手",
        "Oakland Athletics": "运动家",
        "Athletics": "运动家",
        "A's": "运动家",
        "Los Angeles Angels": "天使",
        "Angels": "天使",
    }

    # Parse plays into structured events
    plays = []
    pending_description = None
    dodgers_is_home = None

    for line in scoring_text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue

        # Check if this is a score line like "Bottom 1 - Arizona Diamondbacks: 0, Los Angeles Dodgers: 1"
        if line.startswith("Top ") or line.startswith("Bottom "):
            # Parse inning info
            parts = line.split(" - ", 1)
            inning_part = parts[0]  # "Bottom 1" or "Top 5"
            scores_str = parts[1] if len(parts) > 1 else ""

            # Parse scores and team names
            score_entries = []
            for sp in scores_str.split(", "):
                if ":" in sp:
                    try:
                        team_name = ":".join(sp.rsplit(":", 1)[0].strip().split(":")[1:]) if sp.count(":") > 1 else sp.rsplit(":", 1)[0].strip()
                        score = int(sp.rsplit(":", 1)[1].strip())
                        score_entries.append((team_name, score))
                    except:
                        pass

            away_score = score_entries[0][1] if len(score_entries) > 0 else 0
            home_score = score_entries[1][1] if len(score_entries) > 1 else 0
            away_team = score_entries[0][0] if len(score_entries) > 0 else ""
            home_team = score_entries[1][0] if len(score_entries) > 1 else ""

            # Determine if Dodgers are home or away
            if dodgers_is_home is None:
                dodgers_is_home = "Los Angeles Dodgers" in home_team or "Dodgers" == home_team

            # Determine top/bottom
            is_top = line.startswith("Top ")
            inning_num = inning_part.replace("Top ", "").replace("Bottom ", "").strip()

            plays.append({
                "inning": inning_num,
                "half": "上" if is_top else "下",
                "description": pending_description or "",
                "away_score": away_score,
                "home_score": home_score,
                "dodgers_is_home": dodgers_is_home,
            })
            pending_description = None
        else:
            # This is a play description - save for next inning line
            pending_description = line

    # Don't forget the last play if there's a pending description without inning info
    if pending_description and not plays:
        plays.append({
            "inning": "",
            "half": "",
            "description": pending_description,
            "away_score": 0,
            "home_score": 0,
            "dodgers_is_home": dodgers_is_home if dodgers_is_home is not None else True,
        })

    # Now format each play into Chinese
    formatted = []
    for play in plays:
        desc = play.get("description", "")
        inning = play.get("inning", "")
        half = play.get("half", "")
        away_s = play.get("away_score", 0)
        home_s = play.get("home_score", 0)
        is_home = play.get("dodgers_is_home", True)

        if not desc:
            continue

        # Translate player names
        translated_desc = desc
        for eng_name, cn_name in PLAYER_NAMES.items():
            translated_desc = translated_desc.replace(eng_name, cn_name)

        # Simplify play description
        simplified = simplify_play_description(translated_desc)

        # Format score: Dodgers score first
        if is_home:
            dodgers_s, opp_s = home_s, away_s
        else:
            dodgers_s, opp_s = away_s, home_s

        formatted.append(f"{inning}局{half} — {simplified}，比分 {dodgers_s}-{opp_s}")

    return formatted


def simplify_play_description(desc: str) -> str:
    """Simplify MLB play description into concise Chinese."""
    import re

    result = desc

    # Home run patterns
    # "大谷翔平 homers (22) on a fly ball to center field." → "大谷翔平 阳春本垒打(赛季第22轰)"
    hr_match = re.search(r'(.+?) homers? \((\d+)\)', result)
    if hr_match:
        player = hr_match.group(1).strip()
        hr_num = hr_match.group(2)
        # Check if solo or with runners on
        if "scores" in result.lower() and result.lower().count("scores") > 1:
            # Multiple runners scored = grand slam or multi-run HR
            if result.lower().count("scores") >= 4:
                return f"{player} 满贯本垒打（赛季第{hr_num}轰）"
            else:
                runners = result.lower().count("scores")
                return f"{player} {runners}分本垒打（赛季第{hr_num}轰）"
        else:
            # Check if there are runners on base mentioned
            if any(word in result.lower() for word in ["first baseman", "second baseman", "third baseman"]):
                # Has runners on - check how many
                runner_count = 0
                if "first baseman" in result.lower() or "second baseman" in result.lower() or "third baseman" in result.lower():
                    runner_count = 1  # Approximate
                if runner_count > 0:
                    return f"{player} {runner_count+1}分本垒打（赛季第{hr_num}轰）"
            return f"{player} 阳春本垒打（赛季第{hr_num}轰）"

    # Single patterns
    # "Tommy Edman singles on a fly ball to left fielder..." → "Tommy Edman 左外野安打"
    single_match = re.search(r'(.+?) singles? ', result)
    if single_match:
        player = single_match.group(1).strip()
        # Extract where the hit went
        location = ""
        if "left field" in result.lower():
            location = "左外野"
        elif "right field" in result.lower():
            location = "右外野"
        elif "center field" in result.lower():
            location = "中外野"
        elif "shortstop" in result.lower():
            location = "游击方向"
        elif "third baseman" in result.lower():
            location = "三垒方向"
        elif "second baseman" in result.lower() or "second base" in result.lower():
            location = "二垒方向"
        elif "first baseman" in result.lower():
            location = "一垒方向"

        # Extract who scored
        scored_players = []
        score_pattern = re.findall(r'([\w\s,]+?) scores', result)
        for sp in score_pattern:
            name = sp.strip().rstrip(",")
            if name and name != player and len(name) > 2:
                scored_players.append(name)

        if scored_players:
            if len(scored_players) == 1:
                return f"{player} {location}安打，{scored_players[0]} 得分"
            else:
                scorers = "、".join(scored_players)
                return f"{player} {location}安打，{scorers} 得分"
        else:
            return f"{player} {location}安打"

    # Ground into double play (run can still score)
    gdp_match = re.search(r'(.+?) grounds into a double play', result, re.IGNORECASE)
    if gdp_match:
        player = gdp_match.group(1).strip()
        scored_players = []
        score_pattern = re.findall(r'([\w\s,]+?) scores', result)
        for sp in score_pattern:
            name = sp.strip().rstrip(",")
            if name and name != player and len(name) > 2:
                scored_players.append(name)
        if scored_players:
            return f"{player} 双杀打，{scored_players[0]} 得分"
        return f"{player} 双杀打"

    # Double patterns
    double_match = re.search(r'(.+?) doubles? ', result)
    if double_match:
        player = double_match.group(1).strip()
        location = ""
        if "left field" in result.lower():
            location = "左外野"
        elif "right field" in result.lower():
            location = "右外野"
        elif "center field" in result.lower():
            location = "中外野"

        scored_players = []
        score_pattern = re.findall(r'([\w\s,]+?) scores', result)
        for sp in score_pattern:
            name = sp.strip().rstrip(",")
            if name and name != player and len(name) > 2:
                scored_players.append(name)

        if scored_players:
            scorers = "、".join(scored_players) if len(scored_players) > 1 else scored_players[0]
            return f"{player} {location}二垒安打，{scorers} 得分"
        else:
            return f"{player} {location}二垒安打"

    # Sacrifice fly
    sf_match = re.search(r'(.+?) out on a sacrifice fly', result)
    if sf_match:
        player = sf_match.group(1).strip()
        scored_players = []
        score_pattern = re.findall(r'([\w\s,]+?) scores', result)
        for sp in score_pattern:
            name = sp.strip().rstrip(",")
            if name and name != player and len(name) > 2:
                scored_players.append(name)

        if scored_players:
            return f"{player} 牺牲飞球，{scored_players[0]} 得分"
        return f"{player} 牺牲飞球"

    # Fielder's choice / error
    if "fielder's choice" in result.lower():
        fc_match = re.search(r'(.+?) reaches on a fielder', result)
        if fc_match:
            player = fc_match.group(1).strip()
            scored_players = []
            score_pattern = re.findall(r'([\w\s,]+?) scores', result)
            for sp in score_pattern:
                name = sp.strip().rstrip(",")
                if name and name != player and len(name) > 2:
                    scored_players.append(name)

            if "error" in result.lower():
                return f"{player} 野手选择（对方失误），{scored_players[0] if scored_players else ''} 得分"
            if scored_players:
                return f"{player} 野手选择，{scored_players[0]} 得分"
            return f"{player} 野手选择"

    # Generic "scores" pattern for anything else
    score_match = re.search(r'([\w\s]+?) scores', result)
    if score_match:
        player = score_match.group(1).strip()
        return f"{player} 得分"

    # If nothing matched, return shortened version
    # Limit to ~80 chars
    if len(result) > 80:
        result = result[:77] + "..."
    return result


def find_prev_roster_file(today_str: str) -> Path:
    """Find the most recent dated roster file before today."""
    today = datetime.strptime(today_str, "%Y-%m-%d").date()
    candidates = sorted(
        [p for p in ROSTER_DIR.glob("*.md") if re.match(r"\d{4}-\d{2}-\d{2}\.md", p.name)],
        key=lambda p: p.name,
        reverse=True,
    )
    for p in candidates:
        d = datetime.strptime(p.stem, "%Y-%m-%d").date()
        if d < today:
            return p
    return LATEST_ROSTER


def parse_existing_roster(path: Path) -> dict:
    """Parse roster tables from a markdown file (ignoring the daily report section)."""
    prev = {}
    if not path.exists():
        return prev
    text = path.read_text(encoding="utf-8")
    marker = "\n---\n\n## 比赛日报"
    if marker in text:
        text = text.split(marker)[0]
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 5 and parts[1] and parts[1] != "球员" and not any("---" in p for p in parts):
            prev[parts[1]] = {"status": parts[3], "note": parts[4] if len(parts) > 4 else ""}
    return prev


def fetch_40man_roster() -> list:
    """Fetch the Dodgers 40-man roster from the MLB Stats API."""
    try:
        data = statsapi.get("team_roster", {"teamId": 119, "rosterType": "40Man", "season": datetime.now().year})
        return data.get("roster", [])
    except Exception as e:
        print(f"[ERROR] Failed to fetch 40-man roster: {e}")
        return []


def build_roster_markdown(roster: list, prev: dict, today: str) -> str:
    """Build the 40-man roster markdown section."""
    from collections import defaultdict
    groups = defaultdict(list)
    for p in roster:
        group = GROUP_MAP.get(p["position"]["type"], p["position"]["type"])
        groups[group].append(p)

    md_lines = [f"# 道奇队40人名单快照 — {today}", ""]
    for group in GROUP_ORDER:
        if group not in groups:
            continue
        players = sorted(groups[group], key=lambda x: x["person"]["fullName"])
        md_lines.append(f"## {group} ({group})")
        md_lines.append("")
        md_lines.append("| 球员 | 背号 | 状态 | 备注 |")
        md_lines.append("|------|------|------|------|")
        for p in players:
            name = p["person"]["fullName"]
            jersey = p.get("jerseyNumber", "") or ""
            status = STATUS_MAP.get(p["status"]["code"], p["status"]["code"])
            injury_note = p.get("note", "")
            prev_info = prev.get(name, {})
            prev_status = prev_info.get("status", "")
            prev_note = prev_info.get("note", "")
            note = ""
            if prev_status and prev_status != status:
                if prev_status == "未报到":
                    note = f"已报到并进入{status}"
                elif status == "小联盟":
                    note = f"从 {prev_status} 下放至小联盟"
                elif status == "活跃":
                    note = f"从 {prev_status} 上调至活跃名单"
                else:
                    note = f"从 {prev_status} 变为 {status}"
            elif not prev_status:
                note = "新加入40人名单"
            else:
                note = prev_note if prev_note else injury_note
            md_lines.append(f"| {name} | {jersey} | {status} | {note} |")
        md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## 伤病名单汇总")
    md_lines.append("")
    injury_lists = {"IL-10": [], "IL-15": [], "IL-60": []}
    for p in roster:
        status = STATUS_MAP.get(p["status"]["code"], p["status"]["code"])
        if status in injury_lists:
            injury_lists[status].append(p["person"]["fullName"])
    for status, names in injury_lists.items():
        if names:
            md_lines.append(f"- **{status}**: {', '.join(names)}")
    md_lines.append("")
    return "\n".join(md_lines)


def detect_roster_changes(roster: list, prev: dict) -> list:
    """Compare current roster with previous snapshot and return changes."""
    current = {p["person"]["fullName"]: p for p in roster}
    prev_names = set(prev.keys())
    cur_names = set(current.keys())
    changes = []
    for name in sorted(cur_names - prev_names):
        p = current[name]
        changes.append({
            "type": "added",
            "name": name,
            "jersey": p.get("jerseyNumber", "") or "N/A",
            "status": STATUS_MAP.get(p["status"]["code"], p["status"]["code"]),
            "position": p["position"]["abbreviation"],
        })
    for name in sorted(prev_names - cur_names):
        changes.append({"type": "removed", "name": name})
    for name in sorted(cur_names & prev_names):
        prev_status = prev[name]["status"]
        cur_status = STATUS_MAP.get(current[name]["status"]["code"], current[name]["status"]["code"])
        if prev_status != cur_status:
            changes.append({"type": "status", "name": name, "prev": prev_status, "current": cur_status})
    return changes


def format_roster_changes(changes: list) -> str:
    """Format roster changes for the daily report."""
    if not changes:
        return "\n👥 人员变动\n\n✅ 无人员变动\n\n"
    lines = ["", "👥 人员变动", ""]
    added = [c for c in changes if c["type"] == "added"]
    removed = [c for c in changes if c["type"] == "removed"]
    status_changes = [c for c in changes if c["type"] == "status"]
    if added:
        lines.append("🔥 新增40人名单")
        for c in added:
            lines.append(f"• {c['name']}（#{c['jersey']}，{c['status']}，{c['position']}）")
        lines.append("")
    if removed:
        lines.append("❌ 移出40人名单")
        for c in removed:
            lines.append(f"• {c['name']}")
        lines.append("")
    if status_changes:
        lines.append("🔄 状态变化")
        for c in status_changes:
            lines.append(f"• {c['name']}：{c['prev']} → {c['current']}")
        lines.append("")
    return "\n".join(lines)


def refresh_roster() -> list:
    """Refresh the 40-man roster snapshot and return detected changes."""
    today = datetime.now().strftime("%Y-%m-%d")
    prev_file = find_prev_roster_file(today)
    prev = parse_existing_roster(prev_file)
    roster = fetch_40man_roster()
    if not roster:
        return []
    changes = detect_roster_changes(roster, prev)
    md = build_roster_markdown(roster, prev, today)
    ROSTER_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_ROSTER.write_text(md, encoding="utf-8")
    return changes


def translate_team_name(name: str) -> str:
    """Translate MLB team name to Chinese."""
    TEAM_NAMES = {
        "Arizona Diamondbacks": "响尾蛇",
        "Diamondbacks": "响尾蛇",
        "D-backs": "响尾蛇",
        "San Diego Padres": "教士",
        "Padres": "教士",
        "Los Angeles Dodgers": "道奇",
        "Dodgers": "道奇",
        "San Francisco Giants": "巨人",
        "Giants": "巨人",
        "Colorado Rockies": "洛矶",
        "Rockies": "洛矶",
        "New York Yankees": "洋基",
        "Yankees": "洋基",
        "New York Mets": "大都会",
        "Mets": "大都会",
        "Atlanta Braves": "勇士",
        "Braves": "勇士",
        "Philadelphia Phillies": "费城人",
        "Phillies": "费城人",
        "Chicago Cubs": "小熊",
        "Cubs": "小熊",
        "Milwaukee Brewers": "酿酒人",
        "Brewers": "酿酒人",
        "Cincinnati Reds": "红人",
        "Reds": "红人",
        "St. Louis Cardinals": "红雀",
        "Cardinals": "红雀",
        "Pittsburgh Pirates": "海盗",
        "Pirates": "海盗",
        "Washington Nationals": "国民",
        "Nationals": "国民",
        "Miami Marlins": "马林鱼",
        "Marlins": "马林鱼",
        "Houston Astros": "太空人",
        "Astros": "太空人",
        "Texas Rangers": "游骑兵",
        "Rangers": "游骑兵",
        "Seattle Mariners": "水手",
        "Mariners": "水手",
        "Oakland Athletics": "运动家",
        "Athletics": "运动家",
        "A's": "运动家",
        "Los Angeles Angels": "天使",
        "Angels": "天使",
    }
    return TEAM_NAMES.get(name, name)


def format_daily_report(data: dict) -> str:
    """Format JSON data into Chinese daily report"""
    if not data or not data.get("has_data"):
        return "⚾ 道奇队日报\n\n今日无比赛数据(休赛期或休息日)"

    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"⚾ 道奇队日报 - {today}", ""]

    # Yesterday's recap
    yesterday = data.get("yesterday", {})
    if yesterday.get("played"):
        lines.append("📊 昨晚赛果")
        lines.append("")
        # Translate team names in summary
        summary = yesterday.get("summary", "")
        summary = summary.replace("Los Angeles Dodgers", "道奇").replace("San Diego Padres", "教士").replace("Athletics", "运动家").replace("Philadelphia Phillies", "费城人")
        lines.append(summary)
        lines.append("")

        # Line score
        linescore = yesterday.get("linescore", "")
        if linescore:
            lines.append("逐局比分:")
            for line in linescore.strip().split("\n"):
                # Translate team names in line score
                line = line.replace("Dodgers", "道奇").replace("Padres", "教士").replace("Athletics", "运动家").replace("Phillies", "费城人")
                lines.append(f"  {line}")
            lines.append("")

        # Scoring plays - detailed Chinese format
        scoring = yesterday.get("scoring_plays", "")
        if scoring:
            lines.append("关键得分：")
            formatted_plays = parse_scoring_plays(scoring, team_name="Dodgers")
            for play in formatted_plays[:8]:  # Limit to 8 key moments
                if play.strip():
                    lines.append(f"• {play.strip()}")
            lines.append("")
    else:
        lines.append("📊 昨晚赛果")
        lines.append("昨晚无比赛")
        lines.append("")

    # Today's preview
    today_data = data.get("today", {})
    if today_data.get("scheduled"):
        lines.append("🔮 今日预告")
        lines.append("")

        opponent = today_data.get("opponent", "TBD")
        opponent_cn = translate_team_name(opponent)
        is_home = today_data.get("is_home", True)
        venue = today_data.get("venue", "TBD")

        if is_home:
            lines.append(f"道奇 vs {opponent_cn}")
        else:
            lines.append(f"道奇 @ {opponent_cn}")

        # Convert UTC to Beijing time (+8 hours)
        game_time = today_data.get("game_time", "")
        if game_time:
            try:
                dt = datetime.fromisoformat(game_time.replace("Z", "+00:00"))
                beijing_dt = dt + timedelta(hours=8)
                beijing_time = beijing_dt.strftime("%H:%M")
                lines.append(f"🕐 {beijing_time} (北京时间)")
            except:
                lines.append(f"🕐 {game_time}")

        lines.append(f"🏟️ {venue}")
        lines.append("")

        # Pitcher matchup
        pitcher_stats = data.get("pitcher_stats", {})
        away_pitcher = today_data.get("away_pitcher", "")
        home_pitcher = today_data.get("home_pitcher", "")

        if away_pitcher or home_pitcher:
            lines.append("先发投手:")
            if is_home and home_pitcher:
                stats = pitcher_stats.get(home_pitcher, {})
                era = stats.get("era", "N/A")
                w_l = f"{stats.get('wins', 0)}-{stats.get('losses', 0)}"
                lines.append(f"  道奇: {home_pitcher} ({w_l}, {era} ERA)")
            elif not is_home and away_pitcher:
                stats = pitcher_stats.get(away_pitcher, {})
                era = stats.get("era", "N/A")
                w_l = f"{stats.get('wins', 0)}-{stats.get('losses', 0)}"
                lines.append(f"  道奇: {away_pitcher} ({w_l}, {era} ERA)")
            lines.append("")
    else:
        lines.append("🔮 今日预告")
        lines.append("今日无比赛安排")
        lines.append("")

    # Injury report
    injuries = data.get("injuries", [])
    lines.append("🏥 伤病更新")
    if injuries:
        for injury in injuries:
            name = injury.get("name", "")
            pos = injury.get("position", "")
            desc = injury.get("description", "")
            status = injury.get("status", "")
            lines.append(f"• {name} ({pos}) - {desc} [{status}]")
    else:
        lines.append("✅ 无新增伤病")
    lines.append("")

    return "\n".join(lines)



def update_daily_file(report: str):
    """Update daily file with latest report (create or update game report section)"""
    today = datetime.now().strftime("%Y-%m-%d")
    daily_file = ROSTER_DIR / f"{today}.md"

    # Ensure directory exists
    ROSTER_DIR.mkdir(parents=True, exist_ok=True)

    # Use latest roster content as base so the 40-man snapshot is fresh
    if LATEST_ROSTER.exists():
        roster_content = LATEST_ROSTER.read_text(encoding="utf-8")
    else:
        roster_content = "# 道奇队阵容与日报\n\n"

    # Remove existing daily report section if exists
    if "\n---\n\n## 比赛日报" in roster_content:
        roster_content = roster_content.split("\n---\n\n## 比赛日报")[0].rstrip()

    # Write daily file: roster + daily report
    daily_file.write_text(roster_content + "\n\n---\n\n## 比赛日报\n\n" + report, encoding="utf-8")
    print(f"[SAVED] 日报已保存到: {daily_file}")


def update_roster_file(report: str):
    """Update dodgers-roster.md with latest daily report (replace, not append)"""
    # Ensure directory exists
    ROSTER_DIR.mkdir(parents=True, exist_ok=True)

    # Read current roster content
    if LATEST_ROSTER.exists():
        roster_content = LATEST_ROSTER.read_text(encoding="utf-8")
    else:
        roster_content = "# 道奇队阵容与日报\n\n"

    # Remove existing daily report section if exists
    if "\n---\n\n## 比赛日报" in roster_content:
        roster_content = roster_content.split("\n---\n\n## 比赛日报")[0].rstrip()

    # Write updated roster file
    LATEST_ROSTER.write_text(roster_content + "\n\n---\n\n## 比赛日报\n\n" + report, encoding="utf-8")
    print(f"[UPDATED] dodgers-roster.md 已更新")


def main():
    # Fix Windows console encoding
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # Refresh 40-man roster before generating the daily report
    changes = refresh_roster()
    data = fetch_daily_report()
    report = format_daily_report(data)
    report += format_roster_changes(changes)
    print(report)

    # Update daily file and roster file (replace mode)
    update_daily_file(report)
    update_roster_file(report)

    return report


if __name__ == "__main__":
    main()
