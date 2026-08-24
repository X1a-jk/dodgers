import json, os
os.environ['NO_PROXY'] = '*'
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

with open('D:\\baseball\\data\\game-824320.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Probable pitchers
gameData = data['gameData']
print('=== PROBABLE PITCHERS ===')
print(json.dumps(gameData.get('probablePitchers', {}), indent=2, ensure_ascii=False))

# All plays
print('\n=== SCORING PLAYS ===')
all_plays = data['liveData']['plays']['allPlays']
for play in all_plays:
    if play.get('about', {}).get('isScoringPlay'):
        inning = play['about']['inning']
        half = play['about']['halfInning']
        team = '道奇' if half == 'top' else '洛矶'
        desc = play['result']['description']
        print(f"{inning}局{'上' if half=='top' else '下'} ({team}): {desc}")
