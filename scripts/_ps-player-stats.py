# -*- coding: utf-8 -*-
"""聚合某球员指定年份季后赛数据（schedule + boxscore 逐场累加）。
用法: python _ps-player-stats.py <playerId> <year>"""
import json, sys, urllib.request

sys.stdout.reconfigure(encoding='utf-8')
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

def get(u):
    return json.loads(opener.open(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read().decode())

pid = int(sys.argv[1]); year = int(sys.argv[2])
sch = get(f'https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=119&gameTypes=F,D,L,W&startDate={year}-09-26&endDate={year}-11-08&fields=dates,date,games,gamePk,teams,team,name')
games = [g for d in sch.get('dates', []) for g in d.get('games', [])]
print(f'{year} postseason games: {len(games)}')

agg = dict.fromkeys(['gamesPlayed','plateAppearances','atBats','runs','hits','doubles','triples','homeRuns','rbi','baseOnBalls','strikeOuts','stolenBases','groundIntoDoublePlay'], 0)
pagg = dict.fromkeys(['gamesPlayed','gamesStarted','inningsPitched','wins','losses','earnedRuns','baseOnBalls','strikeOuts','homeRuns','hits','saves','holds','numberOfPitches'], 0)
seen_p = False
for g in games:
    pk = g['gamePk']
    bx = get(f'https://statsapi.mlb.com/api/v1/game/{pk}/boxscore')
    side = None
    for s in ('home', 'away'):
        if bx['teams'][s]['team']['id'] == 119:
            side = s
    if side is None:
        continue
    hitters = bx['teams'][side].get('players', {})
    for key, pl in hitters.items():
        if pl['person']['id'] != pid:
            continue
        st = pl.get('stats', {}).get('batting', {})
        if st and st.get('gamesPlayed'):
            for k in agg:
                agg[k] += int(st.get(k) or 0)
        pt = pl.get('stats', {}).get('pitching', {})
        if pt and pt.get('gamesPlayed'):
            seen_p = True
            for k in pagg:
                v = pt.get(k)
                if k == 'inningsPitched':
                    pagg[k] += float(str(v or '0').replace('.1', '.3333').replace('.2', '.6667'))
                else:
                    pagg[k] += int(v or 0)
ab = agg['atBats']; h = agg['hits']; tb = h + agg['doubles'] + 2*agg['triples'] + 3*agg['homeRuns']
pa = agg['plateAppearances'] or (ab + agg['baseOnBalls'] + (agg.get('hitByPitch') or 0) + (agg.get('sacFlies') or 0))
avg = h/ab if ab else 0
obp = (h + agg['baseOnBalls']) / (ab + agg['baseOnBalls'] + 0) if ab else 0  # 简化（缺HBP/SF细分）
slg = tb/ab if ab else 0
print(json.dumps({'batting': {'gamesPlayed': agg['gamesPlayed'], 'plateAppearances': pa, 'atBats': ab,
                  'runs': agg['runs'], 'hits': h, 'doubles': agg['doubles'], 'triples': agg['triples'],
                  'homeRuns': agg['homeRuns'], 'rbi': agg['rbi'], 'baseOnBalls': agg['baseOnBalls'],
                  'strikeOuts': agg['strikeOuts'], 'stolenBases': agg['stolenBases'],
                  'avg': round(avg,3), 'obp': round(obp,3), 'slg': round(slg,3),
                  'ops': round(obp+slg,3)},
                  'pitching': (None if not seen_p else {
                      'gamesPlayed': pagg['gamesPlayed'], 'gamesStarted': pagg['gamesStarted'],
                      'inningsPitched': round(pagg['inningsPitched'], 1),
                      'wins': pagg['wins'], 'losses': pagg['losses'],
                      'era': round(pagg['earnedRuns'] * 9 / pagg['inningsPitched'], 2) if pagg['inningsPitched'] else None,
                      'whip': round((pagg['hits'] + pagg['baseOnBalls']) / pagg['inningsPitched'], 2) if pagg['inningsPitched'] else None,
                      'strikeOuts': pagg['strikeOuts'], 'baseOnBalls': pagg['baseOnBalls'],
                      'homeRuns': pagg['homeRuns'], 'saves': pagg['saves'], 'holds': pagg['holds']})},
                 ensure_ascii=False))
