#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenerate cover/comparison/grades charts for one player from final data.

用法: python update-player-charts.py <slug> [--ps]

- 图表文件名自动检测 HTML 里引用的名字（lastname_* 或 fullslug_*）
- 评分雷达复用旧报告综合评分表里的数值，保持图文一致
"""
import importlib.util
import io
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

_spec = importlib.util.spec_from_file_location(
    "gm", r"D:\baseball\scripts\generate-missing-reports.py")
gm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gm)

slug = sys.argv[1]
want_ps = "--ps" in sys.argv

FINAL = json.load(io.open(r"D:\baseball\data\final-stats.json", encoding="utf-8"))
ROSTER = json.load(io.open(r"D:\baseball\data\season-roster.json", encoding="utf-8"))
PS = json.load(io.open(r"D:\baseball\data\ps-postseason-final.json", encoding="utf-8"))

pid = None
pos = ""
for r in ROSTER["players"]:
    if gm.slugify(r["name"]) == slug:
        pid = r["id"]
        pos = (r.get("pos") or "").upper()
        break
ps_entry = None
for e in PS["participants"]:
    if gm.slugify(e["name"]) == slug:
        ps_entry = e
        pid = e["id"]
        break
if pid is None:
    print("player not found:", slug)
    sys.exit(1)

is_pitcher = pos in ("P", "SP", "RP", "CL") or (
    ps_entry and ps_entry["pit"]["outs"] > 0 and ps_entry["bat"]["plateAppearances"] == 0)

s26 = {"hitting": FINAL["hitting_2026"].get(str(pid), {}),
       "pitching": FINAL["pitching_2026"].get(str(pid), {})}
s25 = {"hitting": FINAL["hitting_2025"].get(str(pid), {}),
       "pitching": FINAL["pitching_2025"].get(str(pid), {})}

# 2025 不在道奇队数据的（季中/新加盟），单独抓该球员 2025 全年数据做对比
if not s25["hitting"] and not s25["pitching"]:
    try:
        url = f"https://statsapi.mlb.com/api/v1/people/{pid}/stats?stats=season&group=hitting,pitching&season=2025"
        d = gm.fetch_json(url)
        for st in d.get("stats", []):
            grp = st.get("group", {}).get("displayName", "")
            for split in st.get("splits", []):
                if grp == "Hitting":
                    s25["hitting"] = split.get("stat", {})
                elif grp == "Pitching":
                    s25["pitching"] = split.get("stat", {})
        print("  fetched individual 2025 stats")
    except Exception as ex:
        print("  2025 individual fetch failed:", ex)

player_dir = Path(rf"D:\baseball\report\{slug}")
html = (player_dir / f"{slug}-scouting-report.html").read_text(encoding="utf-8")

# 检测 HTML 引用的图表文件名
def ref_names(kind):
    m = re.findall(rf'src="([^"]*_{kind}\.png)"', html)
    return sorted(set(m))

info = gm.fetch_player(pid)

gm.generate_cover(player_dir, info["fullName"], info, s26 if not want_ps else
                  ({"hitting": s26["hitting"], "pitching": s26["pitching"]}))
for name in ref_names("report_cover"):
    src = player_dir / f"{gm.slugify(info['fullName'])}_report_cover.png"
    dst = player_dir / name
    if dst.name != src.name:
        io.open(dst, "wb").write(io.open(src, "rb").read())

gm.generate_season_comparison(player_dir, info["fullName"], s25, s26, is_pitcher)
for name in ref_names("season_comparison"):
    src = player_dir / f"{gm.slugify(info['fullName'])}_season_comparison.png"
    dst = player_dir / name
    if dst.name != src.name:
        io.open(dst, "wb").write(io.open(src, "rb").read())

# 评分：从旧 HTML 综合评分区读取（stat-card 结构：value + label 成对出现）
grades = {}
m = re.search(r"<h2>📊 综合评分</h2>(.*?)<h3", html, re.S)
if m:
    pairs = re.findall(r'stat-value"[^>]*>(\d+)</span>\s*<div class="stat-label">([^<]+)</div>', m.group(1))
    for val, label in pairs:
        grades[label.strip()] = int(val)
if len(grades) >= 4:
    gm.generate_radar(info["fullName"], list(grades.keys()), list(grades.values()),
                      player_dir / f"{gm.slugify(info['fullName'])}_overall_grades.png",
                      "Overall Grades")
    for name in ref_names("overall_grades"):
        src = player_dir / f"{gm.slugify(info['fullName'])}_overall_grades.png"
        dst = player_dir / name
        if dst.name != src.name:
            io.open(dst, "wb").write(io.open(src, "rb").read())
else:
    print("  (grades table not found, skipped grades chart)")

print("charts updated:", slug)
