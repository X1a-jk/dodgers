#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tick one player in PLAYER-REPORTS-PLAN.md: python tick-one.py \"Kyle Tucker\""""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

name = sys.argv[1]
PLAN = r"D:\baseball\PLAYER-REPORTS-PLAN.md"
t = io.open(PLAN, encoding="utf-8").read()

pat = re.compile(r"\| \[ \] \| " + re.escape(name) + r" \|[^\n]*\| ([^|]+) \|")
m = pat.search(t)
if not m:
    print("row not found or already ticked:", name)
    sys.exit(1)
new_row = m.group(0).replace("| [ ] |", "| [x] |", 1)
new_row = re.sub(r"\| [^|]+ \|$", "| ✅ 10-17 旧版更新 |", new_row)
t = t[: m.start()] + new_row + t[m.end():]
io.open(PLAN, "w", encoding="utf-8").write(t)

t2 = io.open(PLAN, encoding="utf-8").read()
print("ticked:", name, "| total [x]:", t2.count("| [x] "))
