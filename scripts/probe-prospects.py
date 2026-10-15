#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""精确探查 Person 定义与 contentText 格式"""
import re
import html as H
import sys

sys.stdout.reconfigure(encoding="utf-8")
t = H.unescape(open(r"D:\baseball\data\prospects-page-raw.txt", encoding="utf-8", errors="ignore").read())

# Person 完整定义（到下一个 ref 键）
m = re.search(r"Person:800543\":\{\"__typename\":\"Person\".{0,2500}?(?=,\\\"Person:|,\s*\"Person:|\})", t)
if not m:
    m = re.search(r"Person:800543\":\{\"__typename\":\"Person\".{0,2500}", t)
body = m.group(0)
# 列出所有键名
keys = re.findall(r"[,\{]\\\"?([a-zA-Z]+)\\\"?:", body)
print("PERSON KEYS:", keys)
for k in ["fullName", "useName", "nameFirstLast", "lastFirstName"]:
    mm = re.search(k + r"\\?\":\\?\"([^\"\\\\]+)", body)
    print(k, "->", mm.group(1) if mm else "N/A")

# contentText 里 Scouting grades 的精确格式
i = t.find("Scouting grades")
print("---RAW CTX---")
print(repr(t[i:i+180]))
