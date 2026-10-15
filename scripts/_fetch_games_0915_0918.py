#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
API = 'https://statsapi.mlb.com/api/v1'
j = requests.get(API + '/schedule', params={
    'teamId': 119, 'startDate': '2026-09-15', 'endDate': '2026-09-18',
    'sportId': 1, 'hydrate': 'linescore,team'}, timeout=30).json()
for d in j.get('dates', []):
    for g in d.get('games', []):
        away = g['teams']['away']['team']['name']
        home = g['teams']['home']['team']['name']
        ar = g['teams']['away'].get('score')
        hr = g['teams']['home'].get('score')
        st = g.get('status', {}).get('detailedState')
        wp = (g.get('decisions') or {}).get('winner', {}).get('fullName', '')
        lp = (g.get('decisions') or {}).get('loser', {}).get('fullName', '')
        print("{} | {} {} @ {} {} | {} | W:{} L:{}".format(
            g['gameDate'][:10], away, ar, home, hr, st, wp, lp))
