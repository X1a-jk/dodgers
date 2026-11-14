#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一次性：2025 季后赛快照 → seasons\\2025\\snapshots\\postseason.json（复用 fetch-postseason.py 全部逻辑）"""
import importlib.util
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location(
    "fetch_postseason", r"D:\baseball\scripts\fetch-postseason.py")
fp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fp)

fp.SEASON = 2025
fp.OUTPUT_FILE = Path(r"D:\baseball\seasons\2025\snapshots\postseason.json")
fp.main()
