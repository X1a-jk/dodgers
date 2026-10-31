#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inspect an old-style report html: stat cards, 2026 table row, h3 sections, footer."""
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

slug = sys.argv[1]
t = io.open(rf"D:\baseball\report\{slug}\{slug}-scouting-report.html", encoding="utf-8").read()

print("=== STAT CARDS ===")
for m in re.finditer(r'<span class="stat-value"[^>]*>([^<]+)</span>\s*<div class="stat-label">([^<]+)</div>', t):
    print("CARD:", m.group(2).strip(), "=", m.group(1))

print("=== 2026 TABLE ROW ===")
m = re.search(r'<td[^>]*>2026</td>(.*?)</tr>', t, re.S)
print(re.sub(r"<[^>]+>", "|", m.group(1)) if m else "not found")

print("=== H3 SECTIONS ===")
for m in re.finditer(r"<h3[^>]*>(.*?)</h3>", t):
    print("H3:", re.sub(r"<[^>]+>", "", m.group(1)).strip())

print("=== FOOTER ===")
m = re.search(r'<div class="footer">(.*?)</div>', t, re.S)
print(re.sub(r"<[^>]+>", " ", m.group(1)).strip() if m else "")

print("=== PROSE WITH NUMBERS (li/p containing digits) ===")
for m in re.finditer(r"<(li|p)>(.*?)</\1>", t, re.S):
    txt = re.sub(r"<[^>]+>", "", m.group(2)).strip()
    if re.search(r"\d", txt) and len(txt) < 220:
        print("-", txt)
