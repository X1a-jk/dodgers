import json, os
os.environ['NO_PROXY'] = '*'
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

with open('D:\\baseball\\data\\game-824320.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

linescore = data['liveData']['linescore']
boxscore = data['liveData']['boxscore']
gameData = data['gameData']

print('=== LINE SCORE ===')
print(json.dumps(linescore, indent=2, ensure_ascii=False))
print()

print('=== STARTING PITCHERS ===')
for team_type in ['away', 'home']:
    team = boxscore['teams'][team_type]
    if 'pitchers' in team and len(team['pitchers']) > 0:
        sp_id = team['pitchers'][0]
        player = team['players'].get(f'ID{sp_id}', {})
        stats = player.get('stats', {}).get('pitching', {})
        print(f"{team_type}: {player.get('fullName')} - {stats}")
print()

print('=== TOP BATTERS ===')
for team_type in ['away', 'home']:
    team = boxscore['teams'][team_type]
    print(team_type)
    for pid, player in team['players'].items():
        if 'batting' in player.get('stats', {}):
            stats = player['stats']['batting']
            if stats.get('atBats', 0) > 0:
                print(f"  {player['person']['fullName']}: {stats}")
