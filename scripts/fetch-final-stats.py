#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch full 2025/2026 team season stats (all counting stats) for report updates."""
import importlib.util
import io
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

_spec = importlib.util.spec_from_file_location(
    "gm", r"D:\baseball\scripts\generate-missing-reports.py")
gm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gm)

out = {}
for group in ("hitting", "pitching"):
    for season in (2025, 2026):
        stats = gm.get_team_stats(group, season)
        out[f"{group}_{season}"] = {str(k): v for k, v in stats.items()}
        print(f"{group} {season}: {len(stats)} players", flush=True)

io.open(r"D:\baseball\data\final-stats.json", "w", encoding="utf-8").write(
    json.dumps(out, ensure_ascii=False))
print("written: data\\final-stats.json")
