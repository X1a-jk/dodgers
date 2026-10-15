#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抓取道奇 40 人名单深度图数据，保存为静态 JSON。
由每日任务调用（与日报一起），门户只读取静态文件。

输出 D:\\baseball\\data\\depth-chart.json：
  - columns: 按守备位置的深度图列（捕手/一垒/.../指定打击）
  - starters / relievers: 投手分表
  - summary: 状态汇总
"""
import json
import re
import shutil
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from datetime import datetime
from pathlib import Path

import statsapi

TEAM_ID = 119
SEASON = datetime.now().year
BASE_DIR = Path(r"D:\baseball")
REPORT_DIR = BASE_DIR / "report"
OUTPUT_FILE = BASE_DIR / "data" / "depth-chart.json"

STATUS_MAP = {"A": "活跃", "RM": "小联盟", "D10": "IL-10", "D15": "IL-15", "D60": "IL-60"}
STATUS_RANK = {"活跃": 0, "IL-10": 1, "IL-15": 1, "IL-60": 2, "小联盟": 3}

# 守备位置 -> 深度图列。不在表内的归入 IF 工具人列。
POS_COLUMNS = [
    ("C", "捕手", "C"),
    ("1B", "一垒", "1B"),
    ("2B", "二垒", "2B"),
    ("3B", "三垒", "3B"),
    ("SS", "游击", "SS"),
    ("IF", "工具人", None),   # None = 兜底列（IF/UT 等）
    ("LF", "左外野", "LF"),
    ("CF", "中外野", "CF"),
    ("RF", "右外野", "RF"),
    ("DH", "指定打击", "DH"),
]


def run_with_timeout(func, timeout=25, default=None):
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


def slugify(name: str) -> str:
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_name = "".join(c for c in nfkd if not unicodedata.combining(c))
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    return slug


def fetch_roster() -> list:
    def _fetch():
        raw = statsapi.get(
            "team_roster",
            {"teamId": TEAM_ID, "rosterType": "40Man", "season": SEASON},
            request_kwargs={"timeout": 60},
        )
        players = []
        for team_entry in raw.get("roster", []):
            person = team_entry.get("person", {})
            pos = team_entry.get("position", {})
            status = team_entry.get("status", {})
            code = status.get("code", "?")
            players.append({
                "id": person.get("id"),
                "name": person.get("fullName", "?"),
                "pos": pos.get("abbreviation", "?"),
                "jersey": team_entry.get("jerseyNumber", ""),
                "statusCode": code,
                "status": STATUS_MAP.get(code, status.get("description", code)),
            })
        return players
    return run_with_timeout(_fetch, timeout=30, default=[])


def fetch_group_stats(group: str) -> dict:
    """group: 'hitting' | 'pitching'。返回 {playerId: stat}。"""
    def _fetch():
        raw = statsapi.get(
            "stats",
            {
                "stats": "season",
                "group": group,
                "playerPool": "ALL",
                "teamId": TEAM_ID,
                "season": SEASON,
                "limit": 200,
            },
            request_kwargs={"timeout": 60},
        )
        out = {}
        for st in raw.get("stats", []):
            for split in st.get("splits", []):
                pid = split.get("player", {}).get("id")
                if pid:
                    out[pid] = split.get("stat", {})
        return out
    result = run_with_timeout(_fetch, timeout=45, default={})
    return result or {}


def pick(stats: dict, *keys):
    for k in keys:
        if k in stats and stats[k] is not None:
            return stats[k]
    return None


def build_player(p: dict, hitting: dict, pitching: dict) -> dict:
    slug = slugify(p["name"])
    report_rel = f"report/{slug}/{slug}-scouting-report.html"
    headshot_rel = f"report/{slug}/headshot.jpg"
    player = {
        "id": p["id"],
        "name": p["name"],
        "pos": p["pos"],
        "jersey": p["jersey"],
        "statusCode": p["statusCode"],
        "status": p["status"],
        "reportUrl": report_rel if (BASE_DIR / report_rel).exists() else None,
        "headshot": headshot_rel if (BASE_DIR / headshot_rel).exists() else None,
    }
    h = hitting.get(p["id"])
    pt = pitching.get(p["id"])
    if h:
        player["bat"] = {
            "g": pick(h, "gamesPlayed"),
            "avg": pick(h, "avg"),
            "obp": pick(h, "obp"),
            "slg": pick(h, "slg"),
            "ops": pick(h, "ops"),
            "hr": pick(h, "homeRuns"),
            "rbi": pick(h, "rbi"),
            "sb": pick(h, "stolenBases"),
        }
    if pt:
        player["pitch"] = {
            "g": pick(pt, "gamesPlayed"),
            "gs": pick(pt, "gamesStarted"),
            "w": pick(pt, "wins"),
            "l": pick(pt, "losses"),
            "era": pick(pt, "era"),
            "whip": pick(pt, "whip"),
            "so": pick(pt, "strikeOuts"),
            "ip": pick(pt, "inningsPitched"),
        }
    return player


def sort_key(player: dict):
    games = 0
    if "bat" in player and player["bat"].get("g"):
        games = int(player["bat"]["g"])
    elif "pitch" in player and player["pitch"].get("g"):
        games = int(player["pitch"]["g"])
    return (STATUS_RANK.get(player["status"], 9), -games, player["name"])


def main():
    print("[INFO] Fetching 40-man roster for depth chart...")
    roster = fetch_roster()
    if not roster:
        print("[ERR] Roster fetch failed; keeping previous data if any.")
        sys.exit(1)
    print(f"[INFO] Roster: {len(roster)} players")

    print("[INFO] Fetching season stats (hitting + pitching)...")
    hitting = fetch_group_stats("hitting")
    pitching = fetch_group_stats("pitching")
    print(f"[INFO] Stats: {len(hitting)} hitters, {len(pitching)} pitchers")

    players = {p["id"]: build_player(p, hitting, pitching) for p in roster}

    # ---- 分列 ----
    columns = []
    for key, label, wanted in POS_COLUMNS:
        cols_players = []
        for p in roster:
            pl = players[p["id"]]
            pos = "DH" if p["pos"] == "TWP" else p["pos"]  # 二刀流归入 DH 列
            if wanted is not None:
                if pos != wanted and not (wanted == "CF" and pos == "OF"):
                    continue
            else:
                # 兜底列：IF/UT 等内野通算，或没匹配上任何列的野手
                known = {"C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "OF", "DH", "P"}
                if pos in known:
                    continue
            cols_players.append(pl)
        cols_players.sort(key=sort_key)
        columns.append({"key": key, "label": label, "players": cols_players})

    # ---- 投手分表 ----
    starters, relievers = [], []
    for p in roster:
        pl = players[p["id"]]
        pos = p["pos"]
        pt = pl.get("pitch")
        if pos == "P" or (pt and pt.get("gs") and int(pt["gs"]) >= 3):
            gs = int(pt.get("gs") or 0) if pt else 0
            g = int(pt.get("g") or 0) if pt else 0
            if gs > g - gs:
                starters.append(pl)
            else:
                relievers.append(pl)
    starters.sort(key=lambda x: (-(int(x.get("pitch", {}).get("gs") or 0)), sort_key(x)))
    relievers.sort(key=lambda x: (-(int(x.get("pitch", {}).get("g") or 0)), sort_key(x)))

    # 二刀流：大谷同时进 DH 列和先发列（若满足先发条件已在上面的 P 判断里，
    # 但 roster 位置是 TWP 时需显式补进先发）
    for p in roster:
        if p["pos"] == "TWP":
            pl = players[p["id"]]
            pt = pl.get("pitch") or {}
            if int(pt.get("gs") or 0) >= 3 and pl not in starters:
                starters.append(pl)
            pl["twoWay"] = True

    summary = {"active": 0, "il": 0, "minors": 0}
    for p in roster:
        s = p["status"]
        if s == "活跃":
            summary["active"] += 1
        elif s.startswith("IL"):
            summary["il"] += 1
        else:
            summary["minors"] += 1

    data = {
        "generatedAt": datetime.now().isoformat(),
        "season": SEASON,
        "summary": summary,
        "columns": columns,
        "starters": starters,
        "relievers": relievers,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUTPUT_FILE.with_suffix(".tmp")
    if OUTPUT_FILE.exists():
        shutil.copy2(OUTPUT_FILE, OUTPUT_FILE.with_suffix(".json.bak"))
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(OUTPUT_FILE)
    print(f"[OK] Saved {OUTPUT_FILE}")
    print(f"     Starters: {len(starters)} | Relievers: {len(relievers)} | "
          f"Active: {summary['active']} IL: {summary['il']} Minors: {summary['minors']}")
    sys.exit(0)


if __name__ == "__main__":
    main()
