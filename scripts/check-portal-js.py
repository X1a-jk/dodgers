#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提取 index.html 内嵌 script 并用 node --check 校验"""
import re
import subprocess
import sys
from pathlib import Path

html = Path(r"D:\baseball\index.html").read_text(encoding="utf-8")
scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)
print(f"found {len(scripts)} script blocks")
ok = True
for i, s in enumerate(scripts):
    if not s.strip():
        continue
    tmp = Path(rf"D:\baseball\data\_check_{i}.js")
    tmp.write_text(s, encoding="utf-8")
    r = subprocess.run(["node", "--check", str(tmp)], capture_output=True, text=True)
    if r.returncode != 0:
        ok = False
        print(f"[FAIL] block {i}: {r.stderr[:800]}")
    else:
        print(f"[OK] block {i} ({len(s)} chars)")
    tmp.unlink()
sys.exit(0 if ok else 1)
