#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify all 53 regular-season player reports: completeness + final data."""
import io
import json
import re
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
root = Path("D:/baseball/report")
bad = []
for r in roster:
    slug = slugify(r["name"])
    d = root / slug
    files = list(d.rglob("*")) if d.exists() else []
    md = [f for f in files if f.suffix == ".md"]
    html = [f for f in files if f.suffix == ".html"]
    png = [f for f in files if f.suffix == ".png"]
    problems = []
    if not md or not html or len(png) < 3:
        problems.append("incomplete files")
    if md:
        t = md[0].read_text(encoding="utf-8")
        # 最终数据版判定：md 生成日期为 2026-10-17 及以后的任一收官批次（17/18/24/26/27/28）
        if not any(d in t for d in ("2026-10-17","2026-10-18","2026-10-24","2026-10-26","2026-10-27","2026-10-28")):
            problems.append("not final-data version")
        if t.count("?") > 0:
            problems.append("has %d ? chars" % t.count("?"))
        bat = r.get("bat") or {}
        pit = r.get("pit") or {}
        if bat or r.get("g"):
            # 只对"首数字列=G"的表校验；GS 列首的表（如 Sheehan）跳过
            hdr = re.search(r"\n\| ([^|\n]+)\|[^\n]*\n\|[-\s|]+\n(?:\| [^\n]*\n)*?\| 2026 \| (\d+) \|", t)
            if hdr and hdr.group(1).strip() == "G" and int(hdr.group(2)) != r.get("g"):
                problems.append("G mismatch: report %s vs roster %s" % (hdr.group(2), r.get("g")))
        if pit and not bat:
            m = re.search(r"\| 2026 \| \d+ \| \d+ \| \d+-\d+ \| ([\d.]+) \|", t)
            if m and pit.get("era") and abs(float(m.group(1)) - float(pit["era"])) > 0.011:
                problems.append("ERA mismatch: %s vs %s" % (m.group(1), pit["era"]))
    print(("OK " if not problems else "BAD"), r["name"], problems if problems else "")
    if problems:
        bad.append((r["name"], problems))

print()
print("total: %d | bad: %d" % (len(roster), len(bad)))
