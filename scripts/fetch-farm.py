#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
道奇农场系统数据抓取：附属小联盟球队昨日赛果 + 亮点扫描 + 层级数据领跑者。
输出 D:\\baseball\\data\\farm.json，由每日任务调用。

数据源：statsapi（小联盟 schedule / boxscore / stats）
注意：本机系统代理常处于关闭状态，所有请求禁用系统代理直连 + 重试。
"""
import json
import shutil
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests

BASE_DIR = Path(r"D:\baseball")
OUTPUT_FILE = BASE_DIR / "data" / "farm.json"
SEASON = datetime.now().year

# 2026 道奇附属球队（Rookie 级 3 队不追踪）
AFFILIATES = [
    {"id": 238, "name": "Oklahoma City Comets", "level": "AAA", "levelCn": "3A", "sportId": 11},
    {"id": 260, "name": "Tulsa Drillers", "level": "AA", "levelCn": "2A", "sportId": 12},
    {"id": 456, "name": "Great Lakes Loons", "level": "A+", "levelCn": "高阶1A", "sportId": 13},
    {"id": 6482, "name": "Ontario Tower Buzzers", "level": "A", "levelCn": "1A", "sportId": 14},
]

API = "https://statsapi.mlb.com/api/v1"


def api_get(path, params=None, retries=4, timeout=20):
    """直连（绕过可能关闭的系统代理）+ 指数退避重试。"""
    url = API + path
    last_err = None
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=timeout,
                             proxies={"http": None, "https": None})
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last_err = e
            print(f"  [retry {attempt + 1}/{retries}] {path}: {type(e).__name__}")
            time.sleep(1.5 * (attempt + 1))
    print(f"  [FAIL] {path}: {last_err}")
    return {}


def ip_to_outs(ip_str):
    """'6.1' -> 19 outs"""
    try:
        whole, _, frac = str(ip_str).partition(".")
        return int(whole) * 3 + int(frac or 0)
    except ValueError:
        return 0


def scan_highlights(box, affiliate_id):
    """从小联盟 boxscore 扫亮点。返回 [(name, feats[])]"""
    highlights = []
    for side in ("home", "away"):
        team = box.get("teams", {}).get(side, {})
        if team.get("team", {}).get("id") != affiliate_id:
            continue
        for pid, p in team.get("players", {}).items():
            name = p.get("person", {}).get("fullName", "?")
            feats = []
            b = p.get("stats", {}).get("batting") or {}
            if b.get("atBats", 0) > 0:
                hr = int(b.get("homeRuns") or 0)
                hits = int(b.get("hits") or 0)
                rbi = int(b.get("rbi") or 0)
                sb = int(b.get("stolenBases") or 0)
                if hr >= 2:
                    feats.append(f"单场 {hr} 轰")
                if hits >= 4:
                    feats.append(f"单场 {hits} 安打")
                if rbi >= 5:
                    feats.append(f"打回 {rbi} 分")
                if sb >= 2:
                    feats.append(f"盗垒 {sb} 次")
                if feats:
                    line = f"{b.get('hits', 0)}/{b.get('atBats', 0)}"
                    feats.append(f"{line} · {hr} HR · {rbi} RBI")
            pt = p.get("stats", {}).get("pitching") or {}
            if pt.get("inningsPitched"):
                outs = ip_to_outs(pt.get("inningsPitched"))
                er = int(pt.get("earnedRuns") or 0)
                so = int(pt.get("strikeOuts") or 0)
                pfeats = []
                if outs >= 18 and er <= 1:
                    pfeats.append(f"优质先发 {pt.get('inningsPitched')} 局仅 {er} 自责")
                if so >= 8:
                    pfeats.append(f"{so} 次三振")
                if pfeats:
                    pfeats.append(f"{pt.get('inningsPitched')} 局 {er} 自责 · {so}K")
                    feats = pfeats
            if feats:
                highlights.append({"name": name, "feats": feats})
    return highlights


def fetch_affiliate(aff):
    today = datetime.now().date()
    start = (today - timedelta(days=4)).strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")

    # 1) 最近一场已赛比赛
    sched = api_get("/schedule", {
        "teamId": aff["id"], "sportId": aff["sportId"],
        "startDate": start, "endDate": end,
    })
    last_game = None
    game_pk = None
    for d in sorted(sched.get("dates", []), key=lambda x: x.get("date", ""), reverse=True):
        for g in d.get("games", []):
            if g.get("status", {}).get("abstractGameState") == "Final":
                is_home = g["teams"]["home"]["team"]["id"] == aff["id"]
                my = g["teams"]["home"] if is_home else g["teams"]["away"]
                opp = g["teams"]["away"] if is_home else g["teams"]["home"]
                my_score = my.get("score", 0)
                opp_score = opp.get("score", 0)
                last_game = {
                    "date": d.get("date"),
                    "opponent": opp.get("team", {}).get("name", "?"),
                    "isHome": is_home,
                    "score": {"for": my_score, "against": opp_score},
                    "result": "W" if my_score > opp_score else "L",
                }
                game_pk = g.get("gamePk")
                break
        if last_game:
            break

    # 今天是否有比赛（预告）
    today_game = None
    for d in sched.get("dates", []):
        if d.get("date") == end:
            for g in d.get("games", []):
                if g.get("status", {}).get("abstractGameState") != "Final":
                    opp_side = "away" if g["teams"]["home"]["team"]["id"] == aff["id"] else "home"
                    today_game = {
                        "opponent": g["teams"][opp_side]["team"].get("name", "?"),
                        "status": g.get("status", {}).get("detailedState", "Scheduled"),
                    }

    # 2) 亮点扫描
    highlights = []
    if game_pk:
        box = api_get(f"/game/{game_pk}/boxscore")
        highlights = scan_highlights(box, aff["id"])

    # 3) 赛季领跑者
    hitters = []
    raw = api_get("/stats", {
        "stats": "season", "group": "hitting", "teamId": aff["id"],
        "sportId": aff["sportId"], "season": SEASON, "limit": 100,
    })
    for st in raw.get("stats", []):
        for sp in st.get("splits", []):
            s = sp.get("stat", {})
            if int(s.get("plateAppearances") or 0) < 80:
                continue
            try:
                ops = float(s.get("ops") or 0)
            except ValueError:
                ops = 0
            hitters.append({
                "name": sp.get("player", {}).get("fullName", "?"),
                "avg": s.get("avg", "-"), "obp": s.get("obp", "-"),
                "slg": s.get("slg", "-"), "ops": s.get("ops", "-"),
                "hr": s.get("homeRuns", 0), "rbi": s.get("rbi", 0),
                "sb": s.get("stolenBases", 0),
                "pa": s.get("plateAppearances", 0),
                "callupWatch": ops >= (0.90 if aff["level"] == "AAA" else 1.00),
            })
    hitters.sort(key=lambda x: float(x["ops"] or 0), reverse=True)
    hitters = hitters[:4]

    pitchers = []
    raw = api_get("/stats", {
        "stats": "season", "group": "pitching", "teamId": aff["id"],
        "sportId": aff["sportId"], "season": SEASON, "limit": 100,
    })
    for st in raw.get("stats", []):
        for sp in st.get("splits", []):
            s = sp.get("stat", {})
            if ip_to_outs(s.get("inningsPitched", "0")) < 35 * 3:
                continue
            try:
                era = float(s.get("era") or 99)
            except ValueError:
                era = 99
            pitchers.append({
                "name": sp.get("player", {}).get("fullName", "?"),
                "w": s.get("wins", 0), "l": s.get("losses", 0),
                "era": s.get("era", "-"), "whip": s.get("whip", "-"),
                "so": s.get("strikeOuts", 0), "ip": s.get("inningsPitched", "0"),
                "callupWatch": aff["level"] == "AAA" and era <= 3.00,
            })
    pitchers.sort(key=lambda x: float(x["era"] if x["era"] not in ("-", "-.--") else 99))
    pitchers = pitchers[:4]

    return {
        **aff,
        "lastGame": last_game,
        "todayGame": today_game,
        "highlights": highlights,
        "leaders": {"hitters": hitters, "pitchers": pitchers},
    }


def main():
    print("[INFO] Fetching farm system data (4 affiliates)...")
    affiliates = []
    for aff in AFFILIATES:
        print(f"[INFO] {aff['level']} {aff['name']} ...")
        affiliates.append(fetch_affiliate(aff))

    data = {
        "generatedAt": datetime.now().isoformat(),
        "season": SEASON,
        "affiliates": affiliates,
    }
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUTPUT_FILE.with_suffix(".tmp")
    if OUTPUT_FILE.exists():
        shutil.copy2(OUTPUT_FILE, OUTPUT_FILE.with_suffix(".json.bak"))
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(OUTPUT_FILE)
    print(f"[OK] Saved {OUTPUT_FILE}")
    for a in affiliates:
        lg = a["lastGame"]
        lg_txt = f"{lg['result']} {lg['score']['for']}-{lg['score']['against']} vs {lg['opponent']}" if lg else "无近期比赛"
        print(f"     {a['level']}: {lg_txt} | highlights={len(a['highlights'])} "
              f"| leaders H={len(a['leaders']['hitters'])} P={len(a['leaders']['pitchers'])}")
    sys.exit(0)


if __name__ == "__main__":
    main()
