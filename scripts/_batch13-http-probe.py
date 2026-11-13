# -*- coding: utf-8 -*-
"""HTTP 探测：批次 index 全部报告链接 200 检查"""
import re, urllib.request

base = 'http://127.0.0.1:8901/seasons/2025/players/'
html = urllib.request.urlopen(base + 'index.html', timeout=15).read().decode('utf-8')
hrefs = sorted(set(re.findall(r'href="([^"]+/[^"]+-scouting-report\.html)"', html)))
print('links found:', len(hrefs))
bad = []
for h in hrefs:
    try:
        r = urllib.request.urlopen(urllib.request.Request(base + h, method='HEAD'), timeout=10)
        if r.status != 200:
            bad.append((h, r.status))
    except Exception as e:
        bad.append((h, str(e)[:60]))
print('ALL 200' if not bad else 'BAD:')
for b in bad:
    print(' ', b)
