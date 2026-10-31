#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量修复投手 season_comparison 雷达图 K/9=0 问题 (2026-10-31)。

bug: generate-missing-reports.py 用了不存在的字段 strikeOutsPer9Inn /
basesOnBallsPer9Inn（正确为 strikeoutsPer9Inn / walksPer9Inn），导致
K/9 顶点恒为 20（贴底看似 0）、BB/9 恒为 80。

本脚本只对三个封存批次里的投手重绘 *_season_comparison.png：
- 不动封面（旧版封面风格必须保留，绝不重绘）
- 不动评分雷达（overall_grades 与 K9 无关）
"""
import importlib.util
import io
import json
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

_spec = importlib.util.spec_from_file_location(
    "gm", r"D:\baseball\scripts\generate-missing-reports.py")
gm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gm)

FINAL = json.load(io.open(r"D:\baseball\data\final-stats.json", encoding="utf-8"))
ROSTER = json.load(io.open(r"D:\baseball\data\season-roster.json", encoding="utf-8"))
PS = json.load(io.open(r"D:\baseball\data\ps-postseason-final.json", encoding="utf-8"))

BATCHES = [
    Path(r"D:\baseball\seasons\2026\players"),
    Path(r"D:\baseball\seasons\2026\players-regular"),
    Path(r"D:\baseball\seasons\2026\players-postseason"),
]

# slug -> (pid, pos) 来自赛季名单；slug -> ps_entry 来自季后赛参与者
roster_by_slug = {}
for r in ROSTER["players"]:
    roster_by_slug[gm.slugify(r["name"])] = r
ps_by_slug = {}
for e in PS["participants"]:
    ps_by_slug[gm.slugify(e["name"])] = e


def fetch_2025_individual(pid):
    """2025 不在道奇数据里的，抓该球员 2025 全年数据（带重试）。"""
    url = (f"https://statsapi.mlb.com/api/v1/people/{pid}/stats"
           f"?stats=season&group=hitting,pitching&season=2025")
    last = None
    for attempt in range(6):
        try:
            d = gm.fetch_json(url)
            out = {"hitting": {}, "pitching": {}}
            for st in d.get("stats", []):
                grp = st.get("group", {}).get("displayName", "")
                for split in st.get("splits", []):
                    if grp == "Hitting":
                        out["hitting"] = split.get("stat", {})
                    elif grp == "Pitching":
                        out["pitching"] = split.get("stat", {})
            return out
        except Exception as ex:
            last = ex
            wait = 2 ** attempt
            print(f"    [retry {attempt + 1}/6] {type(ex).__name__}: {ex}", flush=True)
            time.sleep(wait)
    print(f"    !! 2025 individual fetch failed: {last}")
    return {"hitting": {}, "pitching": {}}


fixed, skipped, failed = [], [], []
for batch in BATCHES:
    for player_dir in sorted(batch.iterdir()):
        if not player_dir.is_dir():
            continue
        slug = player_dir.name
        htmls = list(player_dir.glob("*-scouting-report.html"))
        if not htmls:
            continue
        html = htmls[0].read_text(encoding="utf-8")

        r = roster_by_slug.get(slug)
        e = ps_by_slug.get(slug)
        pid = (r or {}).get("id") or (e or {}).get("id")
        if pid is None:
            skipped.append((batch.name, slug, "no pid"))
            continue
        pos = ((r or {}).get("pos") or "").upper()
        is_pitcher = pos in ("P", "SP", "RP", "CL") or (
            e and e["pit"]["outs"] > 0 and e["bat"]["plateAppearances"] == 0)
        if not is_pitcher:
            skipped.append((batch.name, slug, "not pitcher"))
            continue

        s26 = {"hitting": FINAL["hitting_2026"].get(str(pid), {}),
               "pitching": FINAL["pitching_2026"].get(str(pid), {})}
        s25 = {"hitting": FINAL["hitting_2025"].get(str(pid), {}),
               "pitching": FINAL["pitching_2025"].get(str(pid), {})}
        if not s25["hitting"] and not s25["pitching"]:
            s25 = fetch_2025_individual(pid)

        info = gm.fetch_player(pid)
        try:
            gm.generate_season_comparison(player_dir, info["fullName"], s25, s26, True)
        except Exception as ex:
            failed.append((batch.name, slug, repr(ex)))
            continue

        # 同步到 HTML 引用的所有文件名（lastname_* / fullslug_* 两种命名）
        src = player_dir / f"{gm.slugify(info['fullName'])}_season_comparison.png"
        names = sorted(set(re.findall(r'src="([^"]*_season_comparison\.png)"', html)))
        for name in names:
            dst = player_dir / name
            if dst.name != src.name:
                io.open(dst, "wb").write(io.open(src, "rb").read())
        k9 = s26["pitching"].get("strikeoutsPer9Inn", "?")
        bb9 = s26["pitching"].get("walksPer9Inn", "?")
        fixed.append((batch.name, slug, k9, bb9))
        print(f"  [OK] {batch.name}/{slug}  K/9={k9} BB/9={bb9} refs={len(names)}", flush=True)

print(f"\n==== fixed {len(fixed)}, skipped {len(skipped)}, failed {len(failed)} ====")
for b, s, why in skipped:
    print(f"  skip {b}/{s}: {why}")
for b, s, ex in failed:
    print(f"  FAIL {b}/{s}: {ex}")
