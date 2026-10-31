# -*- coding: utf-8 -*-
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')
for slug in sys.argv[1:]:
    html = open(rf'D:\baseball\report\{slug}\{slug}-scouting-report.html', encoding='utf-8').read()
    m = re.search(r'<h2>.. 综合评分</h2>(.*?)<h3', html, re.S)
    pairs = re.findall(r'stat-value"[^>]*>(\d+)</span>\s*<div class="stat-label">([^<]+)</div>', m.group(1)) if m else []
    print(slug, len(pairs), pairs)
