import json, sys
with open('D:/baseball/game_823916.json', encoding='utf-8') as f:
    d = json.load(f)
plays = d['liveData']['plays']['allPlays']
print('scoringPlayIds', d['liveData']['plays'].get('scoringPlays', []))
print()
for p in plays:
    if p['about'].get('isScoringPlay'):
        print(p['about']['halfInning'], p['about']['inning'], p['result']['description'][:300])
        print('---')
