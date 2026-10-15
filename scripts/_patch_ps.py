# -*- coding: utf-8 -*-
import io
p = r'D:\baseball\scripts\fetch-postseason.py'
t = io.open(p, encoding='utf-8').read()
old = '''                     "fields": "dates,date,games,gamePk,gameDate,gameType,seriesDescription,seriesGameNumber,gamesInSeries,teams,away,home,team,id,name,score,winner,loser,isWinner,status,detailedState,abstractGameState"},
                    min_key="dates")
    series = {}'''
new = '''                     "fields": "dates,date,games,gamePk,gameDate,gameType,seriesDescription,seriesGameNumber,gamesInSeries,teams,away,home,team,id,name,score,winner,loser,isWinner,status,detailedState,abstractGameState"})
    # 未公布季后赛赛程时 dates 为空属正常，不重试
    series = {}'''
assert old in t, 'not found'
t = t.replace(old, new)
io.open(p, 'w', encoding='utf-8').write(t)
print('patched')
