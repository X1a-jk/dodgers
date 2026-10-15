#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
道奇 Pipeline Top 30 新秀榜抓取。
数据源：mlb.com/prospects/dodgers（getPlayerRankingsFromSelection JSON，需浏览器 UA 绕 403）。
输出 D:\\baseball\\data\\prospects.json
"""
import json
import re
import html as htmllib
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
URL = "https://www.mlb.com/prospects/dodgers"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
OUT = Path(r"D:\baseball\data\prospects.json")
RAW = Path(r"D:\baseball\data\prospects-page-raw.txt")


def fetch():
    for i in range(4):
        try:
            r = requests.get(URL, headers=UA, timeout=40)
            if r.status_code == 200 and len(r.text) > 100000:
                RAW.write_text(r.text, encoding="utf-8", errors="ignore")
                return r.text
            print(f"  [retry {i+1}] status={r.status_code} len={len(r.text)}", flush=True)
        except Exception as e:
            print(f"  [retry {i+1}] {type(e).__name__}", flush=True)
        time.sleep(2 * (i + 1))
    return None


def parse(t):
    t = htmllib.unescape(t)
    i = t.find("getPlayerRankingsFromSelection")
    if i < 0:
        return []
    seg = t[i:i + 400000]

    # 1) 全局 Person 缓存：ref id -> fullName / useName
    person_map = {}
    for m in re.finditer(r'"Person:(\d+)":\{"__typename":"Person"', t):
        pid = m.group(1)
        body = t[m.start():m.start() + 4000]
        um = re.search(r'"useName":"([^"]+)"', body)
        ul = re.search(r'"useLastName":"([^"]+)"', body)
        if um and pid not in person_map:
            person_map[pid] = f"{um.group(1)} {ul.group(1) if ul else ''}".strip()

    players = []
    entries = re.split(r'"rank":(\d+),', seg)[1:]
    for k in range(0, min(len(entries), 60), 2):
        try:
            rank = int(entries[k])
        except ValueError:
            continue
        body = entries[k + 1]
        if rank > 30:
            break
        m_ref = re.search(r'"player":\{"__ref":"Person:(\d+)"\}', body)
        m_pos = re.search(r'"position":"([^"]+)"', body)
        m_eta = re.search(r'"eta":"([^"]+)"', body)
        pid = m_ref.group(1) if m_ref else None
        # 最新一年 bio 的评分行（条目按年份升序，取最后一个）
        grades_lines = re.findall(r'Scouting grades:</strong>\s*([A-Za-z: 0-9|]+)', body)
        latest = grades_lines[-1].strip() if grades_lines else None
        g = {}
        overall = None
        if latest:
            for k2, v in re.findall(r'(Hit|Power|Run|Arm|Field|Fastball|Curveball|Slider|Changeup|Control|Cutter|Sweeper|Overall):\s*(\d+)', latest):
                g[k2] = int(v)
            overall = g.pop("Overall", None)
        players.append({
            "rank": rank,
            "name": person_map.get(pid, "?"),
            "playerId": int(pid) if pid else None,
            "position": m_pos.group(1) if m_pos else "?",
            "eta": m_eta.group(1) if m_eta else None,
            "grades": g or None,
            "overall": overall,
        })
    return players


def main():
    t = fetch()
    if not t:
        print("[FAIL] fetch failed")
        sys.exit(1)
    players = parse(t)
    if not players:
        print("[FAIL] parse failed")
        sys.exit(1)

    data = {
        "generatedAt": datetime.now().isoformat(),
        "source": "MLB Pipeline (mlb.com/prospects/dodgers)",
        "teamRankings": players,
    }
    bak = OUT.with_suffix(".json.bak")
    if OUT.exists():
        bak.write_text(OUT.read_text(encoding="utf-8"), encoding="utf-8")
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] {OUT} ({len(players)} players)")
    for p in players:
        print(f"  #{p['rank']:>2} {p['name']:<28} {p['position']:<6} ETA {p['eta']} OV{p['overall']} {p['grades']}")


if __name__ == "__main__":
    main()
