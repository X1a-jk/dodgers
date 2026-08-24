import json, re
from collections import defaultdict

prev_path = r'D:\baseball\roster\2026-08-22.md'
new_path = r'D:\baseball\roster\2026-08-23.md'
latest_path = r'D:\baseball\roster\dodgers-roster.md'

with open(r'D:\baseball\scripts\roster_data.json', encoding='utf-8') as f:
    roster = json.load(f)

# Status mapping
status_map = {
    'Active': '活跃',
    'Injured 10-Day': 'IL-10',
    'Injured 15-Day': 'IL-15',
    'Injured 60-Day': 'IL-60',
    'Reassigned to Minors': '小联盟',
}

cat_cn = {
    'Pitcher': '投手',
    'Two-Way Player': '双向球员',
    'Catcher': '捕手',
    'Infielder': '内野手',
    'Outfielder': '外野手',
}

def position_category(pos_name, pos_code):
    if pos_code == '1':
        return 'Pitcher'
    if pos_code == '10':
        return 'Two-Way Player'
    if pos_code == '2':
        return 'Catcher'
    if pos_code in ('3','4','5','6','7','8','9'):
        return 'Infielder' if pos_code in ('3','4','5','6') else 'Outfielder'
    if pos_name in ('Pitcher','Two-Way Player','Catcher','Infielder','Outfielder'):
        return pos_name
    # fallback
    return 'Infielder'

# Build current player dict from 40Man; include reassigned as minors
players = []
active_ids = {p['person']['id'] for p in roster['active']['roster']}
for p in roster['full']['roster']:
    status_desc = p['status']['description']
    # 40-man snapshot: Active + IL; exclude reassigned minors (or include as minors?)
    if status_desc == 'Reassigned to Minors':
        # include as minors
        pass
    person = p['person']
    name = person['fullName']
    num = p.get('jerseyNumber', '')
    pos = p.get('position', {})
    cat = position_category(pos.get('name',''), pos.get('code',''))
    players.append({
        'id': person['id'],
        'name': name,
        'number': num,
        'category': cat,
        'status': status_map.get(status_desc, status_desc),
        'note': '',
    })

# Parse previous markdown for notes and statuses
prev_text = open(prev_path, encoding='utf-8').read()
prev_player = {}
for line in prev_text.splitlines():
    m = re.match(r'\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|', line)
    if not m:
        continue
    name, num, status, note = (x.strip() for x in m.groups())
    if name in ('球员','---') or not name or re.fullmatch(r'[-\s|]+', name):
        continue
    prev_player[name] = {'status': status, 'note': note}

# Transfer notes from previous if same name and injury IL
for pl in players:
    prev = prev_player.get(pl['name'])
    if prev and prev['note'] and pl['status'].startswith('IL'):
        pl['note'] = prev['note']

# Compare current vs previous
changes = []
# map current by name
cur_by_name = {pl['name']: pl for pl in players}
prev_names = set(prev_player.keys())
cur_names = set(cur_by_name.keys())
# in current but not previous
for name in sorted(cur_names - prev_names):
    changes.append(f'新增 {cur_by_name[name]["status"]}: {name} (#{cur_by_name[name]["number"]})')
# in previous but not current
for name in sorted(prev_names - cur_names):
    changes.append(f'移除 {prev_player[name]["status"]}: {name}')
# status changed
for name in sorted(cur_names & prev_names):
    cur_status = cur_by_name[name]['status']
    prev_status = prev_player[name]['status']
    if cur_status != prev_status:
        changes.append(f'{name}: {prev_status} → {cur_status}')

# Group by category and sort
groups = defaultdict(list)
for pl in players:
    groups[pl['category']].append(pl)
for g in groups:
    groups[g].sort(key=lambda x: x['name'])

# Build markdown
date_str = '2026-08-23'
md = [f'# 道奇队40人名单快照 — {date_str}', '']
order = ['Pitcher','Two-Way Player','Catcher','Infielder','Outfielder']
for cat in order:
    if cat not in groups:
        continue
    md.append(f'## {cat_cn[cat]} ({cat_cn[cat]})')
    md.append('')
    md.append('| 球员 | 背号 | 状态 | 备注 |')
    md.append('|------|------|------|------|')
    for pl in groups[cat]:
        md.append(f'| {pl["name"]} | {pl["number"]} | {pl["status"]} | {pl["note"]} |')
    md.append('')

# Injury summary
il10 = [p['name'] for p in players if p['status']=='IL-10']
il15 = [p['name'] for p in players if p['status']=='IL-15']
il60 = [p['name'] for p in players if p['status']=='IL-60']
md.append('---')
md.append('')
md.append('## 伤病名单汇总')
md.append('')
md.append(f'- **IL-10**: {", ".join(il10) if il10 else "无"}')
md.append(f'- **IL-15**: {", ".join(il15) if il15 else "无"}')
md.append(f'- **IL-60**: {", ".join(il60) if il60 else "无"}')
md.append('')

# Changes section
md.append('## 人员变动')
md.append('')
if changes:
    for ch in changes:
        md.append(f'- {ch}')
else:
    md.append('- ✅ 无人员变动')
md.append('')

new_text = '\n'.join(md)
with open(new_path, 'w', encoding='utf-8') as f:
    f.write(new_text)
with open(latest_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print('Wrote', new_path, 'and', latest_path)
print('Active count', len([p for p in players if p['status']=='活跃']))
print('Changes:')
for ch in changes:
    print(ch)
print('No changes') if not changes else None
