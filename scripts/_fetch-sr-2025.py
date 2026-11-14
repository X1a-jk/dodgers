#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2025 赛季历年阵容快照（一次性脚本）
生成 seasons\\2025\\snapshots\\season-roster.json，schema 与 2026 快照完全一致。
视角截断 2025-11-02（世界大赛结束），status：赛季末仍在队 = a/活跃，否则 departed。
"""
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
BASE_DIR = Path(r"D:\baseball")
OUT = BASE_DIR / "seasons" / "2025" / "snapshots" / "season-roster.json"
SEASON = 2025
CUTOFF = "2025-11-02"      # 世界大赛结束后；之后的宣布自由球员不计
OPENING = "2025-03-31"     # 此后加入算"中途"
API = "https://statsapi.mlb.com/api/v1"
DODGERS = "Los Angeles Dodgers"

# raw typeCode -> (category, 中文标签)
TYPE_MAP = {
    "TR":  ("trade", "交易"),
    "SFA": ("signed", "签约"),
    "SGN": ("signed", "签约"),
    "CLW": ("signed", "认领"),
    "CU":  ("recall", "上调"),
    "SE":  ("recall", "上调"),
    "DES": ("dfa", "DFA"),
    "REL": ("released", "释出"),
    "OUT": ("outright", "Outright 下放"),
    "OPT": ("option", "下放小联盟"),
    "DFA": ("fa", "宣布自由球员"),
}
DEPART_CATS = {"dfa", "released", "outright"}
JOIN_CATS = {"signed", "recall"}


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
    players = {}
    for grp in ("hitting", "pitching"):
        j = api_get("/stats", {"stats": "season", "group": grp, "playerPool": "ALL",
                               "teamId": 119, "season": SEASON, "limit": 200})
        splits = ((j.get("stats") or [{}])[0].get("splits")) or []
        for sp in splits:
            team = sp.get("team") or {}
            if team and team.get("id") != 119:
                continue  # 防御：只留道奇段
            person = sp.get("player") or {}
            stat = sp.get("stat") or {}
            pos = (sp.get("position") or {}).get("abbreviation") or "?"
            pid = person.get("id")
            p = players.setdefault(pid, {"id": pid, "name": person.get("fullName"),
                                         "pos": pos, "g": 0, "bat": None, "pit": None})
            p["g"] = max(p["g"], int(stat.get("gamesPlayed") or 0))
            if grp == "hitting" and int(stat.get("atBats") or 0) > 0:
                p["bat"] = {"avg": stat.get("avg"), "hr": stat.get("homeRuns"),
                            "rbi": stat.get("rbi"), "ops": stat.get("ops"),
                            "sb": stat.get("stolenBases"), "hits": stat.get("hits")}
            if grp == "pitching" and (stat.get("inningsPitched") or "0") != "0":
                p["pit"] = {"w": stat.get("wins"), "l": stat.get("losses"),
                            "era": stat.get("era"), "so": stat.get("strikeOuts"),
                            "sv": stat.get("saves"), "ip": stat.get("inningsPitched")}
            if grp == "pitching" and not p["bat"]:
                p["pos"] = "P"
    return list(players.values())


def fetch_moves():
    j = api_get("/transactions", {"teamId": 119, "startDate": "2025-03-01",
                                  "endDate": CUTOFF})
    by_player = {}
    for tx in j.get("transactions") or []:
        person = tx.get("person") or {}
        pid = person.get("id")
        if not pid:
            continue
        cat, label = TYPE_MAP.get(tx.get("typeCode"), (None, None))
        if not cat:
            continue
        by_player.setdefault(pid, []).append({
            "category": cat, "label": label,
            "date": tx.get("date") or "",
            "toLad": (tx.get("toTeam") or {}).get("name") == DODGERS,
            "fromLad": (tx.get("fromTeam") or {}).get("name") == DODGERS,
        })
    for txs in by_player.values():
        txs.sort(key=lambda x: x["date"])
    return by_player


def player_timeline(txs):
    joined = None
    departed = None
    moves = []
    for tx in txs or []:
        cat, label, d = tx["category"], tx["label"], tx["date"]
        if cat == "trade":
            if tx["toLad"] and not tx["fromLad"]:
                moves.append({"date": d, "text": "交易获得"})
                if d > OPENING and not joined:
                    joined = f"交易获得 {fmt_date(d)}"
            elif tx["fromLad"] and not tx["toLad"]:
                moves.append({"date": d, "text": "交易离队"})
                departed = f"交易离队 {fmt_date(d)}"
        elif cat in JOIN_CATS and tx["toLad"] and not tx["fromLad"]:
            moves.append({"date": d, "text": label})
            if d > OPENING and not joined:
                joined = f"{label} {fmt_date(d)}"
        # DES/REL 的 raw 数据是 fromTeam=None、toTeam=LAD（球队动作格式），OUT 是 LAD→小联盟。
        # 查询已按 teamId=119 限定，这三类一律视为道奇阵容动作 → 离队。
        elif cat in DEPART_CATS:
            moves.append({"date": d, "text": label})
            departed = f"{label} {fmt_date(d)}"
        elif cat == "option" and tx["fromLad"]:
            moves.append({"date": d, "text": label})
        # 宣布自由球员（合同到期跳出，11/2 一批老将）→ 离队
        elif cat == "fa":
            moves.append({"date": d, "text": label})
            departed = f"{label} {fmt_date(d)}"
        # CLW 被别队认领走（fromLad 且 toLad=False）
        elif cat == "signed" and tx["fromLad"] and not tx["toLad"]:
            moves.append({"date": d, "text": f"Waiver 离队"})
            departed = f"Waiver 离队 {fmt_date(d)}"
    return joined, departed, moves


def main():
    print(f"[sr-2025] 抓取 2025 历年阵容快照 {datetime.now():%Y-%m-%d %H:%M}", flush=True)
    players = fetch_appearances()
    print(f"[sr-2025] 出场球员 {len(players)} 人", flush=True)
    moves_map = fetch_moves()
    print(f"[sr-2025] 涉及交易记录球员 {len(moves_map)} 人", flush=True)

    rows = []
    for p in players:
        joined, departed, moves = player_timeline(moves_map.get(p["id"]))
        if departed:
            status, status_cn = "departed", departed.split()[0]
        else:
            status, status_cn = "a", "活跃"
        rows.append({
            **p, "status": status, "statusCn": status_cn,
            "joined": joined,
            "departed": departed,
            "moves": [m for m in moves if m["text"] in
                      ("交易获得", "交易离队", "签约", "认领", "上调", "DFA", "释出",
                       "Outright 下放", "Waiver 离队", "宣布自由球员")][-4:],
        })
    rows.sort(key=lambda r: -r["g"])

    summary = {
        "total": len(rows),
        "current": sum(1 for r in rows if r["status"] == "a"),
        "il": 0, "minors": 0,
        "departed": sum(1 for r in rows if r["status"] == "departed"),
        "joinedMidseason": sum(1 for r in rows if r["joined"]),
    }
    data = {"generatedAt": datetime.now().isoformat(), "season": SEASON,
            "summary": summary, "players": rows}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[sr-2025] 已写入 {OUT}", flush=True)
    print(f"[sr-2025] summary: {summary}", flush=True)
    # 抽样打印
    for r in rows[:3]:
        print("  ", r["name"], r["pos"], r["g"], r["status"], r["joined"] or "", r["departed"] or "")
    dep = [r for r in rows if r["status"] == "departed"]
    print(f"[sr-2025] 离队 {len(dep)} 人:", ", ".join(x["name"] for x in dep[:20]))


if __name__ == "__main__":
    main()
