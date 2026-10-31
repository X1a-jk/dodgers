import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

pks = [849828, 849823, 849819, 849822, 849809, 849812, 849811]
files = [rf'D:\baseball\data\ps-box-{pk}.json' for pk in pks[:-1]] + [r'D:\baseball\data\g3-box.json']

participants = {}  # name -> {'g': set of pks, 'bat': bool, 'pit': bool}

for pk, f in zip(pks, files):
    d = json.load(open(f, encoding='utf-8'))
    for side in ('away', 'home'):
        team = d['teams'][side]
        if team['team']['id'] != 119:
            continue
        for pid, p in team['players'].items():
            st_b = p.get('stats', {}).get('batting', {})
            st_p = p.get('stats', {}).get('pitching', {})
            played = False
            if st_b and st_b.get('gamesPlayed') == 1 and (st_b.get('plateAppearances', 0) > 0):
                played = True
            if st_p and st_p.get('inningsPitched', '0.0') != '0.0':
                played = True
            # 代跑/守备替换可能没有 PA/IP，用 allSubstitutions 不好拿；用 boxscore 的 batOrder/position 兜底
            if not played and 'allPositions' in p and p.get('batOrder'):
                played = True
            if not played and st_b.get('plateAppearances', 0) > 0:
                played = True
            if played:
                name = p['person']['fullName']
                e = participants.setdefault(name, {'games': 0, 'bat': False, 'pit': False})
                e['games'] += 1
                if st_b.get('plateAppearances', 0) > 0:
                    e['bat'] = True
                if st_p.get('inningsPitched', '0.0') != '0.0':
                    e['pit'] = True

print(f'季后赛已出场（截至 NLCS G3，{len(pks)} 场）：{len(participants)} 人')
for name, e in sorted(participants.items(), key=lambda kv: -kv[1]['games']):
    tags = []
    if e['bat']: tags.append('打')
    if e['pit']: tags.append('投')
    print(f"{name:<22} {e['games']}场 {'/'.join(tags)}")

json.dump({k: v for k, v in participants.items()}, open(r'D:\baseball\data\ps-participants.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
