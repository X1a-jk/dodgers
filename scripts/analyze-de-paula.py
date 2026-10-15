#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""De Paula 数据汇总：fielding + 月度拆分 + 近期状态"""
import json
import collections

d = json.load(open(r"D:\baseball\data\de-paula-raw.json", encoding="utf-8"))
for x in d["season_stats"]:
    if x["group"] == "fielding":
        s = x["stat"]
        print(x["year"], x["team"], "POS", s.get("position"), "G", s.get("gamesPlayed"),
              "GS", s.get("gamesStarted"), "Inn", s.get("innings"), "PO", s.get("putOuts"),
              "A", s.get("assists"), "E", s.get("errors"), "FPCT", s.get("fielding"),
              "OFA", s.get("outfieldAssists"))

gl = d["gamelog_2026"]
print("games total:", len(gl))
mon = collections.defaultdict(lambda: dict(ab=0, h=0, hr=0, rbi=0, bb=0, so=0, sb=0, r=0, g=0))
for g in gl:
    m = g["date"][:7]
    s = mon[m]
    s["g"] += 1; s["ab"] += g["ab"]; s["h"] += g["h"]; s["hr"] += g["hr"]; s["rbi"] += g["rbi"]
    s["bb"] += g["bb"]; s["so"] += g["so"]; s["sb"] += g["sb"]; s["r"] += g["r"]
for m in sorted(mon):
    s = mon[m]
    avg = s["h"] / s["ab"] if s["ab"] else 0
    obp_h = s["h"] + s["bb"]
    obp_pa = s["ab"] + s["bb"]
    obp = obp_h / obp_pa if obp_pa else 0
    print(m, f"G{s['g']} AB{s['ab']} H{s['h']} AVG .{int(avg*1000):03d} OBP~.{int(obp*1000):03d} HR{s['hr']} RBI{s['rbi']} BB{s['bb']} SO{s['so']} SB{s['sb']} R{s['r']}")

# 最近7场 / 最近15场
def span(n):
    xs = gl[-n:]
    ab = sum(g["ab"] for g in xs); h = sum(g["h"] for g in xs)
    hr = sum(g["hr"] for g in xs); rbi = sum(g["rbi"] for g in xs)
    bb = sum(g["bb"] for g in xs); so = sum(g["so"] for g in xs)
    avg = h / ab if ab else 0
    print(f"last{n}: G{len(xs)} {h}/{ab} .{int(avg*1000):03d} HR{hr} RBI{rbi} BB{bb} SO{so}")
span(7); span(15); span(30)
