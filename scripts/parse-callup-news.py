#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 callup 新闻 HTML 提取正文"""
import re
import html as htmllib
import sys

sys.stdout.reconfigure(encoding="utf-8")
t = open(r"D:\baseball\data\probe-callup-news.txt", encoding="utf-8", errors="ignore").read()

# mlb.com 文章页：找 headline + body 结构
i = t.find("josue-de-paula-top-prospect-called-up-dodgers")
print("first ref @", i)
# 找 Article 类型的 JSON 块
for m in re.finditer(r'"headline":"([^"]*[Dd]e [Pp]aula[^"]*)"', t):
    print("HEADLINE:", htmllib.unescape(m.group(1)))

# body 字段
bodies = re.findall(r'"body":"(.*?)","contributor"', t, re.S)
if not bodies:
    bodies = re.findall(r'"body":"(.*?)","syndicatable"', t, re.S)
for b in bodies[:1]:
    b = htmllib.unescape(b)
    b = b.replace("\\n", " ").replace("\\t", " ")
    b = re.sub(r"<[^>]+>", " ", b)
    b = re.sub(r"\s+", " ", b)
    print("BODY:", b[:2500])
