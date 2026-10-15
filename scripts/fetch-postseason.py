#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
季后赛对阵追踪（Postseason Tracker）：
1) 从常规赛最终排名构建 12 队双联盟对阵树（分区冠军 1-3 种子 + 外卡 4-6）
2) 抓取季后赛赛程（gameTypes=F,D,L,W——注意季后赛 gameType 不是 P），聚合每个系列赛的比分与状态
3) 道奇专属：种子位、晋级路线、下一个季后赛比赛

输出 D:\\baseball\\data\\postseason.json（.bak 兜底）
接入每日管线：fetch-dashboard-data 之后运行
"""
import json
import shutil
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
BASE_DIR = Path(r"D:\baseball")
OUTPUT_FILE = BASE_DIR / "data" / "postseason.json"
SEASON = datetime.now().year
API = "https://statsapi.mlb.com/api/v1"
DODGERS_ID = 119

CN_NAME = {
    "NL": "国联", "AL": "美联",
}

ROUND_CN = {
    "Wild Card Series": "外卡系列赛",
    "Division Series": "分区系列赛",
    "League Championship Series": "联盟冠军赛",
    "World Series": "世界大赛",
}


def api_get(path, params=None, retries=4, timeout=30, min_key=None):
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


def beijing(iso_dt):
    """ISO 时间 -> 北京时间字符串"""
    try:
        dt = datetime.fromisoformat(iso_dt.replace("Z", "+00:00"))
        return (dt + timedelta(hours=8)).strftime("%m-%d %H:%M")
    except Exception:
        return None


def build_bracket():
    """从常规赛最终排名构建 12 队对阵树。返回 {league: {...}}"""
    st = api_get("/standings",
                 {"leagueId": "103,104", "season": SEASON,
                  "hydrate": "division,team"},
                 min_key="records")
    leagues = {}
    for rec in st.get("records", []):
        if rec.get("standingsType") != "regularSeason":
            continue
        lid = rec.get("league", {}).get("id")
        lcode = "AL" if lid == 103 else "NL"
        div = rec.get("division", {})
        dname = div.get("name", "?")
        for tr in rec.get("teamRecords", []):
            team = tr.get("team") or {}
            leagues.setdefault(lcode, []).append({
                "id": team.get("id"),
                "name": team.get("name"),
                "abbr": team.get("abbreviation"),
                "div": dname.split()[-1],  # East/Central/West
                "divRank": int(tr.get("divisionRank") or 9),
                "w": tr.get("wins"), "l": tr.get("losses"),
                "pct": float(tr.get("winningPercentage") or 0),
            })
    out = {}
    for lcode, teams in leagues.items():
        div_winners = sorted([t for t in teams if t["divRank"] == 1],
                             key=lambda t: -t["pct"])
        for i, t in enumerate(div_winners):
            t["seed"] = i + 1
        others = sorted([t for t in teams if t["divRank"] != 1],
                        key=lambda t: -t["pct"])
        for i, t in enumerate(others[:3]):
            t["seed"] = i + 4
        out[lcode] = {
            "name": CN_NAME.get(lcode, lcode),
            "teams": {t["seed"]: t for t in div_winners + others[:3]},
        }
    return out


def fetch_postseason_games():
    """抓取整个季后赛赛程（双联盟），按系列赛聚合"""
    today = datetime.now().strftime("%Y-%m-%d")
    end = f"{SEASON}-11-10"
    sched = api_get("/schedule",
                    {"sportId": 1, "gameTypes": "F,D,L,W",
                     "startDate": f"{SEASON}-09-28", "endDate": end,
                     "hydrate": "team,linescore,flags",
                     "fields": "dates,date,games,gamePk,gameDate,gameType,seriesDescription,seriesGameNumber,gamesInSeries,teams,away,home,team,id,name,score,winner,loser,isWinner,status,detailedState,abstractGameState"})
    # 未公布季后赛赛程时 dates 为空属正常，不重试
    series = {}
    for d in sched.get("dates", []):
        for g in d.get("games", []):
            desc_full = g.get("seriesDescription") or "?"
            # 实际数据带联盟前缀（"NL Wild Card Series"/"AL Championship Series"）。
            # key 用原始值区分联盟；round 归一化掉前缀供 find_series 匹配。
            desc = desc_full
            for pre in ("AL ", "NL "):
                if desc.startswith(pre):
                    desc = desc[len(pre):]
            if desc == "Championship Series":
                desc = "League Championship Series"
            away = g["teams"]["away"]
            home = g["teams"]["home"]
            a_id, h_id = away["team"].get("id") or 0, home["team"].get("id") or 0
            # key 必须能区分同联盟同轮次的两个系列赛（seriesDescription 只有轮次名）
            key = f"{desc_full}#{min(a_id, h_id)}-{max(a_id, h_id)}"
            s = series.setdefault(key, {"round": desc, "games": []})
            status = g.get("status", {})
            winner_side = None
            if status.get("abstractGameState") == "Final":
                if away.get("isWinner"):
                    winner_side = "away"
                elif home.get("isWinner"):
                    winner_side = "home"
            s["games"].append({
                "gamePk": g.get("gamePk"),
                "date": g.get("gameDate"),
                "beijing": beijing(g.get("gameDate", "")),
                "gameNumber": g.get("seriesGameNumber"),
                "gamesInSeries": g.get("gamesInSeries"),
                "status": status.get("detailedState"),
                "final": status.get("abstractGameState") == "Final",
                "away": {"id": away["team"].get("id"),
                         "name": away["team"].get("name"),
                         "score": away.get("score")},
                "home": {"id": home["team"].get("id"),
                         "name": home["team"].get("name"),
                         "score": home.get("score")},
                "winnerSide": winner_side,
            })
    return series, bool(sched.get("dates"))


def aggregate_series(bracket, series_map):
    """把 schedule 里的系列赛按队伍种子归属到对阵槽位"""
    teams_by_id = {}
    for lcode, lg in bracket.items():
        for t in lg["teams"].values():
            teams_by_id[t["id"]] = (lcode, t["seed"])

    def find_series(round_desc, team_ids):
        """在指定轮次里找涉及这些队伍的系列赛"""
        for s in series_map.values():
            if s["round"] != round_desc or not s["games"]:
                continue
            g = s["games"][0]
            ids = {g["away"]["id"], g["home"]["id"]}
            if ids & set(team_ids):
                return s
        return None

    def series_view(s, best_of):
        if not s:
            return None
        games = sorted(s["games"], key=lambda x: (x["gameNumber"] or 99))
        # 汇总胜场
        wins = {}
        done = 0
        for g in games:
            if g["final"]:
                done += 1
                if g["winnerSide"]:
                    tid = g[g["winnerSide"]]["id"]
                    wins[tid] = wins.get(tid, 0) + 1
        return {"round": s["round"], "bestOf": best_of, "games": games,
                "wins": wins, "gamesPlayed": done,
                "hasData": True}

    out = {}
    for lcode, lg in bracket.items():
        t = lg["teams"]
        wc1 = find_series("Wild Card Series", [t[3]["id"], t[6]["id"]])
        wc2 = find_series("Wild Card Series", [t[4]["id"], t[5]["id"]])
        nl_ds = "Division Series"
        ds1 = find_series(nl_ds, [t[1]["id"]] +
                          ([t[3]["id"], t[6]["id"]] if not wc1 else []))
        ds2 = find_series(nl_ds, [t[2]["id"]] +
                          ([t[4]["id"], t[5]["id"]] if not wc2 else []))
        out[lcode] = {
            "wc": [series_view(wc1, 3), series_view(wc2, 3)],
            "ds": [series_view(ds1, 5), series_view(ds2, 5)],
            "cs": series_view(find_series("League Championship Series",
                                          [x["id"] for x in t.values()]), 7),
        }
    ws = find_series("World Series", list(teams_by_id.keys()))
    out["ws"] = series_view(ws, 7)
    return out


def fetch_team_leaders():
    """道奇常规赛球队领袖：打击 HR/RBI/SB/AVG、投球 W/ERA/WHIP/SV"""
    leaders = {}
    for grp, metrics in (("hitting", ["homeRuns", "rbi", "stolenBases", "avg", "hits", "ops"]),
                         ("pitching", ["wins", "era", "whip", "saves", "strikeOuts", "inningsPitched"])):
        j = api_get("/stats",
                    {"stats": "season", "group": grp, "playerPool": "ALL",
                     "teamId": DODGERS_ID, "season": SEASON, "limit": 100})
        splits = ((j.get("stats") or [{}])[0].get("splits")) or []
        rows = []
        for sp in splits:
            st = sp.get("stat") or {}
            person = ((sp.get("player") or {}))
            rows.append({
                "id": person.get("id"),
                "name": person.get("fullName"),
                **{m: st.get(m) for m in metrics},
                "g": st.get("gamesPlayed"),
            })
        leaders[grp] = rows
    # 简易榜单：打击按 HR 排序取前5（AVG 要求一定场次）
    def top(rows, key, n=5, reverse=True, min_g=0):
        xs = [r for r in rows if r.get(key) is not None and (r.get("g") or 0) >= min_g]
        xs.sort(key=lambda r: (float(r[key]) if str(r[key]).replace('.', '').isdigit() else 0),
                reverse=reverse)
        return xs[:n]
    hit = leaders["hitting"]
    pit = leaders["pitching"]
    return {
        "hitting": {
            "hr": top(hit, "homeRuns"),
            "rbi": top(hit, "rbi"),
            "sb": top(hit, "stolenBases"),
            "avg": top(hit, "avg", min_g=80),
            "ops": top(hit, "ops", min_g=80),
        },
        "pitching": {
            "w": top(pit, "wins"),
            "so": top(pit, "strikeOuts"),
            "sv": top(pit, "saves"),
            "era": top(pit, "era", n=5, reverse=False, min_g=10),
            "whip": top(pit, "whip", n=5, reverse=False, min_g=10),
        },
    }


def main():
    today = datetime.now()
    print(f"[postseason] 抓取 {SEASON} 季后赛对阵 {today:%Y-%m-%d %H:%M}", flush=True)

    bracket = build_bracket()
    if not bracket or "NL" not in bracket:
        print("[postseason] 常规赛排名抓取失败，保留旧缓存")
        return

    series_map, published = fetch_postseason_games()
    print(f"[postseason] 季后赛赛程已公布: {published}（系列赛数: {len(series_map)}）",
          flush=True)

    rounds = aggregate_series(bracket, series_map) if published else {}
    leaders = fetch_team_leaders()
    print(f"[postseason] 球队领袖: 打击{len(leaders['hitting']['hr'])}人/投球{len(leaders['pitching']['w'])}人", flush=True)

    dod = bracket["NL"]["teams"].get(2)
    dodgers_info = {
        "teamId": DODGERS_ID,
        "seed": dod["seed"] if dod and dod.get("id") == DODGERS_ID else None,
        "record": f"{dod['w']}-{dod['l']}" if dod else None,
        "status": "外卡轮轮空，备战分区系列赛" if not published else "季后赛进行中",
    }

    data = {
        "generatedAt": today.isoformat(),
        "season": SEASON,
        "regularSeasonComplete": True,
        "postseasonPublished": published,
        "bracket": {lc: {"name": lg["name"],
                         "teams": {str(k): v for k, v in lg["teams"].items()}}
                    for lc, lg in bracket.items()},
        "rounds": rounds,
        "roundCn": ROUND_CN,
        "dodgers": dodgers_info,
        "leaders": leaders,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT_FILE.exists():
        shutil.copy2(OUTPUT_FILE, str(OUTPUT_FILE) + ".bak")
    OUTPUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=1),
                           encoding="utf-8")
    print(f"[postseason] 已写入 {OUTPUT_FILE}", flush=True)


if __name__ == "__main__":
    main()
