#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

root = Path(r"D:\baseball\report")
for d in sorted(p for p in root.iterdir() if p.is_dir() and p.name != "__pycache__")[:60]:
    pngs = sorted(p.name for p in d.glob("*.png"))
    md = d / f"{d.name}-scouting-report.md"
    html = d / f"{d.name}-scouting-report.html"
    md_len = len(md.read_text(encoding="utf-8")) if md.exists() else 0
    has_bg = False
    if md.exists():
        has_bg = "背景故事" in md.read_text(encoding="utf-8")
    print(f"{d.name:<24} md={md_len:>6} bg={has_bg!s:<5} pngs={pngs}")
