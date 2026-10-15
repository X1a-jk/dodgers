# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
for f in ('build-dodgers-dashboard.py', 'generate-missing-reports.py', 'daily-report.py'):
    t = io.open(rf'D:\baseball\scripts\{f}', encoding='utf-8').read()
    head = t[:800]
    has = 'import datetime' in t or 'from datetime import' in t
    print(f, '| datetime imported:', has)
    if not has:
        print('   head:', repr(head[:300]))
