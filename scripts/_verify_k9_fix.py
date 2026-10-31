# -*- coding: utf-8 -*-
"""核对：三个批次里所有投手的 HTML 引用对比图是否都是今天重绘的。"""
import re, io, json, importlib.util, datetime
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "gm", r"D:\baseball\scripts\generate-missing-reports.py")
gm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gm)

ROSTER = json.load(io.open(r"D:\baseball\data\season-roster.json", encoding="utf-8"))
PS = json.load(io.open(r"D:\baseball\data\ps-postseason-final.json", encoding="utf-8"))
roster_by_slug = {gm.slugify(r["name"]): r for r in ROSTER["players"]}
ps_by_slug = {gm.slugify(e["name"]): e for e in PS["participants"]}

today = datetime.datetime(2026, 10, 31).timestamp()
ok, stale_p = [], []
for batch in ['players', 'players-regular', 'players-postseason']:
    for d in sorted(Path(batch).iterdir()):
        if not d.is_dir():
            continue
        htmls = list(d.glob('*-scouting-report.html'))
        if not htmls:
            continue
        r, e = roster_by_slug.get(d.name), ps_by_slug.get(d.name)
        pos = ((r or {}).get("pos") or "").upper()
        is_p = pos in ("P", "SP", "RP", "CL") or (
            e and e["pit"]["outs"] > 0 and e["bat"]["plateAppearances"] == 0)
        if not is_p:
            continue
        html = htmls[0].read_text(encoding="utf-8")
        refs = sorted(set(re.findall(r'src="([^"]*_season_comparison\.png)"', html)))
        fresh = all((d / n).stat().st_mtime >= today for n in refs)
        (ok if fresh else stale_p).append((batch, d.name, refs))

print(f"pitcher charts fresh today: {len(ok)}")
print(f"pitcher charts STALE: {len(stale_p)}")
for b, s, refs in stale_p:
    print("  STALE", b, s, refs)
