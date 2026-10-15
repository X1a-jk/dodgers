#!/usr/bin/env python3
"""
抓取道奇队赛程与比赛中心所需数据，保存为静态 JSON。
由每日任务调用（与日报一起），门户启动时只读取静态文件。
"""
import json
import re
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from datetime import datetime, timedelta
from pathlib import Path

import statsapi

TEAM_ID = 119
TEAM_NAME = "Los Angeles Dodgers"
SEASON = datetime.now().year
BASE_DIR = Path(r"D:\baseball")
OUTPUT_FILE = BASE_DIR / "data" / "schedule-game-hub.json"


def run_with_timeout(func, timeout=15, default=None):
    """Run a function with a timeout. Return default on timeout or error."""
    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func)
            return future.result(timeout=timeout)
    except TimeoutError:
        print(f"[WARN] Operation timed out after {timeout}s")
        return default
    except Exception as e:
        print(f"[WARN] Operation failed: {e}")
        return default


def safe_get(func, default=None):
    try:
        return func()
    except Exception as e:
        print(f"[WARN] {e}")
        return default


def team_abbrev(full_name: str) -> str:
    mapping = {
        "Arizona Diamondbacks": "ARI", "Atlanta Braves": "ATL",
        "Baltimore Orioles": "BAL", "Boston Red Sox": "BOS",
        "Chicago Cubs": "CHC", "Chicago White Sox": "CWS",
        "Cincinnati Reds": "CIN", "Cleveland Guardians": "CLE",
        "Colorado Rockies": "COL", "Detroit Tigers": "DET",
        "Houston Astros": "HOU", "Kansas City Royals": "KC",
        "Los Angeles Angels": "LAA", "Los Angeles Dodgers": "LAD",
        "Miami Marlins": "MIA", "Milwaukee Brewers": "MIL",
        "Minnesota Twins": "MIN", "New York Mets": "NYM",
        "New York Yankees": "NYY", "Oakland Athletics": "OAK",
        "Philadelphia Phillies": "PHI", "Pittsburgh Pirates": "PIT",
        "San Diego Padres": "SD", "San Francisco Giants": "SF",
        "Seattle Mariners": "SEA", "St. Louis Cardinals": "STL",
        "Tampa Bay Rays": "TB", "Texas Rangers": "TEX",
        "Toronto Blue Jays": "TOR", "Washington Nationals": "WSH",
    }
    return mapping.get(full_name, "".join(w[0] for w in full_name.split() if w)[:3].upper())


def beijing_time(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        bj = dt + timedelta(hours=8)
        return bj.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return iso_str


def fetch_games(start: str, end: str) -> list:
    """Fetch games for a date range with linescore/probable pitcher hydrate."""
    raw = statsapi.get(
        "schedule",
        {
            "teamId": TEAM_ID,
            "sportId": 1,
            "startDate": start,
            "endDate": end,
            "hydrate": "probablePitcher",
        },
        request_kwargs={"timeout": 60},
    )
    games = []
    for d in raw.get("dates", []):
        for g in d.get("games", []):
            is_home = g["teams"]["home"]["team"]["id"] == TEAM_ID
            my_side = g["teams"]["home"] if is_home else g["teams"]["away"]
            opp_side = g["teams"]["away"] if is_home else g["teams"]["home"]
            status = g.get("status", {})
            abstract = status.get("abstractGameState", "Scheduled")
            detailed = status.get("detailedState", "Scheduled")

            res = None
            if abstract == "Final":
                if my_side.get("isWinner"):
                    res = "W"
                else:
                    res = "L"

            game_info = {
                "gamePk": g.get("gamePk"),
                "date": d["date"],
                "utcTime": g.get("gameDate", ""),
                "beijingTime": beijing_time(g.get("gameDate", "")),
                "status": abstract,
                "detailedStatus": detailed,
                "isHome": is_home,
                "opponent": {
                    "id": opp_side["team"]["id"],
                    "name": opp_side["team"]["name"],
                    "abbreviation": team_abbrev(opp_side["team"]["name"]),
                },
                "venue": g.get("venue", {}).get("name", ""),
                "score": {
                    "dodgers": my_side.get("score", 0),
                    "opponent": opp_side.get("score", 0),
                } if abstract == "Final" else None,
                "result": res,
                "probablePitcher": my_side.get("probablePitcher", {}).get("fullName"),
                "opponentProbablePitcher": opp_side.get("probablePitcher", {}).get("fullName"),
            }
            games.append(game_info)
    return games


def fetch_pitcher_stats(name: str) -> dict:
    if not name or name == "TBD":
        return None

    def _fetch():
        search = statsapi.lookup_player(name)
        if not search:
            return None
        pid = search[0]["id"]
        data = statsapi.player_stat_data(pid, group="pitching", type="season")
        if data and data.get("stats"):
            for s in data["stats"]:
                if s.get("stats"):
                    st = s["stats"]
                    return {
                        "name": name,
                        "w": st.get("wins", 0),
                        "l": st.get("losses", 0),
                        "era": st.get("era", "-"),
                        "whip": st.get("whip", "-"),
                    }
        return None

    return run_with_timeout(_fetch, timeout=15, default=None)


def fetch_last_game_details(game_pk: int) -> dict:
    def _fetch():
        linescore = statsapi.linescore(game_pk)
        scoring = safe_get(lambda: statsapi.game_scoring_plays(game_pk), "")
        return {"linescore": linescore, "scoringPlays": scoring}

    return run_with_timeout(_fetch, timeout=30, default={})


HR_WORDS = {1: "阳春炮", 2: "两分炮", 3: "三分炮", 4: "四分炮"}
RUN_WORDS = {1: "1分", 2: "2分", 3: "3分", 4: "4分"}

SCORE_LINE_RE = re.compile(
    r"^(Top|Bottom)\s+(\d+)\s+-\s+(.+?):\s*(\d+)\s*,\s*(.+?):\s*(\d+)\s*$"
)


def _describe_play(desc: str, runs: int) -> str:
    """把英文得分描述压缩成中文短语，如 'Freeman 两分炮'。"""
    first = desc.split(". ")[0]
    # "X out on a sacrifice fly" → X 牺牲飞球
    m = re.match(r"^(.+?) out on a (sacrifice fly|sacrifice bunt)", first)
    if m:
        actor, kind = m.groups()
        action = "牺牲飞球" if kind == "sacrifice fly" else "牺牲触击"
        return f"{actor} {action}打回{RUN_WORDS.get(runs, str(runs) + '分')}"
    m = re.match(
        r"^(.+?)\s+(homers?|triples?|doubles?|singles?|sacrifice fly|"
        r"sacrifice bunt|walks?|hit by pitch|reaches on a fielder's choice|"
        r"reaches on an error|error by|grounds out|flies out|lines out|pops out)\b",
        first,
    )
    if not m:
        return first[:36] + ("..." if len(first) > 36 else "")
    actor, verb = m.groups()
    if verb.startswith("homer"):
        return f"{actor} {HR_WORDS.get(runs, str(runs) + '分炮')}"
    out_actions = {"grounds out": "滚地球", "flies out": "飞球", "lines out": "平飞球", "pops out": "内野飞球"}
    if verb in out_actions:
        return f"{actor} {out_actions[verb]}出局打回{RUN_WORDS.get(runs, str(runs) + '分')}"
    action = {
        "triples": "三垒安打", "doubles": "二垒安打", "singles": "安打",
        "sacrifice fly": "牺牲飞球", "sacrifice bunt": "牺牲触击",
        "walks": "保送", "hit by pitch": "触身球",
        "reaches on a fielder's choice": "野手选择",
        "reaches on an error": "对手失误", "error by": "对手失误",
    }.get(verb, verb)
    return f"{actor} {action}打回{RUN_WORDS.get(runs, str(runs) + '分')}"


def extract_key_moments(scoring_text: str, is_home: bool, max_moments: int = 8) -> list:
    """把 statsapi 的得分打席文本解析成紧凑的中文一句话时刻。

    原文是 '描述 + Top/Bottom N - 客队: a, 主队: b' 交替的多行文本，
    直接展示既啰嗦又是英文。这里解析成 '1局下 · Freeman 两分炮 · 3-0' 这种格式。
    """
    if not scoring_text:
        return []
    lines = [l.strip() for l in scoring_text.strip().split("\n") if l.strip()]

    # 先按比分行把描述分组
    plays = []
    pending = []
    for line in lines:
        m = SCORE_LINE_RE.match(line)
        if m:
            half, inn, _away_name, away_s, _home_name, home_s = m.groups()
            plays.append({
                "desc": " ".join(pending),
                "half": half,
                "inning": int(inn),
                "away": int(away_s),
                "home": int(home_s),
            })
            pending = []
        else:
            pending.append(line)

    moments = []
    prev_d = prev_o = 0
    for p in plays:
        d_score = p["home"] if is_home else p["away"]
        o_score = p["away"] if is_home else p["home"]
        d_delta, o_delta = d_score - prev_d, o_score - prev_o
        prev_d, prev_o = d_score, o_score
        runs = d_delta + o_delta
        if runs <= 0 or not p["desc"]:
            continue
        inning_cn = f"{p['inning']}局{'下' if p['half'] == 'Bottom' else '上'}"
        who = "dodgers" if d_delta > 0 else "opponent"
        moments.append({
            "inning": inning_cn,
            "team": who,
            "text": _describe_play(p["desc"], runs),
            "score": f"{d_score}-{o_score}",
        })

    # 得分打席太多时保留最后 max_moments 个（比赛后期的关键分更决定性）
    if len(moments) > max_moments:
        moments = moments[-max_moments:]
    return moments


def series_games(games: list, today_str: str) -> dict:
    """Build the CURRENT series summary.

    选择优先级（全部按北京时间判断，与抓取时点一致）：
    1. 有比赛正在进行/待开赛的系列（比赛日抓取锁定当前系列）
    2. 今天（北京时间）刚打完比赛的系列（系列收官战打完的当天不翻篇）
    3. 北京时间范围覆盖今天的系列（如系列赛首场今晚开打）
    4. 休息日：最近刚有完赛的系列
    5. 全部未赛：取最近的未来系列
    """
    sorted_games = sorted(games, key=lambda x: x["date"])
    groups = []
    for g in sorted_games:
        if groups and groups[-1]["opponent_id"] == g["opponent"]["id"]:
            groups[-1]["games"].append(g)
        else:
            groups.append({
                "opponent_id": g["opponent"]["id"],
                "opponent": g["opponent"]["name"],
                "opponent_abbreviation": g["opponent"]["abbreviation"],
                "games": [g],
            })
    if not groups:
        return None

    today = datetime.strptime(today_str, "%Y-%m-%d").date()

    LIVE_STATES = {"Live", "In Progress", "Warmup", "Pre-Game", "Delayed", "Delayed Start"}

    def bj_date(g):
        """比赛开始日的北京时间日期（beijingTime 格式 'YYYY-MM-DD HH:MM'）。"""
        bt = (g.get("beijingTime") or "")[:10]
        try:
            return datetime.strptime(bt, "%Y-%m-%d").date()
        except ValueError:
            return datetime.strptime(g["date"], "%Y-%m-%d").date()

    def is_live(g):
        st = (g.get("status") or "")
        return st in LIVE_STATES or st.startswith("Delayed")

    def is_final(g):
        return g.get("status") == "Final"

    chosen = None
    for grp in groups:
        if any(is_live(g) for g in grp["games"]):
            chosen = grp
            break
    if chosen is None:
        for grp in groups:
            if any(is_final(g) and bj_date(g) == today for g in grp["games"]):
                chosen = grp
                break
    if chosen is None:
        for grp in groups:
            dates = [bj_date(g) for g in grp["games"]]
            if min(dates) <= today <= max(dates):
                chosen = grp
                break
    if chosen is None:
        best = None
        for grp in groups:
            finals = [bj_date(g) for g in grp["games"] if is_final(g)]
            if not finals:
                continue
            last_final = max(finals)
            if best is None or last_final > best[0]:
                best = (last_final, grp)
        if best:
            chosen = best[1]
    if chosen is None:
        best_key = None
        for grp in groups:
            dates = [bj_date(g) for g in grp["games"]]
            dist = min(abs((d - today).days) for d in dates)
            if best_key is None or dist < best_key:
                best_key = dist
                chosen = grp

    played = [g for g in chosen["games"] if g["status"] == "Final"]
    wins = sum(1 for g in played if g["result"] == "W")
    losses = len(played) - wins
    next_game = next((g for g in chosen["games"] if g["status"] != "Final"), None)

    return {
        "opponent": chosen["opponent"],
        "opponentAbbreviation": chosen["opponent_abbreviation"],
        "totalGames": len(chosen["games"]),
        "gamesPlayed": len(played),
        "wins": wins,
        "losses": losses,
        "nextGameDate": next_game["date"] if next_game else None,
        "nextGameBeijingTime": next_game.get("beijingTime") if next_game else None,
        "games": [
            {
                "date": g["date"],
                "status": g["status"],
                "result": g["result"],
                "score": g.get("score"),
                "isHome": g["isHome"],
            }
            for g in chosen["games"]
        ],
    }


def build_calendar(games: list) -> dict:
    today = datetime.now()
    return {
        "year": today.year,
        "month": today.month,
        "games": [
            {
                "date": g["date"],
                "day": int(g["date"].split("-")[2]),
                "opponent": g["opponent"]["abbreviation"],
                "opponentName": g["opponent"]["name"],
                "isHome": g["isHome"],
                "result": g["result"],
                "status": g["status"],
                "score": g.get("score"),
            }
            for g in sorted(games, key=lambda x: x["date"])
            if g["date"].startswith(f"{today.year}-{today.month:02d}")
        ],
    }


def atomic_write(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    if path.exists():
        shutil.copy2(path, path.with_suffix(".json.bak"))
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def main():
    print("[INFO] Fetching schedule & game hub data...")
    today = datetime.now()
    past_start = (today - timedelta(days=21)).strftime("%Y-%m-%d")
    future_end = (today + timedelta(days=14)).strftime("%Y-%m-%d")
    today_str = today.strftime("%Y-%m-%d")

    games = fetch_games(past_start, future_end)
    print(f"[INFO] Fetched {len(games)} games ({past_start} ~ {future_end})")

    # Upcoming: next scheduled game
    upcoming = [g for g in games if g["status"] != "Final"]
    next_game = upcoming[0] if upcoming else None

    # Last final game
    past = [g for g in games if g["status"] == "Final"]
    last_game = past[-1] if past else None

    if next_game:
        next_game["pitcherStats"] = safe_get(
            lambda: fetch_pitcher_stats(next_game["probablePitcher"]), None
        )
        next_game["opponentPitcherStats"] = safe_get(
            lambda: fetch_pitcher_stats(next_game["opponentProbablePitcher"]), None
        )
        next_game.pop("countdown", None)

    if last_game:
        details = safe_get(lambda: fetch_last_game_details(last_game["gamePk"]), {})
        last_game["linescore"] = details.get("linescore")
        last_game["keyMoments"] = extract_key_moments(
            details.get("scoringPlays", ""), last_game["isHome"]
        )

    data = {
        "generatedAt": datetime.now().isoformat(),
        "season": SEASON,
        "team": {"id": TEAM_ID, "name": TEAM_NAME, "abbreviation": "LAD"},
        "calendar": build_calendar(games),
        "nextGame": next_game,
        "lastGame": last_game,
        "series": series_games(games, today_str),
        "recentAndUpcoming": [
            {k: v for k, v in g.items() if k not in ("boxscore", "linescore", "keyMoments")}
            for g in sorted(games, key=lambda x: x["date"])
        ],
    }

    atomic_write(OUTPUT_FILE, data)
    print(f"[OK] Saved {OUTPUT_FILE}")
    print(f"     Games: {len(games)} | Next: {next_game['date'] if next_game else 'none'} | Last: {last_game['date'] if last_game else 'none'}")
    sys.exit(0)


if __name__ == "__main__":
    main()
