# -*- coding: utf-8 -*-
"""从 MLB API 构建 2025 道奇名单快照（dashboard DASH_ROSTER_JSON 格式）-> scripts\_batch13-roster-2025.json"""
import json, time
import urllib.request

HDR = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
OUT = r'D:\baseball\scripts\_batch13-roster-2025.json'

def get(url):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=HDR)
            return json.load(urllib.request.urlopen(req, timeout=40))
        except Exception as e:
            print('retry', attempt + 1, str(e)[:60], flush=True)
            time.sleep(4)
    return None

players = {}
for group in ['hitting', 'pitching']:
    d = get(f'https://statsapi.mlb.com/api/v1/stats?stats=season&group={group}&playerPool=ALL&teamId=119&season=2025&sportIds=1')
    for split in d.get('stats', [{}])[0].get('splits', []):
        p = split['player']
        pid = p['id']
        e = players.setdefault(pid, {'id': pid, 'name': p['fullName'], 'pos': '', 'status': 'departed', 'bat': None, 'pit': None})
        s = split['stat']
        if group == 'hitting':
            # 仅当真打者（PA>=50）才记 bat，避免投手客串打席误判二刀流
            if int(s.get('plateAppearances', 0) or 0) >= 50:
                e['bat'] = {'avg': s.get('avg', '-'), 'obp': s.get('obp', '-'), 'slg': s.get('slg', '-'),
                            'ops': s.get('ops', '-'), 'hr': s.get('homeRuns', '-'), 'rbi': s.get('rbi', '-')}
        else:
            if float(str(s.get('inningsPitched', '0') or '0')) >= 10:
                e['pit'] = {'era': s.get('era', '-'), 'whip': s.get('whip', '-'), 'w': s.get('wins', '-'),
                            'l': s.get('losses', '-'), 'so': s.get('strikeOuts', '-'), 'ip': s.get('inningsPitched', '-')}
    time.sleep(1)

# 位置：从 people 端点按 id 批量拿 primaryPosition（50 个一批）
ids = list(players)
for i in range(0, len(ids), 50):
    chunk = ','.join(str(x) for x in ids[i:i+50])
    d = get(f'https://statsapi.mlb.com/api/v1/people?personIds={chunk}&fields=people,id,primaryPosition,primaryNumber')
    for p in d.get('people', []):
        e = players.get(p['id'])
        if e:
            e['pos'] = p.get('primaryPosition', {}).get('abbreviation', '')
    time.sleep(1)

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump({'players': list(players.values())}, f, ensure_ascii=False, indent=1)
print('written', OUT, len(players), 'players')
twoway = [p['name'] for p in players.values() if p['bat'] and p['pit']]
print('two-way:', twoway)
