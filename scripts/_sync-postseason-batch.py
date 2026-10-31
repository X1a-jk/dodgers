#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync the 25 postseason players' live report dirs to seasons\\2026\\players-postseason\\"""
import io, json, re, shutil, sys, unicodedata
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

copied, missing = 0, []
for p in ps["participants"]:
    name = p.get("name") or p.get("fullName")
    slug = slugify(name)
    s, d = src / slug, dst / slug
    if not s.exists():
        missing.append(name)
        continue
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(s, d)
    copied += 1

print("copied:", copied, "| missing:", missing)
