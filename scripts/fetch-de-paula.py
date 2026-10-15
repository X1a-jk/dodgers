#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抓 Josue De Paula (800543) 小联盟数据 — 直连无代理"""
import json
import time
import requests
from pathlib import Path

PID = 800543
API = "https://statsapi.mlb.com/api/v1"
OUT = Path(r"D:\baseball\data\de-paula-raw.json")
# 本机直连超时，必须走系统代理（实测：direct 11s 超时，proxy 2.6s 200）
NO_PROXY = None

def get(path, params=None, retries=4, timeout=30):
    for i in range(retries):
        try:
            r = requests.get(API + path, params=params, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"  [retry {i+1}] {path}: {type(e).__name__}", flush=True)
            time.sleep(1.5 * (i + 1))
    return {}

# info
data = {"info": get(f"/people/{PID}").get("people", [{}])[0]}

# 逐附属球队查他的赛季数据（Tulsa 260/12 今年；Great Lakes 456/13 去年；Ogden/Rancho 等历史）
TEAM_QUERIES = [
    (2026, 260, 12), (2026, 238, 11),  # 今年 Tulsa + Oklahoma City
    (2025, 456, 13), (2025, 260, 12),  # 去年 Great Lakes / Tulsa
    (2024, 456, 13), (2024, 238, 11),  # 前年
    (2023, 678, 16), (2023, 541, 16),  # ACL Dodgers / DSL 尝试
]
data["season_stats"] = []
for yr, tid, sid in TEAM_QUERIES:
    for grp in ["hitting", "fielding"]:
        j = get("/stats", {"stats": "season", "group": grp, "teamId": tid,
                           "sportId": sid, "season": yr, "limit": 200})
        for st in j.get("stats", []):
            for sp in st.get("splits", []):
                if (sp.get("player") or {}).get("id") == PID:
                    data["season_stats"].append({
                        "year": yr, "group": grp,
                        "team": (sp.get("team") or {}).get("name"),
                        "league": st.get("league", {}).get("name"),
                        "stat": sp["stat"],
                    })

# 2026 逐场：Tulsa 赛程 + boxscore 解析他的打席
from datetime import datetime, timedelta
today = datetime.now().date()
start = (today - timedelta(days=60)).strftime("%Y-%m-%d")
end = today.strftime("%Y-%m-%d")
sched = get("/schedule", {"teamId": 260, "sportId": 12, "startDate": start, "endDate": end})
games = []
for d in sched.get("dates", []):
    for g in d.get("games", []):
        if g.get("status", {}).get("abstractGameState") == "Final":
            games.append((d.get("date"), g.get("gamePk")))

gamelog = []
for date, pk in games:
    box = get(f"/game/{pk}/boxscore", timeout=30)
    for side in ("home", "away"):
        team = box.get("teams", {}).get(side, {})
        if team.get("team", {}).get("id") != 260:
            continue
        p = team.get("players", {}).get(f"ID{PID}")
        if not p:
            continue
        b = p.get("stats", {}).get("batting") or {}
        opp = box.get("teams", {}).get("away" if side == "home" else "home", {}).get("team", {}).get("name", "?")
        gamelog.append({
            "date": date, "opponent": opp, "isHome": side == "home",
            "ab": b.get("atBats", 0), "r": b.get("runs", 0), "h": b.get("hits", 0),
            "dbl": b.get("doubles", 0), "tpl": b.get("triples", 0), "hr": b.get("homeRuns", 0),
            "rbi": b.get("rbi", 0), "bb": b.get("baseOnBalls", 0), "so": b.get("strikeOuts", 0),
            "sb": b.get("stolenBases", 0), "avg": b.get("avg", "-"),
        })
data["gamelog_2026"] = gamelog

# transactions
data["transactions"] = get("/transactions", {"playerId": PID, "startDate": "2026-01-01", "endDate": end}).get("transactions", [])

OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("[OK]", OUT)
print("season splits:")
for x in data["season_stats"]:
    if x["group"] == "hitting":
        s = x["stat"]
        print(f"  {x['year']} {x['team']}: G{s.get('gamesPlayed')} PA{s.get('plateAppearances')} "
              f"{s.get('avg')}/{s.get('obp')}/{s.get('slg')} OPS {s.get('ops')} HR{s.get('homeRuns')} SB{s.get('stolenBases')} "
              f"BB{s.get('baseOnBalls')} SO{s.get('strikeOuts')}")
print("gamelog games:", len(gamelog))
if gamelog:
    recent = gamelog[-10:]
    print("最近10场:", [(g['date'][5:], g['h'], g['hr'], g['rbi'], g['so']) for g in recent])
