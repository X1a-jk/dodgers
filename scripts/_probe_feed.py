#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, requests
pk = 824467
j = requests.get(f'https://statsapi.mlb.com/api/v1.1/game/{pk}/feed/live', timeout=60).json()
ld = j['liveData']
ls = ld['linescore']
print('== linescore innings ==')
for inn in ls['innings']:
    print(inn['num'], 'away', inn['away'].get('runs'), 'home', inn['home'].get('runs'))
print('totals:', {s: ls['teams'][s] for s in ('away','home')})
print()
print('== scoring plays ==')
for p in ld['plays']['allPlays']:
    if p['about'].get('isScoringPlay'):
        r = p['result']
        print(p['about']['halfInning'], p['about']['inning'],
              '| awayScore:', r.get('awayScore'), 'homeScore:', r.get('homeScore'))
        print('   desc:', r['description'][:100])
print()
bx = ld['boxscore']
for side in ('away','home'):
    t = bx['teams'][side]
    pid = t['pitchers'][0]
    person = t['players']['ID' + str(pid)]
    st = person.get('seasonStats', {}).get('pitching', {})
    print(side, 'SP:', person['person']['fullName'],
          '| season:', st.get('wins'), '-', st.get('losses'), st.get('era'))
print()
print('decisions:', ld.get('decisions', {}))
