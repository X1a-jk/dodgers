# -*- coding: utf-8 -*-
"""临时查看工具: python _peek.py <slug> [section]"""
import io, re, sys
slug = sys.argv[1]
t = io.open(rf'D:\baseball\report\{slug}\{slug}-scouting-report.html', encoding='utf-8').read()
print('LEN', len(t))
for m in re.finditer(r'<h2>(.*?)</h2>', t):
    print('H2:', m.group(1))
print('IMGS:', re.findall(r'src="([^"]+\.png)"', t))
if len(sys.argv) > 2:
    i = t.find(sys.argv[2])
    print(re.sub(r'\s+', ' ', t[i:i+1500]) if i >= 0 else 'NOT FOUND: ' + sys.argv[2])
