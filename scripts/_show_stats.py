#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print final 2026 (and 2025 if Dodger) stat line for a player slug."""
import importlib.util
import io
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

_spec = importlib.util.spec_from_file_location(
    "gm", r"D:\baseball\scripts\generate-missing-reports.py")
gm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gm)

slug = sys.argv[1]
ROSTER = json.load(io.open(r"D:\baseball\data\season-roster.json", encoding="utf-8"))
FINAL = json.load(io.open(r"D:\baseball\data\final-stats.json", encoding="utf-8"))
pid = None
for r in ROSTER["players"]:
    if gm.slugify(r["name"]) == slug:
        pid = r["id"]
        break
if pid is None:
    print("not found")
    sys.exit(1)
h26 = FINAL["hitting_2026"].get(str(pid), {})
p26 = FINAL["pitching_2026"].get(str(pid), {})
h25 = FINAL["hitting_2025"].get(str(pid), {})
p25 = FINAL["pitching_2025"].get(str(pid), {})
print("2026 hitting:", json.dumps(h26, ensure_ascii=False))
print("2026 pitching:", json.dumps(p26, ensure_ascii=False))
if h25 or p25:
    print("2025(dodgers) hitting:", json.dumps(h25, ensure_ascii=False))
    print("2025(dodgers) pitching:", json.dumps(p25, ensure_ascii=False))
else:
    print("2025: NOT in Dodgers stats (need individual fetch)")
