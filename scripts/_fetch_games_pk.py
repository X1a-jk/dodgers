#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抓 9/15~9/19 道奇比赛数据，为补录日报做准备"""
import json
import requests

API = 'https://statsapi.mlb.com/api/v1'
j = requests.get(API + '/schedule', params={
    'teamId': 119, 'startDate': '2026-09-14', 'endDate': '2026-09-19',
    'sportId': 1, 'hydrate': 'probablePitcher,team,linescore,decisions'}, timeout=30).json()
out = []
for d in j.get('dates', []):
    for g in d.get('games', []):
        away = g['teams']['away']['team']['name']
        home = g['teams']['home']['team']['name']
        ar = g['teams']['away'].get('score')
        hr = g['teams']['home'].get('score')
        pk = g['gamePk']
        venue = g.get('venue', {}).get('name', '')
        gd = g['gameDate']
        wp = (g.get('decisions') or {}).get('winner', {}).get('fullName', '')
        lp = (g.get('decisions') or {}).get('loser', {}).get('fullName', '')
        sp = (g.get('decisions') or {}).get('save', {}).get('fullName', '')
        proba = ((g['teams']['away'].get('probablePitcher') or {}).get('fullName', ''))
        probh = ((g['teams']['home'].get('probablePitcher') or {}).get('fullName', ''))
        print(f"pk={pk} {gd} {away} {ar} @ {home} {hr} | {venue} | W:{wp} L:{lp} SV:{sp} | probable away:{proba} home:{probh}")
        out.append(pk)
print('gamePks:', out)
