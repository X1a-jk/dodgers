#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
里程碑与纪录：球星追逐中的里程碑 + 球队 vs 2024 冠军年同期对比。
输出 D:\\baseball\\data\\milestones.json
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
OUTPUT_FILE = BASE_DIR / "data" / "milestones.json"
SEASON = datetime.now().year
API = "https://statsapi.mlb.com/api/v1"

TRACKED = [
    # (playerId, 中文名, 关注项)
    (660271, "大谷翔平", ["hr", "sb", "rbi", "hits"]),
    (605141, "Mookie Betts", ["hits", "hr"]),
    (518692, "Freddie Freeman", ["hits", "hr"]),
]

STAT_CN = {"hr": "本垒打", "hits": "安打", "sb": "盗垒", "rbi": "打点"}
API_KEY = {"hr": "homeRuns", "hits": "hits", "sb": "stolenBases", "rbi": "rbi"}


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


def next_target(v):
    """下一个整数里程碑：按量级取 10/25/50/100 的倍数"""
    if v < 25:
        return ((v // 10) + 1) * 10
    if v < 100:
        return ((v // 25) + 1) * 25
    if v < 300:
        return ((v // 50) + 1) * 50
    return ((v // 100) + 1) * 100


def player_stats(pid, group="hitting"):
    # 注意：stats=season,career 合并查询时 career split 可能缺 homeRuns 等字段，分开查更稳
    # 网络不稳时 CDN 可能返回缺字段的降级响应，校验关键键，不达标重试
    season = career = {}
    for attempt in range(5):
        j = api_get(f"/people/{pid}/stats", {"stats": "season", "group": group})
        splits = (j.get("stats") or [{}])[0].get("splits", [])
        if splits and "homeRuns" in splits[-1].get("stat", {}):
            season = splits[-1]["stat"]
            break
        season = splits[-1].get("stat", {}) if splits else {}
        print(f"  [warn] season 响应缺字段，重试 {attempt + 1}/5", flush=True)
        time.sleep(2)
    time.sleep(0.4)
    for attempt in range(5):
        j = api_get(f"/people/{pid}/stats", {"stats": "career", "group": group})
        splits = (j.get("stats") or [{}])[0].get("splits", [])
        if splits and "homeRuns" in splits[-1].get("stat", {}):
            career = splits[-1]["stat"]
            break
        career = splits[-1].get("stat", {}) if splits else {}
        print(f"  [warn] career 响应缺字段，重试 {attempt + 1}/5", flush=True)
        time.sleep(2)
    return season, career


def main():
    players = []
    for pid, cn_name, keys in TRACKED:
        info = next((p for p in api_get(f"/people/{pid}").get("people", [])), {})
        season, career = player_stats(pid)
        items = []
        for k in keys:
            sv = int(season.get(API_KEY[k]) or 0)
            cv = int(career.get(API_KEY[k]) or 0)
            it = {"stat": STAT_CN[k], "seasonValue": sv}
            if cv:
                tgt = next_target(cv)
                it.update({
                    "careerValue": cv,
                    "target": tgt,
                    "remaining": max(tgt - cv, 0),
                    "progress": round(cv / tgt * 100, 1),
                })
            items.append(it)
        players.append({
            "name": info.get("fullName", cn_name),
            "nameCn": cn_name,
            "seasonLine": f'{season.get("avg", "-")}/{season.get("obp", "-")}/{season.get("slg", "-")}',
            "seasonHr": int(season.get("homeRuns") or 0),
            "seasonSb": int(season.get("stolenBases") or 0),
            "milestones": items,
        })
        time.sleep(0.4)

    # 球队：当前战绩 + 2024 冠军年同期战绩 + 最终战绩
    st_j = {}
    for attempt in range(5):
        st_j = api_get("/standings", {"leagueId": 104, "season": SEASON})
        if any(div.get("teamRecords") for div in st_j.get("records", [])):
            break
        print(f"  [warn] standings 响应异常，重试 {attempt + 1}/5", flush=True)
        time.sleep(2)
    cur = {}
    for div in st_j.get("records", []):
        for tr in div.get("teamRecords", []):
            if (tr.get("team") or {}).get("id") == 119:
                cur = {"w": tr.get("wins"), "l": tr.get("losses"),
                       "pct": tr.get("winningPercentage"),
                       "divisionRank": tr.get("divisionRank"),
                       "magicNumber": tr.get("magicNumber"),
                       "gamesBack": tr.get("gamesBack")}
    cur["gamesPlayed"] = (cur.get("w") or 0) + (cur.get("l") or 0)

    def record_through(date_cap):
        for attempt in range(5):
            j = api_get("/schedule", {"teamId": 119, "sportId": 1,
                                      "startDate": "2024-03-20", "endDate": date_cap})
            dates = j.get("dates", [])
            if dates:
                break
            print(f"  [warn] schedule({date_cap}) 响应为空，重试 {attempt + 1}/5", flush=True)
            time.sleep(2)
        w = l = 0
        for d in dates:
            for g in d.get("games", []):
                if g.get("status", {}).get("abstractGameState") != "Final":
                    continue
                home = g["teams"]["home"]
                away = g["teams"]["away"]
                me = home if home["team"]["id"] == 119 else away
                opp = away if me is home else home
                if me.get("score", 0) > opp.get("score", 0):
                    w += 1
                else:
                    l += 1
        return w, l

    today_md = datetime.now().strftime("%m-%d")
    y2024_w, y2024_l = record_through(f"2024-{today_md}")
    final2024_w, final2024_l = record_through("2024-11-30")
    time.sleep(0.4)

    gp = cur.get("gamesPlayed") or 0
    pace_w = round((cur.get("w") or 0) / gp * 162) if gp else None
    team_cmp = {
        "current": cur,
        "pace162": pace_w,
        "y2024ThroughToday": {"w": y2024_w, "l": y2024_l},
        "y2024Final": {"w": final2024_w, "l": final2024_l},
        "diffThroughToday": (cur.get("w") or 0) - y2024_w,
    }

    data = {
        "generatedAt": datetime.now().isoformat(),
        "season": SEASON,
        "players": players,
        "teamComparison": team_cmp,
    }
    if OUTPUT_FILE.exists():
        shutil.copy2(OUTPUT_FILE, OUTPUT_FILE.with_suffix(".json.bak"))
    OUTPUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] {OUTPUT_FILE}")
    for p in players:
        ms = "; ".join(f'{m["stat"]}: 生涯{m.get("careerValue", "?")}→{m.get("target", "?")}' for m in p["milestones"])
        print(f'  {p["name"]} ({p["seasonLine"]}) {ms}')
    print(f"  球队 {cur.get('w')}-{cur.get('l')} 分区第{cur.get('divisionRank')} pace {pace_w}胜 | "
          f"2024 同日 {y2024_w}-{y2024_l}（最终 {final2024_w}-{final2024_l}） 差 {team_cmp['diffThroughToday']:+d}")


if __name__ == "__main__":
    main()
