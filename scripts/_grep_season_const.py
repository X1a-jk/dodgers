# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
for name in ('daily-report.py', 'build-dodgers-dashboard.py', 'generate-missing-reports.py'):
    p = rf'D:\baseball\scripts\{name}'
    t = io.open(p, encoding='utf-8').read()
    for m in re.finditer(r'[^\n]*SEASON\s*=\s*2026[^\n]*|[^\n]*"season": 2026[^\n]*|[^\n]*season=2026[^\n]*', t):
        print(name, '|', m.group(0).strip()[:110])
