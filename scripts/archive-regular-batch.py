#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Copy the 53 regular-season report dirs to seasons\\2026\\players-regular\\"""
import io
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def slugify(name):
    n = unicodedata.normalize("NFKD", name)
    a = "".join(c for c in n if unicodedata.category(c) != "Mn")
    a = a.lower().replace(" ", "-").replace("'", "").replace(".", "")
    return re.sub(r"[^a-z0-9-]", "", a)


roster = json.load(io.open(r"D:\baseball\data\season-roster.json", encoding="utf-8"))["players"]
src = Path("D:/baseball/report")
dst = Path("D:/baseball/seasons/2026/players-regular")
dst.mkdir(parents=True, exist_ok=True)

copied, missing = 0, []
for r in roster:
    slug = slugify(r["name"])
    s, d = src / slug, dst / slug
    if not s.exists():
        missing.append(r["name"])
        continue
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(s, d)
    copied += 1

# 报告目录里名单外的额外目录（不封存，只提示）
extras = sorted(p.name for p in src.iterdir()
                if p.is_dir() and p.name not in {slugify(r["name"]) for r in roster}
                and p.name != "__pycache__")
print("copied:", copied, "| missing:", missing)
print("extras left in report\\:", extras)
