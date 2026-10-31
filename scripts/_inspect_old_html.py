#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

t = io.open(r"D:\baseball\report\freddie-freeman\freddie-freeman-scouting-report.html", encoding="utf-8").read()
print("LEN", len(t))
for m in re.finditer(r"<(h1|h2|h3)[^>]*>(.*?)</\1>", t):
    print(m.group(1), "|", re.sub(r"<[^>]+>", "", m.group(2))[:50])
print("---imgs---")
for m in re.finditer(r'<img[^>]*src="([^"]+)"', t):
    print(m.group(1))
print("---style head---")
m = re.search(r"<style>(.*?)</style>", t, re.S)
print(m.group(1)[:600] if m else "no style")
