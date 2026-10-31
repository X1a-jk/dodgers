# -*- coding: utf-8 -*-
"""Per-player chart update with old-cover protection.
用法: python _update_charts_batch.py slug1 slug2 ...
"""
import shutil
import subprocess
import sys
from pathlib import Path

REPORT = Path(r"D:\baseball\report")
BACKUP = Path(r"D:\baseball\scripts\_cover_backup")
BACKUP.mkdir(exist_ok=True)

for slug in sys.argv[1:]:
    d = REPORT / slug
    covers = sorted(d.glob("*_report_cover.png"))
    if not covers:
        print(slug, "NO COVER FOUND")
        continue
    # backup all covers
    bdir = BACKUP / slug
    bdir.mkdir(exist_ok=True)
    for c in covers:
        shutil.copy2(c, bdir / c.name)
    r = subprocess.run([sys.executable, r"D:\baseball\scripts\update-player-charts.py", slug],
                       capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    # restore all covers
    for c in covers:
        shutil.copy2(bdir / c.name, d / c.name)
    print("=" * 10, slug, "rc=", r.returncode)
    print(out.strip()[-600:])
