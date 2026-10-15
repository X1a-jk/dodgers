#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补抓 De Paula 2023/2024 小联盟赛季数据 + 官方 callup 新闻"""
import json
import time
import requests
import re
import html as htmllib
import sys

sys.stdout.reconfigure(encoding="utf-8")
PID = 800543
API = "https://statsapi.mlb.com/api/v1"
OUT = r"D:\baseball\data\de-paula-raw.json"

def get(url, params=None, timeout=30, retries=3):
    for i in range(retries):
        try:
            r = requests.get(url, params=params, timeout=timeout)
            r.raise_for_status()
            return r.json() if "api/v1" in url else r.text
        except Exception as e:
            print(f"  [retry {i+1}] {url[:60]}: {type(e).__name__}", flush=True)
            time.sleep(2 * (i + 1))
    return {} if "api/v1" in url else ""

data = json.load(open(OUT, encoding="utf-8"))
existing = {(x["year"], x["team"], x["group"]) for x in data["season_stats"]}

# 2023/2024 可能的球队组合
QUERIES = [
    (2023, 678, 16, "ACL Dodgers"),
    (2023, 526, 13, "Rancho Cucamonga"),
    (2024, 526, 13, "Rancho Cucamonga"),
    (2024, 456, 13, "Great Lakes"),
]
for yr, tid, sid, tname in QUERIES:
    for grp in ["hitting"]:
        j = get(f"{API}/stats", {"stats": "season", "group": grp, "teamId": tid,
                                 "sportId": sid, "season": yr, "limit": 300})
        for st in j.get("stats", []):
            for sp in st.get("splits", []):
                if (sp.get("player") or {}).get("id") == PID:
                    team = (sp.get("team") or {}).get("name")
                    if (yr, team, grp) in existing:
                        continue
                    data["season_stats"].append({
                        "year": yr, "group": grp, "team": team,
                        "league": st.get("league", {}).get("name"),
                        "stat": sp["stat"],
                    })
                    print(f"FOUND {yr} {team}: {sp['stat'].get('avg')}/{sp['stat'].get('obp')}/{sp['stat'].get('slg')} "
                          f"G{sp['stat'].get('gamesPlayed')} HR{sp['stat'].get('homeRuns')} SB{sp['stat'].get('stolenBases')}")

json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("[OK] season data saved")

# callup 新闻
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
txt = get("https://www.mlb.com/news/josue-de-paula-top-prospect-called-up-dodgers", timeout=30)
if txt:
    open(r"D:\baseball\data\probe-callup-news.txt", "w", encoding="utf-8", errors="ignore").write(txt)
    # 提取正文
    m = re.findall(r'"body":"(.*?)","', txt, re.S)
    if m:
        body = htmllib.unescape(m[0]).encode().decode("unicode_escape", errors="ignore")
        body = re.sub(r"<[^>]+>", " ", body)
        body = re.sub(r"\\[nt]", " ", body)
        body = re.sub(r"\s+", " ", body)
        print("NEWS BODY:", body[:1500])
    else:
        print("news fetched, len", len(txt), "no body match")
