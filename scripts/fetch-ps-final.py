#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch all Dodgers 2026 postseason games, aggregate boxscores into per-player totals.

Outputs:
  data\ps-postseason-final.json   原始聚合（含每场合计与球员累计）
  data\ps-roster-snapshot.json    赛季名单同构快照（给 build-dodgers-dashboard.py 的 DASH_ROSTER_JSON 用）
"""
import io
import json
import sys
import time
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# 2026-10-17: 绕过失效系统代理 + DNS 缓存（同 build-dodgers-dashboard.py 的修法）
urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler({})))
import socket as _socket
_real_getaddrinfo = _socket.getaddrinfo
_DNS_CACHE = {}
def _cached_getaddrinfo(host, port, *a, **kw):
    key = (host, port)
    if key not in _DNS_CACHE:
        _DNS_CACHE[key] = _real_getaddrinfo(host, port, *a, **kw)
    return _DNS_CACHE[key]
_socket.getaddrinfo = _cached_getaddrinfo


def fetch_json(url: str) -> dict:
    last_err = None
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            last_err = e
            print(f"  [retry {attempt + 1}/5] {type(e).__name__}: {e}", flush=True)
            time.sleep(3 * (attempt + 1))
    raise last_err


DATA = Path("D:/baseball/data")


def ip_to_outs(ip):
    if ip in (None, ""):
        return 0
    s = str(ip)
    if "." in s:
        whole, frac = s.split(".")
        return int(whole) * 3 + int(frac)
    return int(s) * 3


def outs_to_ip(outs):
    return f"{outs // 3}.{outs % 3}"


B_KEYS = ["plateAppearances", "atBats", "runs", "hits", "doubles", "triples", "homeRuns",
          "rbi", "baseOnBalls", "strikeOuts", "stolenBases", "sacrificeFlies", "hitByPitch"]
P_KEYS = ["hits", "runs", "earnedRuns", "baseOnBalls", "strikeOuts", "homeRuns", "wins",
          "losses", "saves", "gamesStarted"]

ZERO_B = {k: 0 for k in B_KEYS}
ZERO_P = {k: 0 for k in P_KEYS}
ZERO_P["outs"] = 0


def main():
    sched = fetch_json("https://statsapi.mlb.com/api/v1/schedule?teamId=119&sportId=1"
                       "&gameTypes=F,D,L,W&startDate=2026-09-28&endDate=2026-11-05"
                       "&hydrate=team,linescore")
    games = []
    for d in sched.get("dates", []):
        for g in d.get("games", []):
            if g.get("status", {}).get("abstractGameState") == "Final":
                games.append({
                    "pk": g["gamePk"],
                    "date": g.get("gameDate", "")[:10],
                    "desc": g.get("seriesDescription", "") or g.get("description", ""),
                    "away": g["teams"]["away"]["team"]["name"],
                    "home": g["teams"]["home"]["team"]["name"],
                    "score": f"{g['teams']['away'].get('score', '?')} - {g['teams']['home'].get('score', '?')}",
                })
    print(f"found {len(games)} final postseason games", flush=True)

    participants = {}  # pid -> {id,name,pos,games,bat:{...},pit:{...}}
    for i, g in enumerate(games, 1):
        box = fetch_json(f"https://statsapi.mlb.com/api/v1/game/{g['pk']}/boxscore")
        for side in ("away", "home"):
            team = box["teams"][side]
            if team["team"]["id"] != 119:
                continue
            for key, p in team.get("players", {}).items():
                sb = p.get("stats", {}).get("batting", {}) or {}
                sp = p.get("stats", {}).get("pitching", {}) or {}
                pa = sb.get("plateAppearances", 0) or 0
                ip_outs = ip_to_outs(sp.get("inningsPitched"))
                played = pa > 0 or ip_outs > 0 or bool(p.get("batOrder"))
                if not played:
                    continue
                pid = p["person"]["id"]
                name = p["person"]["fullName"]
                pos = (p.get("position") or {}).get("abbreviation", "")
                e = participants.setdefault(pid, {
                    "id": pid, "name": name, "pos": pos, "games": 0,
                    "bat": dict(ZERO_B), "pit": dict(ZERO_P), "gs": 0,
                })
                e["games"] += 1
                if pa > 0:
                    for k in B_KEYS:
                        e["bat"][k] += int(sb.get(k, 0) or 0)
                if ip_outs > 0:
                    e["pit"]["outs"] += ip_outs
                    for k in P_KEYS:
                        e["pit"][k] += int(sp.get(k, 0) or 0)
                    e["gs"] += 1 if int(sp.get("gamesStarted", 0) or 0) else 0
        print(f"  [{i}/{len(games)}] pk={g['pk']} {g['date']} {g['desc']} aggregated", flush=True)

    # 计算率值
    for e in participants.values():
        b = e["bat"]
        ab, h, bb, hr, sf = b["atBats"], b["hits"], b["baseOnBalls"], b["hitByPitch"], b["sacrificeFlies"]
        pa_denom = ab + bb + hr + sf
        b["avg"] = f"{h / ab:.3f}" if ab else "-"
        b["obp"] = f"{(h + bb + hr) / pa_denom:.3f}" if pa_denom else "-"
        tb = h + b["doubles"] + 2 * b["triples"] + 3 * b["homeRuns"]
        b["slg"] = f"{tb / ab:.3f}" if ab else "-"
        try:
            b["ops"] = f"{float(b['obp']) + float(b['slg']):.3f}" if ab else "-"
        except Exception:
            b["ops"] = "-"
        p = e["pit"]
        if p["outs"] > 0:
            ip = p["outs"] / 3
            p["ip"] = outs_to_ip(p["outs"])
            p["era"] = f"{p['earnedRuns'] * 9 / ip:.2f}"
            whip_denom = ip
            p["whip"] = f"{(p['hits'] + p['baseOnBalls']) / whip_denom:.2f}"
            p["k9"] = f"{p['strikeOuts'] * 9 / ip:.1f}"
            p["bb9"] = f"{p['baseOnBalls'] * 9 / ip:.1f}"
        else:
            p["ip"], p["era"], p["whip"], p["k9"], p["bb9"] = "0.0", "-", "-", "-", "-"

    out = {"generatedAt": time.strftime("%Y-%m-%d %H:%M"), "games": games,
           "participants": sorted(participants.values(), key=lambda e: -e["games"])}
    io.open(DATA / "ps-postseason-final.json", "w", encoding="utf-8").write(
        json.dumps(out, ensure_ascii=False, indent=1))
    print(f"\nparticipants: {len(participants)}")
    for e in out["participants"]:
        tags = []
        if e["bat"]["plateAppearances"] > 0:
            tags.append("打")
        if e["pit"]["outs"] > 0:
            tags.append("投")
        print(f"  {e['name']:<24} {e['games']}场 {'/'.join(tags)}")

    # 赛季名单同构快照（仪表盘用）
    snap = {"generatedAt": out["generatedAt"], "season": 2026,
            "players": [{
                "id": e["id"], "name": e["name"], "pos": e["pos"], "g": e["games"],
                "bat": e["bat"] if e["bat"]["plateAppearances"] > 0 else None,
                "pit": {"era": e["pit"]["era"], "whip": e["pit"]["whip"],
                        "w": e["pit"]["wins"], "l": e["pit"]["losses"],
                        "so": e["pit"]["strikeOuts"], "ip": e["pit"]["ip"]} if e["pit"]["outs"] > 0 else None,
                "status": "a", "statusCn": "季后赛",
            } for e in out["participants"]]}
    io.open(DATA / "ps-roster-snapshot.json", "w", encoding="utf-8").write(
        json.dumps(snap, ensure_ascii=False, indent=1))
    print("\nsnapshot written: data\\ps-roster-snapshot.json")


if __name__ == "__main__":
    main()
