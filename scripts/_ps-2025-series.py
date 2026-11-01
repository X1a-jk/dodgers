# -*- coding: utf-8 -*-
"""2025 道奇季后赛全程对阵（供 2025 报告叙事用）"""
import json, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
u = 'https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=119&gameTypes=F,D,L,W&startDate=2025-09-26&endDate=2025-11-08'
d = json.loads(opener.open(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read().decode())
seen = {}
for dt in d.get('dates', []):
    for g in dt.get('games', []):
        sd = g.get('seriesDescription', '?')
        away = g['teams']['away']['team']['name']
        home = g['teams']['home']['team']['name']
        aw = g['teams']['away'].get('score')
        hs = g['teams']['home'].get('score')
        seen.setdefault(sd, []).append('%s %s-%s %s' % (away, aw, hs, home))
for k, v in seen.items():
    print('==', k, '(%d场)' % len(v))
    for s in v:
        print('  ', s)
