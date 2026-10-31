#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mechanical data refresh for old-style reports.

用法: python apply-data-update.py <slug> <spec.json>
spec: {"cards": {"出赛": "149", ...}, "row2026": ["149", ".252", ...], "note": "季后赛版"}
- cards: 按 stat-label 精确替换 stat-card 数值
- row2026: 替换对比表中 2026 整行单元格（按顺序，None 表示保留原值）
- footer 日期统一改为 2026-10-17，并标注最终数据
"""
import io
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

slug = sys.argv[1]
spec = json.load(io.open(sys.argv[2], encoding="utf-8"))

path = rf"D:\baseball\report\{slug}\{slug}-scouting-report.html"
t = io.open(path, encoding="utf-8").read()

# 1) stat cards
for label, new_val in spec.get("cards", {}).items():
    pat = re.compile(r'(<span class="stat-value"[^>]*>)([^<]*)(</span>\s*<div class="stat-label">' + re.escape(label) + r"</div>)")
    t, n = pat.subn(lambda m: m.group(1) + new_val + m.group(3), t)
    if n != 1:
        print(f"  WARN card '{label}': {n} replacements")

# 2) 2026 comparison row
row = spec.get("row2026")
if row:
    m = re.search(r"(<tr>\s*<td[^>]*>2026</td>)(.*?)(</tr>)", t, re.S)
    if not m:
        print("  WARN: 2026 row not found")
    else:
        cells = re.findall(r"<td[^>]*>.*?</td>", m.group(2), re.S)
        if len(cells) != len(row):
            print(f"  WARN: row has {len(cells)} cells, spec has {len(row)}")
        else:
            new_cells = []
            for old_cell, new_val in zip(cells, row):
                if new_val is None:
                    new_cells.append(old_cell)
                else:
                    cls = re.search(r'class="[^"]*"', old_cell)
                    cls_attr = f' {cls.group(0)}' if cls else ""
                    new_cells.append(f"<td{cls_attr}>{new_val}</td>")
            t = t[: m.start()] + m.group(1) + "\n " + "\n ".join(new_cells) + "\n " + m.group(3) + t[m.end():]

# 3) footer
t = re.sub(r"报告生成时间：\d{4}-\d{2}-\d{2} \| 数据截止日期：\d{4}-\d{2}-\d{2}",
           "报告生成时间：2026-10-17 | 数据截止日期：2026-10-17（常规赛+季后赛最终数据）", t)
# 有些 footer 只有生成时间
t = re.sub(r"报告生成时间：\d{4}-\d{2}-\d{2}(?! \| 数据截止)",
           "报告生成时间：2026-10-17 | 数据截止日期：2026-10-17（常规赛+季后赛最终数据）", t)

io.open(path, "w", encoding="utf-8").write(t)
print("data updated:", slug)
