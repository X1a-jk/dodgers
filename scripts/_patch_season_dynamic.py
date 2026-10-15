# -*- coding: utf-8 -*-
"""把生产脚本里写死的赛季年份改为动态年份（新赛季零改动）"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

def patch(path, old, new):
    t = io.open(path, encoding='utf-8').read()
    assert t.count(old) == 1, f'{path}: anchor {t.count(old)}x'
    io.open(path, 'w', encoding='utf-8').write(t.replace(old, new))
    print('ok:', path.split('\\')[-1], '|', old.strip()[:60])

# 1. daily-report.py（每日管线，最重要）
patch(r'D:\baseball\scripts\daily-report.py',
      'data = statsapi.get("team_roster", {"teamId": 119, "rosterType": "40Man", "season": 2026})',
      'data = statsapi.get("team_roster", {"teamId": 119, "rosterType": "40Man", "season": datetime.now().year})')

# 2. 报告生成器
for f in ('build-dodgers-dashboard.py', 'generate-missing-reports.py'):
    p = rf'D:\baseball\scripts\{f}'
    t = io.open(p, encoding='utf-8').read()
    old = 'SEASON = 2026'
    assert t.count(old) == 1, f'{f}: {t.count(old)}x'
    io.open(p, 'w', encoding='utf-8').write(t.replace(old, 'SEASON = datetime.now().year'))
    print('ok:', f)

# generate-missing-reports.py 是否已 import datetime
t = io.open(r'D:\baseball\scripts\generate-missing-reports.py', encoding='utf-8').read()
if 'import datetime' not in t and 'from datetime import' not in t:
    print('[warn] generate-missing-reports.py 缺 datetime import，需补上')
t2 = io.open(r'D:\baseball\scripts\build-dodgers-dashboard.py', encoding='utf-8').read()
if 'import datetime' not in t2 and 'from datetime import' not in t2:
    print('[warn] build-dodgers-dashboard.py 缺 datetime import，需补上')
