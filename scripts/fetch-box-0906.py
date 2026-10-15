# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import statsapi

r = statsapi.get('schedule', {'teamId': 119, 'sportId': 1, 'startDate': '2026-09-06', 'endDate': '2026-09-06'})
game = r['dates'][0]['games'][0]
pk = game['gamePk']
print('PK:', pk)

# 比分细节
away = game['teams']['away']; home = game['teams']['home']
print('SCORE: {} {} - {} {}'.format(away['team']['name'], away.get('score'), home.get('score'), home['team']['name']))

# 每局比分（从 boxscore 里拿）
bs = statsapi.get('game_boxscore', {'gamePk': pk})
for side in ('away','home'):
    tb = bs['teams'][side].get('teamStats',{}).get('batting',{})
    tp = bs['teams'][side].get('teamStats',{}).get('pitching',{})
    print(side.upper(), 'R/H/E:', tb.get('runs'), tb.get('hits'), bs['teams'][side].get('teamStats',{}).get('fielding',{}).get('errors'))

sp = statsapi.game_scoring_plays(pk)
print('---SCORING---')
print(sp)

dodgers_key = None
for key, team in bs['teams'].items():
    if team['team']['id'] == 119:
        dodgers_key = key
print('---DODGERS BATTERS---')
batters = bs['teams'][dodgers_key].get('batters', [])
for b in batters:
    p = bs['teams'][dodgers_key]['players']['ID'+str(b)]
    st = p.get('stats',{}).get('batting',{})
    if st.get('plateAppearances',0) > 0:
        print(p['person']['fullName'], '| AB', st.get('atBats'), 'R', st.get('runs'), 'H', st.get('hits'), 'RBI', st.get('rbi'), 'BB', st.get('baseOnBalls'), 'HR', st.get('homeRuns'), 'SB', st.get('stolenBases'))

print('---DODGERS PITCHERS---')
pitchers = bs['teams'][dodgers_key].get('pitchers', [])
for b in pitchers:
    p = bs['teams'][dodgers_key]['players']['ID'+str(b)]
    st = p.get('stats',{}).get('pitching',{})
    print(p['person']['fullName'], '| IP', st.get('inningsPitched'), 'H', st.get('hits'), 'R', st.get('runs'), 'ER', st.get('earnedRuns'), 'BB', st.get('baseOnBalls'), 'SO', st.get('strikeOuts'))

# 胜投败投救援
dec = game.get('decisions', {})
print('---DECISIONS---')
for k in ('winner','loser','save'):
    if k in dec:
        print(k, ':', dec[k].get('fullName'))

# 先发投手
for side in ('away','home'):
    pp = game['teams'][side].get('probablePitcher',{})
    if pp:
        print('PROBABLE', side, pp.get('fullName'))
