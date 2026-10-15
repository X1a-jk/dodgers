#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提取 De Paula 全部年度 bio 与评分 + Top100 排名"""
import re
import html
import sys

sys.stdout.reconfigure(encoding="utf-8")
t = html.unescape(open(r"D:\baseball\data\probe-mlb-prospect-page.txt", encoding="utf-8", errors="ignore").read())

# 找到 rank:1 的 De Paula 段落（Person:800543）
i = t.find('"rank":1,"playerEntity"')
seg = t[i:i + 30000]

bios = re.findall(r'"contentText":"(.*?)","contentTitle":"(\d{4})"', seg, re.S)
for content, year in bios:
    clean = html.unescape(content)
    clean = re.sub(r"<[^>]+>", " ", clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    grades = re.search(r"Scouting grades:\s*(.*?)(?:</|$)", clean)
    print(f"=== {year} ===")
    if grades:
        print("GRADES:", grades.group(1)[:120])
    # 只打印前 700 字
    print(clean[:800])
    print()

# Top 100 排名（页面上可能有 overall rank 字段）
for m in re.finditer(r'"player":\{"__ref":"Person:800543"\}', t):
    s = t[max(0, m.start() - 2000):m.start()]
    r = re.findall(r'"rank":(\d+)', s)
    if r:
        print("context ranks near person ref:", r[-3:])
