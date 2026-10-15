# -*- coding: utf-8 -*-
"""拉取道奇 40 人名单，与最近快照对比，输出变化。"""
import sys, io, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import statsapi

r = statsapi.get('team_roster', {'teamId': 119, 'rosterType': '40Man', 'season': 2026})
items = r.get('roster', [])

out = []
for p in items:
    out.append({
        'id': p['person']['id'],
        'name': p['person']['fullName'],
        'pos': p.get('position', {}).get('abbreviation', '?'),
        'status': p.get('status', {}).get('code', '?'),
        'desc': p.get('status', {}).get('description', ''),
    })

STATUS_MAP = {
    'A': '活跃', 'RM': '小联盟', 'D10': 'IL-10', 'D15': 'IL-15',
    'D60': 'IL-60', 'IL': '伤病名单', 'NRI': 'NRI', 'BRV': '小联盟',
}

def norm(code):
    return STATUS_MAP.get(code, code)

# 输出全量名单
print('===ROSTER=== count=%d' % len(out))
out.sort(key=lambda x: (x['status'], x['pos'], x['name']))
for o in out:
    print('{} | {} | {} | {} | {}'.format(o['id'], o['name'], o['pos'], norm(o['status']), o['desc']))

# 与 dodgers-roster.md 快照对比（解析表格行: | 名字 | 背号 | 状态 | 备注 |）
snap_path = r'D:\baseball\roster\dodgers-roster.md'
prev = {}
if os.path.exists(snap_path):
    with open(snap_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('|') and '---' not in line and '球员' not in line:
                cells = [c.strip() for c in line.strip('|').split('|')]
                if len(cells) >= 3 and cells[0] and cells[0] != '球员':
                    prev[cells[0]] = cells[2]

cur = {o['name']: norm(o['status']) for o in out}
changes = []
for name, st in cur.items():
    if name not in prev:
        changes.append('NEW: {} -> {}'.format(name, st))
    elif prev[name] != st:
        changes.append('CHANGE: {} {} -> {}'.format(name, prev.get(name, '?'), st))
for name in prev:
    if name not in cur:
        changes.append('REMOVED: {}'.format(name))

print('===CHANGES===')
if changes:
    for c in changes:
        print(c)
else:
    print('(no changes)')
