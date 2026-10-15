# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import statsapi

# 9/6 与 9/7 赛程
r = statsapi.get('schedule', {'teamId': 119, 'sportId': 1, 'startDate': '2026-09-06', 'endDate': '2026-09-07'})
for d in r.get('dates', []):
    print('===DATE===', d['date'])
    for g in d.get('games', []):
        st = g['status']['detailedState']
        away = g['teams']['away']; home = g['teams']['home']
        print('GAME:', away['team']['name'], '@', home['team']['name'])
        print('STATE:', st)
        if st == 'Final':
            print('SCORE:', away['team']['name'], away.get('score'), '-', home.get('score'), home['team']['name'])
            ls = g.get('linescore', {})
            for side in ('away','home'):
                inn = ls.get('innings', [])
                rows = []
                tot_r = tot_h = tot_e = None
            # 简化输出 line score
            ainn = [i.get('away',{}).get('runs','-') for i in ls.get('innings',[])]
            hinn = [i.get('home',{}).get('runs','-') for i in ls.get('innings',[])]
            print('AWAY_INN:', ainn)
            print('HOME_INN:', hinn)
            print('AWAY R/H/E:', ls.get('teams',{}).get('away',{}))
            print('HOME R/H/E:', ls.get('teams',{}).get('home',{}))
        else:
            print('TIME (ET):', g.get('gameDate'))
            away_prob = g.get('probablePitchers',{}).get('away',{})
            home_prob = g.get('probablePitchers',{}).get('home',{})
            print('AWAY_PROB:', away_prob.get('fullName'), away_prob.get('id'))
            print('HOME_PROB:', home_prob.get('fullName'), home_prob.get('id'))
        print('VENUE:', g.get('venue',{}).get('name'))
        print()
