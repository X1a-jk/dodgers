#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补录 2026-09-16 / 2026-09-17 名单快照，并重写 2026-09-18（修正变动归属日期）。

方法：当前 40 人名单(EOD 9/18) ←(撤销当日 transactions)← EOD 9/17 ← EOD 9/16 ← EOD 9/15
用重建出的 9/15 状态与真实的 2026-09-15.md 比对做校验。
"""
import re
import sys
import requests
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

API = 'https://statsapi.mlb.com/api/v1'
ROSTER_DIR = r'D:\baseball\roster'

STATUS_MAP = {
    'Active': '活跃',
    'Injured 10-Day': 'IL-10',
    'Injured 15-Day': 'IL-15',
    'Injured 60-Day': 'IL-60',
    'Reassigned to Minors': '小联盟',
}
CAT_CN = {
    'Pitcher': '投手', 'Two-Way Player': '双向球员', 'Catcher': '捕手',
    'Infielder': '内野手', 'Outfielder': '外野手',
}


def category(pos):
    code = pos.get('code', '')
    if code == '1':
        return 'Pitcher'
    if code == '10':
        return 'Two-Way Player'
    if code == '2':
        return 'Catcher'
    if code in ('3', '4', '5', '6'):
        return 'Infielder'
    if code in ('7', '8', '9'):
        return 'Outfielder'
    return 'Infielder'


def fetch_current():
    j = requests.get(API + '/teams/119/roster',
                     params={'rosterType': '40Man', 'season': 2026}, timeout=30).json()
    state = {}
    for p in j.get('roster', []):
        name = p['person']['fullName']
        state[name] = {
            'name': name,
            'number': p.get('jerseyNumber', ''),
            'category': category(p.get('position', {})),
            'status': STATUS_MAP.get(p['status']['description'], p['status']['description']),
        }
    return state


def fetch_tx(start, end):
    j = requests.get(API + '/transactions',
                     params={'teamId': 119, 'startDate': start, 'endDate': end}, timeout=30).json()
    return j.get('transactions', [])


def parse_prev_md(path):
    """解析既有 md：name -> (status, note)"""
    info = {}
    for line in open(path, encoding='utf-8'):
        m = re.match(r'\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|', line)
        if not m:
            continue
        name, num, status, note = (x.strip() for x in m.groups())
        if name in ('球员', '') or set(name) <= set('-| '):
            continue
        info[name] = {'status': status, 'note': note, 'number': num}
    return info


# ---------- 1. 拉当前名单 + 校验 transactions ----------
s18 = fetch_current()
txs = fetch_tx('2026-09-16', '2026-09-18')
by_date = defaultdict(list)
for t in txs:
    by_date[t.get('date', '')].append(t)
for d in ('2026-09-16', '2026-09-17', '2026-09-18'):
    print(f'{d}: {len(by_date.get(d, []))} 条 transactions')
    for t in by_date.get(d, []):
        print('   ', t.get('typeDesc'), '::', (t.get('person') or {}).get('fullName'))

# ---------- 2. 回溯 ----------
# EOD 9/18 →(撤销 9/18 变动)→ EOD 9/17 →(撤销 9/17 变动)→ EOD 9/16
# 注意：每天结束时的状态已包含当天发生的变动，只有跨天才需要撤销
s17 = {k: dict(v) for k, v in s18.items()}          # 9/18 无变动，s17 = s18

s16 = {k: dict(v) for k, v in s17.items()}          # 撤销 9/17：Knack 回归、Miller 下放
assert s16['Landon Knack']['status'] == '活跃'
assert s16['Bobby Miller']['status'] == '小联盟'
s16['Landon Knack']['status'] = '小联盟'
s16['Bobby Miller']['status'] = '活跃'

# ---------- 3. 继续回溯到 9/15（仅校验用） ----------
# s16 已在第 2 节构建好（含 9/17 的撤销），这里只撤销 9/16 的变动：Bubic 激活、Gervase 下放、Ward DFA
assert s16['Kris Bubic']['status'] == '活跃', s16['Kris Bubic']
assert s16['Paul Gervase']['status'] == '小联盟', s16['Paul Gervase']
assert 'Ryan Ward' not in s16          # Ward 9/16 被 DFA，EOD 9/16 已不在 40 人名单

s15_check = {k: dict(v) for k, v in s16.items()}
s15_check['Kris Bubic']['status'] = 'IL-60'
s15_check['Paul Gervase']['status'] = '活跃'
ward = {'name': 'Ryan Ward', 'number': '67', 'category': 'Outfielder', 'status': '小联盟'}
s15_check['Ryan Ward'] = ward

# ---------- 4. 与真实 9/15 文件校验 ----------
real15 = parse_prev_md(ROSTER_DIR + r'\2026-09-15.md')
mismatch = []
for name, v in s15_check.items():
    if name not in real15:
        mismatch.append(f'重建有但 9/15 文件无: {name}')
    elif real15[name]['status'] != v['status']:
        mismatch.append(f"状态不符 {name}: 重建={v['status']} 文件={real15[name]['status']}")
for name in real15:
    if name not in s15_check:
        mismatch.append(f'9/15 文件有但重建无: {name}')
print('\n[校验] 重建 9/15 vs 真实 9/15 文件:',
      '✅ 完全一致' if not mismatch else '⚠️ 有差异')
for m in mismatch:
    print('   ', m)

# ---------- 5. 备注继承 ----------
# 伤病细节备注（非变动类备注）从 9/15 文件继承
INJURY_NOTES = {
    'Ben Casparius': 'Right shoulder inflammation',
    'Edwin Díaz': 'Neck inflammation',
    'Gavin Stone': 'Right shoulder inflammation',
    'Andy Pages': 'Left hand fracture',
}
# 每日变动备注（覆盖继承值）
DAY_NOTES = {
    '2026-09-16': {
        'Kris Bubic': '从 IL-60 上调至活跃名单',
        'Paul Gervase': '从 活跃 下放至小联盟',
        'Edgardo Henriquez': '从 活跃 变为 IL-15（9/14，Lower back discomfort）',
    },
    '2026-09-17': {
        'Landon Knack': '从 小联盟 上调至活跃名单',
        'Bobby Miller': '从 活跃 下放至小联盟',
        'Edgardo Henriquez': '从 活跃 变为 IL-15（9/14，Lower back discomfort）',
    },
    '2026-09-18': {
        'Landon Knack': '从 小联盟 上调至活跃名单',
        'Bobby Miller': '从 活跃 下放至小联盟',
        'Kris Bubic': '从 IL-60 上调至活跃名单',
        'Paul Gervase': '从 活跃 下放至小联盟',
        'Edgardo Henriquez': '从 活跃 变为 IL-15（9/14，Lower back discomfort）',
    },
}
# 更早的历史变动备注（在 9/15 文件里已有，向后延续）
LEGACY_NOTES = {k: v['note'] for k, v in real15.items() if v['note'] and not v['note'].startswith('从') and '新加入' not in v['note']}
LEGACY_NOTES.update(INJURY_NOTES)

CHANGES = {
    '2026-09-16': ['Kris Bubic：IL-60 → 活跃', 'Paul Gervase：活跃 → 小联盟',
                   'Ryan Ward：DFA（指定让渡），移出 40 人名单'],
    '2026-09-17': ['Landon Knack：小联盟 → 活跃', 'Bobby Miller：活跃 → 小联盟'],
    '2026-09-18': [],
}

GAMES = {
    '2026-09-16': {
        'last': '道奇 4 @ 红人 0（胜）',
        'today': '道奇 2 @ 红人 6（负）—— 作客辛辛那提三连战第 2 场',
    },
    '2026-09-17': {
        'last': '道奇 2 @ 红人 6（负）',
        'today': '道奇 8 @ 红人 2（胜）—— 作客辛辛那提三连战收官战',
    },
    '2026-09-18': {
        'last': '道奇 8 @ 红人 2（胜）',
        'today': '无比赛（休息日，三连战结束后转场回洛杉矶）',
    },
}

HEADER_NOTE = {
    '2026-09-16': '> 补录文件：9/16 当日的 40 人名单状态由 MLB transactions 重建',
    '2026-09-17': '> 补录文件：9/17 当日的 40 人名单状态由 MLB transactions 重建',
    '2026-09-18': '> 更新文件：修正人员变动归属（原版本误将 9/16-17 的变动计入 9/18）；9/18 为休息日，无人员变动',
}

STATES = {'2026-09-16': s16, '2026-09-17': s17, '2026-09-18': s18}


def build_md(date):
    state = STATES[date]
    players = list(state.values())
    for p in players:
        note = LEGACY_NOTES.get(p['name'], '')
        note = DAY_NOTES[date].get(p['name'], note)
        p['note'] = note
    groups = defaultdict(list)
    for p in players:
        groups[p['category']].append(p)
    for g in groups:
        groups[g].sort(key=lambda x: x['name'])

    md = [f'# 道奇队40人名单快照 — {date}', '']
    md.append(HEADER_NOTE[date])
    md.append('')
    for cat in ['Pitcher', 'Two-Way Player', 'Catcher', 'Infielder', 'Outfielder']:
        if cat not in groups:
            continue
        md.append(f'## {CAT_CN[cat]} ({CAT_CN[cat]})')
        md.append('')
        md.append('| 球员 | 背号 | 状态 | 备注 |')
        md.append('|------|------|------|------|')
        for p in groups[cat]:
            md.append(f"| {p['name']} | {p['number']} | {p['status']} | {p['note']} |")
        md.append('')
    md.append('---')
    md.append('')
    md.append('## 伤病名单汇总')
    md.append('')
    for il in ('IL-10', 'IL-15', 'IL-60'):
        names = sorted(p['name'] for p in players if p['status'] == il)
        md.append(f'- **{il}**: {", ".join(names) if names else "无"}')
    md.append('')
    md.append('---')
    md.append('')
    md.append('## 人员变动')
    md.append('')
    ch = CHANGES[date]
    if ch:
        for c in ch:
            md.append(f'- {c}')
    else:
        md.append('- ✅ 无人员变动')
    md.append('')
    md.append('---')
    md.append('')
    md.append('## 比赛日报')
    md.append('')
    md.append(f'**昨晚赛果**（{date} 前一场）')
    md.append('')
    md.append(GAMES[date]['last'])
    md.append('')
    md.append(f'**今日**（{date}）')
    md.append('')
    md.append(GAMES[date]['today'])
    md.append('')
    if date == '2026-09-18':
        md.append('**明日预告**')
        md.append('')
        md.append('9/19 旧金山巨人 @ 道奇（主场系列赛开打）')
        md.append('')
    return '\n'.join(md)


for date in ('2026-09-16', '2026-09-17', '2026-09-18'):
    text = build_md(date)
    path = ROSTER_DIR + f'\\{date}.md'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'\n[写入] {path}  ({len(STATES[date])} 人)')

# dodgers-roster.md 始终同步最新一天
latest = build_md('2026-09-18')
with open(ROSTER_DIR + r'\dodgers-roster.md', 'w', encoding='utf-8') as f:
    f.write(latest)
print('[同步] dodgers-roster.md')
