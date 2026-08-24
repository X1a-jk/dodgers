#!/usr/bin/env python3
"""
道奇队周报自动生成脚本
从 MLB API 抓取当周精确数据，生成红黑榜和 Markdown 报告
"""

import json
import urllib.request
import urllib.error
import ssl
from datetime import datetime, timedelta
from pathlib import Path
import re
import sys

# Add baseball skill to path for importing mlb_api
BASEBALL_SKILL_DIR = Path(r"C:\Users\Junkai XIA\.openclaw\workspace\skills\baseball\scripts")
if str(BASEBALL_SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(BASEBALL_SKILL_DIR))

try:
    from mlb_api import fetch_schedule, fetch_live_game
    HAS_BASEBALL_SKILL = True
except ImportError:
    HAS_BASEBALL_SKILL = False
    print("[WARN] baseball skill not available, falling back to basic schedule data")

TEAM_ID = 119
OUTPUT_DIR = Path(r"D:\baseball\weekly")
ROSTER_FILE = Path(r"D:\baseball\roster\dodgers-roster.md")

# SSL context for older systems
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE


def fetch_json(url: str, retries: int = 2) -> dict:
    """Fetch JSON from URL with simple retry for transient SSL/network errors."""
    last_error = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            last_error = e
            print(f"[WARN] API attempt {attempt + 1}/{retries + 1} failed: {url} -> {e}")
    print(f"[ERROR] API failed after {retries + 1} attempts: {url} -> {last_error}")
    return {}


def get_week_dates() -> dict:
    """Calculate date ranges for this week and last week"""
    today = datetime.now()
    monday = today - timedelta(days=(today.weekday() + 1) % 7 or 7)
    if today.weekday() == 0:
        monday = today
    sunday = monday + timedelta(days=6)
    prev_monday = monday - timedelta(days=7)
    prev_sunday = monday - timedelta(days=1)
    return {
        "monday": monday.strftime("%Y-%m-%d"),
        "sunday": sunday.strftime("%Y-%m-%d"),
        "prev_monday": prev_monday.strftime("%Y-%m-%d"),
        "prev_sunday": prev_sunday.strftime("%Y-%m-%d"),
        "monday_dt": monday,
        "next_monday": (monday + timedelta(days=7)).strftime("%Y-%m-%d"),
    }


def get_week_number(output_dir: Path) -> int:
    """Auto-increment week number based on existing valid reports.

    Ignores backup / wrong / temp files so a mis-named report cannot
    poison the next week's number.
    """
    current_year = datetime.now().year
    reports = sorted(
        p for p in output_dir.glob(f"{current_year}-*-week*.md")
        if re.search(r"week\d+\.md$", p.name, re.IGNORECASE)
    )
    if reports:
        latest = reports[-1].name
        match = re.search(r"week(\d+)", latest)
        if match:
            return int(match.group(1)) + 1
    return 1


def get_games(start: str, end: str, team_id: int) -> list:
    """Fetch schedule for date range"""
    url = f"https://statsapi.mlb.com/api/v1/schedule?teamId={team_id}&sportId=1&startDate={start}&endDate={end}"
    data = fetch_json(url)
    games = []
    for date_info in data.get("dates", []):
        for game in date_info.get("games", []):
            is_home = game["teams"]["home"]["team"]["id"] == team_id
            my_side = game["teams"]["home"] if is_home else game["teams"]["away"]
            opp_side = game["teams"]["away"] if is_home else game["teams"]["home"]
            status = game["status"]["codedGameState"]
            
            loc = "主场" if is_home else "客场"
            res_code = "-"
            res_display = "-"
            if status == "F":
                if my_side.get("isWinner"):
                    res_code = "W"
                    res_display = "✅ 胜"
                else:
                    res_code = "L"
                    res_display = "❌ 负"
            
            games.append({
                "date": date_info["date"],
                "time": (datetime.fromisoformat(game["gameDate"].replace("Z", "+00:00")) + timedelta(hours=8)).strftime("%H:%M"),
                "opponent": opp_side["team"]["name"],
                "location": loc,
                "score": f"{my_side['score']}-{opp_side['score']}" if status == "F" else "待赛",
                "result": res_display,
                "result_code": res_code,
            })
    return games


def get_game_details(game_pk: int) -> dict:
    """Fetch detailed box score using baseball skill's API client"""
    if not HAS_BASEBALL_SKILL:
        return {}
    try:
        data = fetch_live_game(game_pk)
        if not data:
            return {}
        
        # Extract line score
        linescore = data.get("liveData", {}).get("linescore", {})
        innings = linescore.get("innings", [])
        
        # Build line score text
        linescore_text = ""
        home_team = data.get("gameData", {}).get("teams", {}).get("home", {}).get("abbreviation", "HOME")
        away_team = data.get("gameData", {}).get("teams", {}).get("away", {}).get("abbreviation", "AWAY")
        
        # Get final score
        home_score = linescore.get("teams", {}).get("home", {}).get("runs", 0)
        away_score = linescore.get("teams", {}).get("away", {}).get("runs", 0)
        
        # Get scoring plays summary
        plays = data.get("liveData", {}).get("plays", {})
        scoring_plays = plays.get("scoringPlays", [])
        scoring_summary = []
        for sp in scoring_plays[:5]:  # Top 5 scoring plays
            play = plays.get("allPlays", [])[sp] if sp < len(plays.get("allPlays", [])) else None
            if play:
                desc = play.get("result", {}).get("description", "")
                scoring_summary.append(desc)
        
        return {
            "home_team": home_team,
            "away_team": away_team,
            "home_score": home_score,
            "away_score": away_score,
            "scoring_plays": scoring_summary,
            "has_details": True
        }
    except Exception as e:
        print(f"[WARN] Failed to fetch game details for {game_pk}: {e}")
        return {}


def get_player_stats(start: str, end: str, team_id: int, group: str) -> list:
    """Fetch player stats by date range"""
    url = f"https://statsapi.mlb.com/api/v1/stats?stats=byDateRange&group={group}&startDate={start}&endDate={end}&teamId={team_id}&playerPool=all"
    data = fetch_json(url)
    players = []
    for stat_group in data.get("stats", []):
        for split in stat_group.get("splits", []):
            s = split.get("stat", {})
            players.append({
                "name": split["player"]["fullName"],
                "id": split["player"]["id"],
                "pos": split["position"]["abbreviation"],
                "gp": s.get("gamesPlayed", 0),
                "avg": s.get("avg", ".000"),
                "obp": s.get("obp", ".000"),
                "slg": s.get("slg", ".000"),
                "ops": s.get("ops", ".000"),
                "hr": s.get("homeRuns", 0),
                "rbi": s.get("rbi", 0),
                "pa": s.get("plateAppearances", 0),
                "ab": s.get("atBats", 0),
                "h": s.get("hits", 0),
                "era": s.get("era"),
                "whip": s.get("whip"),
                "ip": s.get("inningsPitched"),
                "w": s.get("wins", 0),
                "sv": s.get("saves", 0),
                "so": s.get("strikeOuts", 0),
            })
    return players


def get_injured_players(roster_file: Path) -> list:
    """Parse injury list from roster markdown.

    Supports the current format which uses a single '## 伤病名单汇总' section
    with bullet entries like '- **IL-XX**: Player Name, Another Name'.
    """
    if not roster_file.exists():
        return []

    injured = []
    content = roster_file.read_text(encoding="utf-8")

    # Try new format: ## 伤病名单汇总
    section_match = re.search(
        r"##\s*伤病名单汇总\s*\n(.*?)(?=\n## |\Z)",
        content,
        re.DOTALL,
    )
    if section_match:
        section = section_match.group(1)
        for line in section.splitlines():
            line = line.strip()
            if not line.startswith("-") or line.startswith("---"):
                continue
            # Remove the leading bullet and bold IL label
            line = re.sub(r"^-\s*\*\*IL-\d+\*\*[:：]?\s*", "", line)
            # Split by comma / Chinese comma / semicolon
            names = re.split(r"[,，;；]", line)
            for name in names:
                name = name.strip().strip("*")
                # Remove parenthetical notes like (Neck inflammation)
                name = re.sub(r"\s*\(.*\)$", "", name)
                if name and not name.startswith("-"):
                    injured.append(name)
        return injured

    # Fallback to legacy per-section format
    for label in ("IL-60", "IL-15", "IL-10"):
        il_match = re.search(rf"###?\s*{label}.*?(?=###?\s*IL|\n## |\Z)", content, re.DOTALL)
        if il_match:
            injured.extend(re.findall(r"^- ([A-Za-z\s\.]+?) \(", il_match.group(), re.MULTILINE))

    return [name.strip() for name in injured if name.strip()]


def get_standings(team_id: int) -> tuple:
    """Fetch season record and division rank"""
    url = f"https://statsapi.mlb.com/api/v1/standings?leagueId=104&season={datetime.now().year}"
    data = fetch_json(url)
    for record in data.get("records", []):
        for team_rec in record.get("teamRecords", []):
            if team_rec["team"]["id"] == team_id:
                record_str = f"{team_rec['wins']}-{team_rec['losses']}"
                rank = team_rec.get("divisionRank", "N/A")
                return record_str, rank
    return "N/A", "N/A"


def safe_float(val, default=0.0):
    """Convert stat value to float, returning default for missing/dash values."""
    if val is None:
        return default
    try:
        if isinstance(val, str) and val.startswith("-."):
            return default
        return float(val)
    except (ValueError, TypeError):
        return default


def build_red_black(hitters: list, pitchers: list, injured: list) -> tuple:
    """Build red and black lists based on weekly performance with sample-size awareness."""

    def is_injured(name: str) -> bool:
        name_clean = name.lower().replace(".", " ").strip()
        for i in injured:
            i_clean = i.lower().replace(".", " ").strip()
            if name_clean == i_clean or name_clean in i_clean or i_clean in name_clean:
                return True
        return False

    active_hitters = [p for p in hitters if not is_injured(p["name"])]
    active_pitchers = [p for p in pitchers if not is_injured(p["name"])]

    # Hitters: require at least 10 PA and not a pitcher entry (use era presence to decide)
    qualified_hitters = [
        p for p in active_hitters
        if safe_float(p.get("pa")) >= 10 and p.get("era") is None
    ]

    # Pitchers: at least 1 IP to appear, and era present
    qualified_pitchers = [
        p for p in active_pitchers
        if safe_float(p.get("ip")) >= 1.0 and p.get("era") is not None
    ]

    # Red list: top 3 hitters by OPS + top 2 pitchers by ERA+WHIP (require IP >= 4 for red pitchers)
    red_hitters = sorted(
        qualified_hitters,
        key=lambda x: safe_float(x.get("ops")),
        reverse=True,
    )[:3]

    def pitcher_score(p):
        era = safe_float(p.get("era"), 99.0)
        whip = safe_float(p.get("whip"), 99.0)
        ip = safe_float(p.get("ip"), 0.0)
        # Prefer pitchers with more innings; penalize by ERA and WHIP
        return era + whip - (ip * 0.1)

    red_pitchers = sorted(
        [p for p in qualified_pitchers if safe_float(p.get("ip")) >= 4.0],
        key=pitcher_score,
    )[:2]

    # Black list: bottom hitters by OPS, but only regulars (PA >= 15)
    black_hitters = sorted(
        [p for p in qualified_hitters if safe_float(p.get("pa")) >= 15],
        key=lambda x: safe_float(x.get("ops")),
    )[:3]

    # Black list pitchers: bad ERA; require IP >= 3 for meaningful sample
    black_pitchers = sorted(
        [p for p in qualified_pitchers if safe_float(p.get("ip")) >= 3.0 and safe_float(p.get("era")) > 0],
        key=lambda x: safe_float(x.get("era"), 0.0),
        reverse=True,
    )[:2]

    red_list = red_hitters + red_pitchers
    black_list = black_hitters + black_pitchers
    return red_list, black_list


def _is_pitcher_entry(p: dict) -> bool:
    """Return True if this stat dict represents a pitcher."""
    return p.get("era") is not None


def _is_small_sample(p: dict) -> bool:
    """Mark small sample for display."""
    if _is_pitcher_entry(p):
        ip = safe_float(p.get("ip"))
        gp = int(safe_float(p.get("gp")))
        return ip < 3.0 or gp < 2
    return safe_float(p.get("pa")) < 15


def _hitter_comment(p: dict, is_red: bool) -> str:
    """Generate a data-driven comment for a hitter."""
    avg = safe_float(p.get("avg"))
    obp = safe_float(p.get("obp"))
    slg = safe_float(p.get("slg"))
    ops = safe_float(p.get("ops"))
    hr = int(safe_float(p.get("hr")))
    rbi = int(safe_float(p.get("rbi")))
    pa = int(safe_float(p.get("pa")))

    parts = []
    if is_red:
        if ops >= 1.0:
            parts.append(f"OPS {ops:.3f} 全队顶尖")
        elif ops >= 0.85:
            parts.append(f"OPS {ops:.3f} 状态稳定")
        if hr >= 2:
            parts.append(f"{hr} 轰，长打火力在线")
        elif slg >= 0.5:
            parts.append(f"长打率 {slg:.3f}，有额外垒打贡献")
        if rbi >= 5:
            parts.append(f"{rbi} 打点，关键串联贡献大")
        elif rbi >= 3:
            parts.append(f"{rbi} 打点，有一定串联输出")
        if obp - avg >= 0.08:
            parts.append(f"上垒率 {obp:.3f} 高于打击率，选球纪律好")
        elif obp - avg < 0.02 and avg >= 0.3:
            parts.append(f"打击率 {avg:.3f} 亮眼，但保送贡献有限")
        if slg - avg <= 0.15 and avg >= 0.3:
            parts.append("以 contact 为主，长打推力稍显不足")
    else:
        if ops <= 0.55:
            parts.append(f"OPS 仅 {ops:.3f}，进攻贡献极低")
        elif ops <= 0.7:
            parts.append(f"OPS {ops:.3f} 低于球队平均")
        if obp <= 0.25:
            parts.append(f"上垒率 {obp:.3f}，选球与打击同步低迷")
        elif obp - avg <= 0.04:
            parts.append(f"上垒率 {obp:.3f} 几乎靠打击率支撑，缺乏保送")
        if slg <= 0.3 and hr == 0:
            parts.append(f"长打率 {slg:.3f}，整周无长打")
        elif hr == 0:
            parts.append("整周无全垒打，长打火力断线")
        if rbi <= 1:
            parts.append(f"{rbi} 打点，串联效率不足")

    if pa < 15:
        parts.append(f"小样本（{pa} PA）")

    if not parts:
        return "当周表现平稳" if is_red else "当周表现低于预期"
    return "；".join(parts) + "。"


def _pitcher_comment(p: dict, is_red: bool) -> str:
    """Generate a data-driven comment for a pitcher."""
    era = safe_float(p.get("era"))
    whip = safe_float(p.get("whip"))
    ip = safe_float(p.get("ip"))
    w = int(safe_float(p.get("w")))
    so = int(safe_float(p.get("so")))
    gp = int(safe_float(p.get("gp")))

    # Heuristic role: starter if >= 4 IP in a week (usually one start)
    is_starter = ip >= 4.0 or gp <= 2

    parts = []
    if is_red:
        if era <= 1.0:
            parts.append(f"{ip} 局 ERA {era:.2f}，压制力顶级")
        elif era <= 3.0:
            parts.append(f"{ip} 局 ERA {era:.2f}，稳定优质")
        if whip <= 1.0:
            parts.append(f"WHIP {whip:.2f}，压制跑者效率出色")
        if w > 0:
            parts.append(f"拿下 {w} 胜")
        if so >= 8:
            parts.append(f"{so} 次三振，制造挥空能力强")
        if is_starter and ip >= 6.0:
            parts.append("至少撑过 6 局，减轻牛棚负担")
    else:
        if era >= 7.0:
            parts.append(f"{ip} 局 ERA {era:.2f}，失分控制糟糕")
        elif era >= 4.5:
            parts.append(f"{ip} 局 ERA {era:.2f}，表现低于预期")
        if whip >= 1.4:
            parts.append(f"WHIP {whip:.2f}，垒上危机偏多")
        if is_starter and ip < 6.0:
            parts.append(f"仅 {ip} 局退场，先发深度不足")
        if not is_starter:
            parts.append("中继/后援小样本，后续观察")

    if not parts:
        return "当周投球表现平稳" if is_red else "当周投球表现低于预期"

    # Add sample caveat for tiny reliever samples
    if not is_starter and ip < 3.0:
        parts.append(f"小样本（{ip} 局）")

    return "；".join(parts) + "。"


def format_report(dates: dict, last_games: list, this_games: list,
                  red_list: list, black_list: list,
                  season_record: str, division_rank: str,
                  injured: list, week_number: int) -> str:
    """Format the weekly report as Markdown"""
    wins = sum(1 for g in last_games if g["result_code"] == "W")
    losses = sum(1 for g in last_games if g["result_code"] == "L")
    
    # Game rows
    game_rows = ""
    for g in last_games:
        d = datetime.fromisoformat(g["date"]).strftime("%m/%d")
        prefix = "@" if g["location"] == "客场" else "vs"
        opp_display = f"{prefix} {g['opponent']}"
        game_rows += f"| {d} | {g['time']} | {opp_display} | {g['location']} | {g['score']} | {g['result']} |\n"
    
    # Schedule rows
    schedule_rows = ""
    for g in this_games:
        d = datetime.fromisoformat(g["date"]).strftime("%m/%d")
        schedule_rows += f"| {d} | {g['time']} | {g['opponent']} | {g['location']} | 待赛 |\n"
    
    # Red rows
    red_rows = ""
    for idx, p in enumerate(red_list):
        medal = ["🥇", "🥈", "🥉", "4", "5"][idx] if idx < 5 else str(idx + 1)
        sample_note = ""
        if _is_small_sample(p):
            sample_note = "*小样本* "
        if _is_pitcher_entry(p):
            stats = f"{p['ip']}IP, ERA {p['era']}, WHIP {p['whip']}, {int(safe_float(p['w']))}W"
            comment = sample_note + _pitcher_comment(p, True)
        else:
            stats = f"{p['avg']}/{p['obp']}/{p['slg']}, {int(safe_float(p['hr']))}HR, {int(safe_float(p['rbi']))}RBI"
            comment = sample_note + _hitter_comment(p, True)
        red_rows += f"| {medal} | **{p['name']}** | {p['pos']} | {stats} | {comment} |\n"
    
    # Black rows
    black_rows = ""
    for idx, p in enumerate(black_list):
        medal = ["🥇", "🥈", "🥉", "4", "5"][idx] if idx < 5 else str(idx + 1)
        sample_note = ""
        if _is_small_sample(p):
            sample_note = "*小样本* "
        if _is_pitcher_entry(p):
            stats = f"{p['ip']}IP, ERA {p['era']}, WHIP {p['whip']}, {int(safe_float(p['w']))}W"
            comment = sample_note + _pitcher_comment(p, False)
        else:
            stats = f"{p['avg']}/{p['obp']}/{p['slg']}, {int(safe_float(p['hr']))}HR, {int(safe_float(p['rbi']))}RBI"
            comment = sample_note + _hitter_comment(p, False)
        black_rows += f"| {medal} | **{p['name']}** | {p['pos']} | {stats} | {comment} |\n"
    
    # Injury table
    if injured:
        injury_text = "| 球员 | 状态 |\n|------|------|\n"
        for name in injured:
            injury_text += f"| {name} | 伤病名单 |\n"
        injury_text += "\n> 详情见 `D:\\baseball\\roster\\dodgers-roster.md`（按 IL-10 / IL-15 / IL-60 分类）。\n"
    else:
        injury_text = "无活跃伤病信息。"
    
    # Trend analysis from actual data
    rising = []
    falling = []
    watching = []
    
    if red_list:
        top_red = red_list[0]
        if _is_pitcher_entry(top_red):
            rising.append(f"**{top_red['name']}** 当周 {top_red['ip']} 局 ERA {top_red['era']}，投球压制力出色。")
        else:
            rising.append(f"**{top_red['name']}** 当周 OPS {top_red['ops']} 领跑全队，进攻状态火热。")
    
    if wins >= 5:
        rising.append(f"球队上周 {wins} 胜 {losses} 负，气势正旺。")
    elif losses >= 4:
        falling.append(f"球队上周仅 {wins} 胜 {losses} 负，整体状态需要调整。")
    
    if black_list:
        top_black = black_list[0]
        if _is_pitcher_entry(top_black):
            falling.append(f"**{top_black['name']}** 当周 ERA {top_black['era']} 偏高，投球状态下滑。")
        else:
            falling.append(f"**{top_black['name']}** 当周 OPS {top_black['ops']} 全队最低，进攻贡献不足。")
    
    if this_games:
        opp_names = [g['opponent'] for g in this_games]
        watching.append(f"本周对手：{', '.join(set(opp_names))}，客场连续作战考验投打续航。")
    
    # Key IL names to watch
    key_injured = [n for n in injured if any(x in n.lower() for x in ["smith", "glasnow", "díaz", "graterol"])]
    if key_injured:
        watching.append(f"伤病追踪：{', '.join(key_injured)} 仍在伤病名单，回归时程影响战力。")
    
    rising_text = "\n".join(f"- {x}" for x in rising) if rising else "- 暂无显著上升趋势。"
    falling_text = "\n".join(f"- {x}" for x in falling) if falling else "- 暂无显著下降趋势。"
    watching_text = "\n".join(f"- {x}" for x in watching) if watching else "- 常规观察中。"

    report = f"""# 道奇队每周战报 - Week {week_number}

> 更新时间: {dates['monday']} (Week {week_number})
> 数据截止: {dates['monday']}
> 下回更新: {dates['next_monday']} (每周一中午12:00自动更新)

---

## 一、上周战绩 ({dates['prev_monday']} ~ {dates['prev_sunday']})

| 项目 | 数据 |
|------|------|
| **上周战绩** | {wins}胜{losses}负 |
| **分区排名** | 国联西区第{division_rank}名 |
| **赛季总战绩** | {season_record} |

### 比赛记录

| 日期 | 时间 | 对手 | 场地 | 比分 | 结果 |
|------|------|------|------|------|------|
{game_rows}

---

## 二、本周赛程 ({dates['monday']} ~ {dates['sunday']})

| 日期 | 时间 | 对手 | 场地 | 状态 |
|------|------|------|------|------|
{schedule_rows}

---

## 三、本周红黑榜

> 原则：当红/当黑只看 **{dates['prev_monday']} ~ {dates['prev_sunday']} 当周表现**。伤病名单球员已排除；小样本球员单独标注。

### 🔥 红榜 (当周火热)

| 排名 | 球员 | 位置 | 当周数据 | 备注 |
|------|------|------|----------|------|
{red_rows}

### 🥶 黑榜 (当周冰冷)

| 排名 | 球员 | 位置 | 当周数据 | 备注 |
|------|------|------|----------|------|
{black_rows}

> 数据来源：MLB Stats API byDateRange（{dates['prev_monday']} ~ {dates['prev_sunday']}）。伤病名单球员已按 40 人名单快照排除；小样本球员已加注。

---

## 四、伤病名单

{injury_text}

---

## 五、趋势分析

### 上升
{rising_text}

### 下降
{falling_text}

### 关注
{watching_text}

---

*文件: {OUTPUT_DIR}\\{dates['monday']}-week{week_number}.md*
*数据来源: MLB Stats API + D:\\baseball\\roster\\dodgers-roster.md*
*更新方式: 每周一中午12:00自动更新*
"""
    return report


def main():
    print("========== 道奇队周报生成开始 ==========")
    
    dates = get_week_dates()
    week_number = get_week_number(OUTPUT_DIR)
    print(f"本周: Week {week_number} ({dates['prev_monday']} ~ {dates['prev_sunday']})")
    
    # Fetch data
    print("抓取上周赛程...")
    last_games = get_games(dates["prev_monday"], dates["prev_sunday"], TEAM_ID)
    print(f"上周比赛: {len(last_games)} 场")
    
    print("抓取本周赛程...")
    this_games = get_games(dates["monday"], dates["sunday"], TEAM_ID)
    print(f"本周比赛: {len(this_games)} 场")
    
    print("抓取打者数据...")
    hitters = get_player_stats(dates["prev_monday"], dates["prev_sunday"], TEAM_ID, "hitting")
    print(f"打者: {len(hitters)}")
    
    print("抓取投手数据...")
    pitchers = get_player_stats(dates["prev_monday"], dates["prev_sunday"], TEAM_ID, "pitching")
    print(f"投手: {len(pitchers)}")
    
    print("读取伤病名单...")
    injured = get_injured_players(ROSTER_FILE)
    print(f"伤病球员: {len(injured)}")
    
    print("抓取赛季战绩...")
    season_record, division_rank = get_standings(TEAM_ID)
    print(f"赛季战绩: {season_record}, 分区排名: {division_rank}")
    
    print("生成红黑榜...")
    red_list, black_list = build_red_black(hitters, pitchers, injured)
    print(f"红榜: {len(red_list)}, 黑榜: {len(black_list)}")
    
    print("生成报告...")
    report = format_report(dates, last_games, this_games, red_list, black_list,
                          season_record, division_rank, injured, week_number)
    
    # Write output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{dates['monday']}-week{week_number}.md"
    # If a mis-named report for this Monday already exists, back it up so the
    # correct week-numbered file can replace it.
    for stale in OUTPUT_DIR.glob(f"{dates['monday']}-week*.md"):
        if stale.name != output_path.name:
            backup = stale.with_suffix(".bak.md")
            stale.replace(backup)
            print(f"[BACKUP] 已备份错误命名报告: {backup}")
    output_path.write_text(report, encoding="utf-8")
    
    print(f"[SUCCESS] 报告已保存: {output_path}")
    print(f"OUTPUT_FILE: {output_path}")
    print("========== 道奇队周报生成完成 ==========")


if __name__ == "__main__":
    main()
