#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Copy postseason participants' report dirs to seasons\\2026\\players-postseason\\"""
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


ps = json.load(io.open(r"D:\baseball\data\ps-postseason-final.json", encoding="utf-8"))
src = Path("D:/baseball/report")
dst = Path("D:/baseball/seasons/2026/players-postseason")
dst.mkdir(parents=True, exist_ok=True)

copied = 0
for e in ps["participants"]:
    s, d = src / slugify(e["name"]), dst / slugify(e["name"])
    if not s.exists():
        print("MISSING:", e["name"])
        continue
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(s, d)
    copied += 1
print("copied:", copied)
