#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
季后赛模拟器：
1) 若赛季今天结束：国联 1-6 种子排布 + 道奇首轮对阵
2) 道奇与主要竞争者的剩余赛程难度（对手胜率加权）
3) 魔术数字 /  clinch / 淘汰状态
输出 D:\\baseball\\data\\playoff.json
"""
import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
BASE_DIR = Path(r"D:\baseball")
OUTPUT_FILE = BASE_DIR / "data" / "playoff.json"
SEASON = datetime.now().year
API = "https://statsapi.mlb.com/api/v1"
DODGERS_ID = 119


def api_get(path, params=None, retries=5, timeout=30, min_key=None):
    for i in range(retries):
        try:
            r = requests.get(API + path, params=params, timeout=timeout)
            r.raise_for_status()
            j = r.json()
            if min_key is None or j.get(min_key):
                return j
            print(f"  [warn] {path} 响应缺 {min_key}，重试 {i+1}/{retries}", flush=True)
        except Exception as e:
            print(f"  [retry {i+1}/{retries}] {path}: {type(e).__name__}", flush=True)
        time.sleep(2 * (i + 1))
    return {}


def main():
    today = datetime.now().strftime("%Y-%m-%d")

    # 1) 国联 standings
    st = api_get("/standings", {"leagueId": 104, "season": SEASON}, min_key="records")
    divisions = []
    all_teams = []
    for div in st.get("records", []):
        dname = div.get("division", {}).get("name", "?")
        rows = []
        for tr in div.get("teamRecords", []):
            team = tr.get("team") or {}
            rows.append({
                "id": team.get("id"), "name": team.get("name"), "abbr": (team.get("abbreviation") or team.get("name", "?"))[:3],
                "w": tr.get("wins"), "l": tr.get("losses"),
                "pct": float(tr.get("winningPercentage") or 0),
                "gb": tr.get("gamesBack"), "divRank": int(tr.get("divisionRank") or 9),
                "wcRank": int(tr.get("wildCardRank") or 9) if tr.get("wildCardRank") else None,
                "wcGb": tr.get("wildCardGamesBack"),
                "magic": tr.get("magicNumber"), "elim": tr.get("eliminationNumber"),
                "clinch": tr.get("clinchIndicator"),
            })
            all_teams.append(rows[-1])
        rows.sort(key=lambda x: x["divRank"])
        divisions.append({"name": dname, "teams": rows})

    # 2) 种子排布（赛季今天结束）
    div_winners = []
    for div in divisions:
        t = div["teams"][0]
        div_winners.append({**t, "division": div["name"]})
    div_winners.sort(key=lambda x: -x["pct"])
    for i, t in enumerate(div_winners):
        t["seed"] = i + 1

    wc_pool = [t for div in divisions for t in div["teams"] if t["divRank"] > 1]
    wc_pool.sort(key=lambda x: (-x["pct"], x["wcRank"] or 99))
    wildcards = []
    for i, t in enumerate(wc_pool[:3]):
        wildcards.append({**t, "seed": i + 4})

    bracket = sorted(div_winners + wildcards, key=lambda x: x["seed"])
    dodgers = next((t for t in bracket if t["id"] == DODGERS_ID), None)
    scenario = None
    if dodgers:
        seed = dodgers["seed"]
        if seed <= 2:
            scenario = f'轮空直入分区系列赛，等待外卡战胜者'
        elif seed == 3:
            opp = next((t for t in bracket if t["seed"] == 6), None)
            scenario = f'外卡轮 vs 6号种子 {opp["name"] if opp else "?"}（三战两胜）'
        elif seed == 4:
            opp = next((t for t in bracket if t["seed"] == 5), None)
            scenario = f'外卡轮 vs 5号种子 {opp["name"] if opp else "?"}（三战两胜，有主场优势）'
        else:
            opp = next((t for t in bracket if t["seed"] == 4), None)
            scenario = f'外卡轮客场 vs 4号种子 {opp["name"] if opp else "?"}（三战两胜）'

    # 3) 剩余赛程难度：道奇 + 国联前 8 竞争者
    pct_by_id = {t["id"]: t["pct"] for t in all_teams}
    name_by_id = {t["id"]: t["name"] for t in all_teams}
    contenders = sorted(all_teams, key=lambda x: -x["pct"])[:8]
    if not any(t["id"] == DODGERS_ID for t in contenders):
        contenders.append(dodgers)

    def remaining(team_id):
        j = api_get("/schedule", {"teamId": team_id, "sportId": 1,
                                  "startDate": today, "endDate": f"{SEASON}-10-06"}, min_key="dates")
        games = []
        for d in j.get("dates", []):
            for g in d.get("games", []):
                if g.get("status", {}).get("abstractGameState") == "Final":
                    continue
                home = g["teams"]["home"]["team"]["id"]
                opp = g["teams"]["away"]["team"]["id"] if home == team_id else home
                is_home = home == team_id
                if opp not in pct_by_id or opp == team_id:
                    continue
                games.append({"oppId": opp, "isHome": is_home, "date": g.get("gameDate", "")[:10]})
        return games

    strengths = []
    for t in contenders:
        if not t:
            continue
        gs = remaining(t["id"])
        if not gs:
            strengths.append({"id": t["id"], "name": t["name"], "gamesLeft": 0,
                              "oppWinPct": None, "home": 0, "away": 0})
            continue
        avg = sum(pct_by_id[g["oppId"]] for g in gs) / len(gs)
        strengths.append({
            "id": t["id"], "name": t["name"], "gamesLeft": len(gs),
            "oppWinPct": round(avg, 3),
            "home": sum(1 for g in gs if g["isHome"]),
            "away": sum(1 for g in gs if not g["isHome"]),
        })
        time.sleep(0.5)
    # 难度排名（对手胜率越高越难）
    ranked = sorted([s for s in strengths if s["oppWinPct"] is not None],
                    key=lambda x: -x["oppWinPct"])
    for i, s in enumerate(ranked):
        s["difficultyRank"] = i + 1

    data = {
        "generatedAt": datetime.now().isoformat(),
        "season": SEASON,
        "ifSeasonEndedToday": {
            "bracket": [{"seed": t["seed"], "name": t["name"], "abbr": t["abbr"],
                         "w": t["w"], "l": t["l"], "pct": t["pct"],
                         "isDodgers": t["id"] == DODGERS_ID,
                         "division": t.get("division")} for t in bracket],
            "dodgers": ({"seed": dodgers["seed"], "record": f'{dodgers["w"]}-{dodgers["l"]}',
                         "scenario": scenario} if dodgers else None),
        },
        "divisions": divisions,
        "remainingStrength": strengths,
    }
    if OUTPUT_FILE.exists():
        shutil.copy2(OUTPUT_FILE, OUTPUT_FILE.with_suffix(".json.bak"))
    OUTPUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] {OUTPUT_FILE}")
    for t in bracket:
        print(f'  #{t["seed"]} {t["name"]} {t["w"]}-{t["l"]} {"🏠" if t["id"] == DODGERS_ID else ""}')
    print(f'  道奇剧本: {scenario}')
    for s in strengths:
        print(f'  剩余难度: {s["name"]:<28} {s["gamesLeft"]}场 对手均胜率 {s["oppWinPct"]} 难度第{s.get("difficultyRank", "?")}')


if __name__ == "__main__":
    main()
