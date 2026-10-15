#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对手情报局：下一场对手近期战绩 / 关键打者 / 投手群 / 对战历史 / 球场信息。
读 schedule-game-hub.json 拿对手，输出 D:\\baseball\\data\\opponent.json。
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
HUB_FILE = BASE_DIR / "data" / "schedule-game-hub.json"
OUTPUT_FILE = BASE_DIR / "data" / "opponent.json"
SEASON = datetime.now().year
API = "https://statsapi.mlb.com/api/v1"

# 常见球场风格备注（人工整理，用于情报卡）
PARK_NOTES = {
    "loanDepot park": "投手友好型球场，长打不易，外野空间偏大",
    "Coors Field": "全联盟最极端打者球场，球飞行距离明显加成，落点判断困难",
    "Dodger Stadium": "投手略友好，傍晚海风向内吹，全垒打墙偏高",
    "Yankee Stadium": "右外野短 porch，左打拉打吃香",
    "Fenway Park": "绿色怪物墙，右打二垒打变相加成",
    "Oracle Park": "极端投手球场，右外野大且风冷",
    "Petco Park": "中性偏投手，海雾夜场影响飞行",
    "Chase Field": "炎热干燥，球飞行好；新人工草皮弹跳快",
    "American Family Field": "可开合屋顶，夏季闷热球飞",
    "Great American Ball Park": "打者友好，右外野墙低",
    "Citizens Bank Park": "打者友好，夏季热流助推",
    "Truist Park": "轻微打者友好",
    "Daikin Park": "空调穹顶，环境稳定",
    "George M. Steinbrenner Field": "春训球场改主场，外野偏小",
    "Sutter Health Park": "小联盟球场，外野墙不规则，打者友好",
}


def api_get(path, params=None, retries=4, timeout=30):
    for i in range(retries):
        try:
            r = requests.get(API + path, params=params, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"  [retry {i+1}/{retries}] {path}: {type(e).__name__}", flush=True)
            time.sleep(1.5 * (i + 1))
    return {}


def team_games(team_id, start, end, sport_id=1):
    j = api_get("/schedule", {
        "teamId": team_id, "sportId": sport_id,
        "startDate": start, "endDate": end,
    })
    games = []
    for d in j.get("dates", []):
        for g in d.get("games", []):
            games.append(g)
    return games


def game_result(g, team_id):
    st = g.get("status", {}).get("abstractGameState")
    if st != "Final":
        return None
    home = g["teams"]["home"]
    away = g["teams"]["away"]
    is_home = home["team"]["id"] == team_id
    me = home if is_home else away
    opp = away if is_home else home
    my_score = me.get("score", 0)
    opp_score = opp.get("score", 0)
    return {
        "date": g.get("gameDate", "")[:10],
        "opponent": opp.get("team", {}).get("name"),
        "opponentId": opp.get("team", {}).get("id"),
        "isHome": is_home,
        "scoreFor": my_score,
        "scoreAgainst": opp_score,
        "result": "W" if my_score > opp_score else "L",
    }


def main():
    hub = json.loads(HUB_FILE.read_text(encoding="utf-8"))
    ng = hub.get("nextGame")
    if not ng:
        print("[ERR] schedule-game-hub.json 没有 nextGame")
        sys.exit(1)

    opp_id = ng["opponent"]["id"]
    opp_name = ng["opponent"]["name"]
    opp_abbr = ng["opponent"]["abbreviation"]
    print(f"[INFO] 对手：{opp_name} ({opp_abbr}) id={opp_id}")

    today = datetime.now().strftime("%Y-%m-%d")

    # 1) 对手近期战绩（最近15场已赛）
    games = team_games(opp_id, f"{SEASON}-03-20", today)
    results = [r for r in (game_result(g, opp_id) for g in games) if r]
    results.sort(key=lambda x: x["date"], reverse=True)
    last15 = results[:15]
    last10 = results[:10]
    streak = 0
    if last10:
        last_r = last10[0]["result"]
        for r in last10:
            if r["result"] == last_r:
                streak += 1
            else:
                break
    record_now = next((t for t in api_get("/teams", {"teamId": opp_id, "hydrate": "teamStats"}).get("teams", [])), {})
    ts = (record_now.get("teamStats") or [{}])[0].get("splits", [{}])[0].get("stat", {})
    # 战绩以 standings 接口为准（需遍历分区记录找球队）
    st_j = api_get("/standings", {"leagueId": 104, "season": SEASON})
    rec = {"w": None, "l": None, "pct": None, "divisionRank": "?", "gamesBack": None}
    for div in st_j.get("records", []):
        for tr in div.get("teamRecords", []):
            if (tr.get("team") or {}).get("id") == opp_id:
                rec = {"w": tr.get("wins"), "l": tr.get("losses"),
                       "pct": tr.get("winningPercentage"),
                       "divisionRank": tr.get("divisionRank") or "?",
                       "divisionName": div.get("division", {}).get("name", ""),
                       "gamesBack": tr.get("gamesBack")}
                break
        if rec.get("w") is not None:
            break

    # 2) 对手关键打者（OPS 排序 PA≥150）
    hitters = []
    raw = api_get("/stats", {"stats": "season", "group": "hitting", "playerPool": "ALL",
                             "teamId": opp_id, "sportId": 1, "season": SEASON, "limit": 200})
    for st in raw.get("stats", []):
        for sp in st.get("splits", []):
            s = sp.get("stat", {})
            if int(s.get("plateAppearances") or 0) < 150:
                continue
            hitters.append({
                "name": sp.get("player", {}).get("fullName"),
                "avg": s.get("avg"), "obp": s.get("obp"), "slg": s.get("slg"),
                "ops": s.get("ops"), "hr": s.get("homeRuns"), "rbi": s.get("rbi"),
                "sb": s.get("stolenBases"), "pa": s.get("plateAppearances"),
            })
    hitters.sort(key=lambda x: float(x["ops"] or 0), reverse=True)
    hitters = hitters[:5]

    # 3) 对手投手群（ERA 排序 IP≥40）+ 先发轮值（GS≥5 按 ERA）
    pitchers = []
    raw = api_get("/stats", {"stats": "season", "group": "pitching", "playerPool": "ALL",
                             "teamId": opp_id, "sportId": 1, "season": SEASON, "limit": 200})
    for st in raw.get("stats", []):
        for sp in st.get("splits", []):
            if (sp.get("team") or {}).get("id") != opp_id:
                continue
            s = sp.get("stat", {})
            ip = float(s.get("inningsPitched", "0").replace(".1", ".33").replace(".2", ".67") or 0)
            if ip < 25:
                continue
            pitchers.append({
                "name": sp.get("player", {}).get("fullName"),
                "era": s.get("era"), "whip": s.get("whip"),
                "w": s.get("wins"), "l": s.get("losses"),
                "so": s.get("strikeOuts"), "ip": s.get("inningsPitched"),
                "gs": int(s.get("gamesStarted") or 0), "sv": int(s.get("saves") or 0),
            })
    pitchers.sort(key=lambda x: float(x["era"] if x["era"] not in ("-", "-.--") else 99))
    starters = sorted([p for p in pitchers if p["gs"] >= 3],
                      key=lambda x: float(x["era"] if x["era"] not in ("-", "-.--") else 99))[:4]
    relievers = sorted([p for p in pitchers if p["sv"] >= 2],
                       key=lambda x: -x["sv"])[:3]

    # 4) 对战历史：本季 + 上季 vs 道奇
    h2h = []
    for yr in (SEASON, SEASON - 1):
        gs = team_games(opp_id, f"{yr}-03-20", f"{yr}-12-01" if yr < SEASON else today)
        for g in gs:
            other = g["teams"]["home"]["team"]["id"] if g["teams"]["away"]["team"]["id"] == opp_id else g["teams"]["away"]["team"]["id"]
            if other == 119:
                r = game_result(g, opp_id)
                if r:
                    h2h.append(r)
        time.sleep(0.4)
    h2h.sort(key=lambda x: x["date"], reverse=True)
    h2h = h2h[:10]
    h2h_record = {"w": sum(1 for r in h2h if r["result"] == "L"), "l": sum(1 for r in h2h if r["result"] == "W")}
    # 站在道奇视角：对手胜 = 道奇负
    dodgers_view = [{"date": r["date"], "result": r["result"], "score": f'{r["scoreAgainst"]}-{r["scoreFor"]}', "venue": "主场" if r["isHome"] else "客场"} for r in h2h]

    # 5) 球场
    venue = ng.get("venue", "")
    park_note = PARK_NOTES.get(venue, "中性球场，暂无特殊备注")

    data = {
        "generatedAt": datetime.now().isoformat(),
        "season": SEASON,
        "nextGame": {
            "date": ng.get("date"),
            "beijingTime": ng.get("beijingTime"),
            "venue": venue,
            "isHome": ng.get("isHome"),
            "gamePk": ng.get("gamePk"),
            "dodgersPitcher": ng.get("probablePitcher"),
            "dodgersPitcherStats": ng.get("pitcherStats"),
            "opponentPitcher": ng.get("opponentProbablePitcher"),
            "opponentPitcherStats": ng.get("opponentPitcherStats"),
        },
        "opponent": {
            "id": opp_id, "name": opp_name, "abbr": opp_abbr,
            "record": rec,
        },
        "recentForm": {
            "last10": {"w": sum(1 for r in last10 if r["result"] == "W"),
                       "l": sum(1 for r in last10 if r["result"] == "L")},
            "last15": [{"date": r["date"], "r": r["result"],
                        "score": f'{r["scoreFor"]}-{r["scoreAgainst"]}',
                        "vs": r["opponent"]} for r in last15],
            "streak": {"type": last_r if last10 else None, "count": streak},
        },
        "keyHitters": hitters,
        "keyPitchers": {"rotation": starters, "bullpen": relievers},
        "headToHead": {"games": dodgers_view, "dodgersW": h2h_record["w"], "dodgersL": h2h_record["l"]},
        "park": {"name": venue, "note": park_note},
    }

    if OUTPUT_FILE.exists():
        shutil.copy2(OUTPUT_FILE, OUTPUT_FILE.with_suffix(".json.bak"))
    OUTPUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] {OUTPUT_FILE}")
    print(f"     对手战绩 {rec.get('w')}-{rec.get('l')}（分区第{rec.get('divisionRank','?')}） 近10场 {data['recentForm']['last10']}"
          f"  streak {streak}{last_r if last10 else ''}")
    print(f"     对战史（道奇视角）近{len(dodgers_view)}场 {h2h_record['w']}胜{h2h_record['l']}负")
    print(f"     关键打者: {[h['name'] for h in hitters]}")
    print(f"     先发: {[p['name'] for p in starters]} 终结者: {[p['name'] for p in relievers]}")


if __name__ == "__main__":
    main()
