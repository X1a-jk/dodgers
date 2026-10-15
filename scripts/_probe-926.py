#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, io, sys, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get(u, **p):
    for a in range(6):
        try:
            return requests.get(u, timeout=60, **p).json()
        except Exception as e:
            print('retry', a, type(e).__name__)
            time.sleep(4 * (a + 1))
    raise SystemExit('fail')

box = get('https://statsapi.mlb.com/api/v1/game/823167/boxscore')
for side in ('away', 'home'):
    print(side.upper(), box['teams'][side]['team']['name'])
    for pid, pl in box['teams'][side]['players'].items():
        st = pl.get('stats', {}).get('pitching')
        if st and st.get('inningsPitched'):
            print('  %s: %s IP, %s H, %s R/%s ER, %s BB, %s K, ERA %s' % (
                pl['person']['fullName'], st['inningsPitched'], st['hits'], st['runs'],
                st['earnedRuns'], st['baseOnBalls'], st['strikeOuts'], st.get('era')))
# live feed decisions
feed = get('https://statsapi.mlb.com/api/v1.1/game/823167/feed/live')
d = feed['liveData'].get('decisions', {})
print('FEED DECISIONS:', {k: (v or {}).get('fullName') for k, v in d.items()})

# Matt Wilkinson season line
j = get('https://statsapi.mlb.com/api/v1/people', params={'names': 'Matt Wilkinson'})
pid = j['people'][0]['id']
s = get('https://statsapi.mlb.com/api/v1/people/%d/stats' % pid, params={'stats': 'season', 'group': 'pitching'})
sp = (s.get('stats') or [{}])[0].get('splits', [])
print('WILKINSON:', sp[0]['stat'] if sp else 'no stats')
