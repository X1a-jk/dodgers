#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历年阵容（Season Roster）——某赛季所有为道奇出场过的球员，含中途签来/DFA/交易离队者。

数据源：
1. /api/v1/stats（playerPool=ALL，hitting+pitching）→ 本赛季出场过的所有球员及数据
2. depth-chart.json → 当前 40 人状态（活跃/伤病/小联盟）；不在其中 = 已离队
3. transactions.json（all 全量）→ 每人赛季轨迹：签约/交易获得/上调/下放/DFA/释出

输出 D:\\baseball\\data\\season-roster.json
归档后由门户按 seasons\\YYYY\\snapshots\\season-roster.json 读取（archive-season.py 自动快照）
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
OUTPUT_FILE = BASE_DIR / "data" / "season-roster.json"
SEASON = datetime.now().year
API = "https://statsapi.mlb.com/api/v1"
DODGERS = "Los Angeles Dodgers"

# 交易方向之外的离队动作（用于判定"已离队"原因）
DEPART_CATS = {"dfa": "DFA", "released": "释出", "outright": "Outright 下放",
               "option": "下放小联盟"}
JOIN_CATS = {"signed": "签约", "recall": "上调"}


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


def fmt_date(d):
    return d[5:].replace("-", "/") if d else "?"


def fetch_appearances():
    """本赛季为道奇出场的所有球员（打击+投球合并，二刀流合一）"""
    players = {}
    for grp in ("hitting", "pitching"):
        j = api_get("/stats", {"stats": "season", "group": grp,
                               "playerPool": "ALL", "teamId": 119,
                               "season": SEASON, "limit": 200})
        splits = ((j.get("stats") or [{}])[0].get("splits")) or []
        for sp in splits:
            person = sp.get("player") or {}
            stat = sp.get("stat") or {}
            pos = (sp.get("position") or {}).get("abbreviation") or "?"
            pid = person.get("id")
            p = players.setdefault(pid, {
                "id": pid, "name": person.get("fullName"), "pos": pos,
                "g": 0, "bat": None, "pit": None,
            })
            p["g"] = max(p["g"], int(stat.get("gamesPlayed") or 0))
            if grp == "hitting" and int(stat.get("atBats") or 0) > 0:
                p["bat"] = {"avg": stat.get("avg"), "hr": stat.get("homeRuns"),
                            "rbi": stat.get("rbi"), "ops": stat.get("ops"),
                            "sb": stat.get("stolenBases"),
                            "hits": stat.get("hits")}
            if grp == "pitching" and (stat.get("inningsPitched") or "0") != "0":
                p["pit"] = {"w": stat.get("wins"), "l": stat.get("losses"),
                            "era": stat.get("era"), "so": stat.get("strikeOuts"),
                            "sv": stat.get("saves"),
                            "ip": stat.get("inningsPitched")}
            # 位置偏好：投球数据存在且为主要身份时标 P
            if grp == "pitching" and not p["bat"]:
                p["pos"] = "P"
    return list(players.values())


def load_current_status():
    """depth-chart.json → {playerId: (statusCode, statusCn)}"""
    path = BASE_DIR / "data" / "depth-chart.json"
    out = {}
    if not path.exists():
        return out
    j = json.loads(path.read_text(encoding="utf-8"))
    groups = []
    for col in j.get("columns") or []:
        groups.extend(col.get("players") or [])
    groups.extend(j.get("starters") or [])
    groups.extend(j.get("relievers") or [])
    for p in groups:
        if p.get("id"):
            out[p["id"]] = (p.get("statusCode") or "?"), (p.get("status") or "?")
    return out


def load_moves():
    """transactions.json all → 按球员分组的赛季轨迹"""
    path = BASE_DIR / "data" / "transactions.json"
    if not path.exists():
        return {}
    j = json.loads(path.read_text(encoding="utf-8"))
    by_player = {}
    for tx in j.get("all") or []:
        pid = tx.get("playerId")
        if not pid:
            continue
        by_player.setdefault(pid, []).append(tx)
    for txs in by_player.values():
        txs.sort(key=lambda x: x.get("date") or "")
    return by_player


def player_timeline(txs):
    """从全量 transactions 提取：joined（中途加入标签）/ departed（离队标签）/ moves（展示用轨迹）"""
    joined = None
    departed = None
    moves = []
    opening_day = f"{SEASON}-04-05"  # 4 月初之后加入算"中途"
    for tx in txs or []:
        cat = tx.get("category")
        d = tx.get("date") or ""
        to_lad = tx.get("toTeam") == DODGERS
        from_lad = tx.get("fromTeam") == DODGERS
        if cat == "trade":
            if to_lad and not from_lad:
                moves.append({"date": d, "text": "交易获得"})
                if d > opening_day and not joined:
                    joined = f"交易获得 {fmt_date(d)}"
            elif from_lad and not to_lad:
                moves.append({"date": d, "text": "交易离队"})
                departed = f"交易离队 {fmt_date(d)}"
        elif cat in JOIN_CATS and to_lad:
            moves.append({"date": d, "text": JOIN_CATS[cat]})
            if d > opening_day and not joined:
                joined = f"{JOIN_CATS[cat]} {fmt_date(d)}"
        elif cat in DEPART_CATS and (from_lad or not to_lad):
            moves.append({"date": d, "text": DEPART_CATS[cat]})
            if cat in ("dfa", "released", "outright"):
                departed = f"{DEPART_CATS[cat]} {fmt_date(d)}"
    return joined, departed, moves


def main():
    print(f"[season-roster] 抓取 {SEASON} 历年阵容 {datetime.now():%Y-%m-%d %H:%M}", flush=True)

    players = fetch_appearances()
    if not players:
        print("[season-roster] 出场数据为空，保留旧缓存")
        return
    status_map = load_current_status()
    moves_map = load_moves()

    rows = []
    for p in players:
        joined, departed, moves = player_timeline(moves_map.get(p["id"]))
        if p["id"] in status_map:
            code, cn = status_map[p["id"]]
            status, status_cn = code.lower(), cn
        else:
            status, status_cn = "departed", (departed.split()[0] if departed else "已离队")
        rows.append({
            **p,
            "status": status,
            "statusCn": status_cn,
            "joined": joined,
            "departed": None if status != "departed" else (departed or "已离队"),
            "moves": [m for m in moves if m["text"] in
                      ("交易获得", "交易离队", "签约", "DFA", "释出", "Outright 下放")][-4:],
        })
    rows.sort(key=lambda r: -r["g"])

    summary = {
        "total": len(rows),
        "current": sum(1 for r in rows if r["status"] in ("a", "active")),
        "il": sum(1 for r in rows if r["status"] in ("il", "d10", "d15", "d60")),
        "minors": sum(1 for r in rows if r["status"] in ("minors", "rm")),
        "departed": sum(1 for r in rows if r["status"] == "departed"),
        "joinedMidseason": sum(1 for r in rows if r["joined"]),
    }

    data = {
        "generatedAt": datetime.now().isoformat(),
        "season": SEASON,
        "summary": summary,
        "players": rows,
    }
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT_FILE.exists():
        shutil.copy2(OUTPUT_FILE, str(OUTPUT_FILE) + ".bak")
    OUTPUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[season-roster] 已写入 {OUTPUT_FILE}（{summary['total']} 人，"
          f"中途加入 {summary['joinedMidseason']}，离队 {summary['departed']}）", flush=True)


if __name__ == "__main__":
    main()
