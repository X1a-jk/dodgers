import json
with open('D:/baseball/game_823916.json', encoding='utf-8') as f:
    d = json.load(f)
plays = d['liveData']['plays']['allPlays']
for p in plays:
    ab = p['about']
    if ab.get('isScoringPlay'):
        print(f"{ab['halfInning']} {ab['inning']}: {p['result']['description'][:200]}")
    # also print runs scored in play
    #print(p['result'].get('rbi'), p['result'].get('awayScore'), p['result'].get('homeScore'))
print('---line score---')
print(d['liveData']['linescore']['teams'])
print('innings')
for inn in d['liveData']['linescore']['innings']:
    print(inn['num'], 'away', inn.get('away',{}).get('runs'), 'home', inn.get('home',{}).get('runs'))
