# -*- coding: utf-8 -*-
import requests, sys
sys.stdout.reconfigure(encoding='utf-8')
r = requests.get('https://statsapi.mlb.com/api/v1/stats',
                 params={'stats': 'season', 'group': 'hitting', 'playerPool': 'ALL',
                         'teamId': 119, 'season': 2026, 'limit': 100}, timeout=30)
splits = (r.json().get('stats') or [{}])[0].get('splits') or []
sb_keys = [k for k in splits[0]['stat'] if 'stolen' in k.lower() or 'steal' in k.lower()]
print('sb keys:', sb_keys)
for sp in splits[:5]:
    print(sp['player']['fullName'], {k: sp['stat'].get(k) for k in sb_keys})
