import urllib.request, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get(u):
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

pk = 823895
plays = get(f'https://statsapi.mlb.com/api/v1/game/{pk}/playByPlay')
print('SCORING PLAYS')
all_plays = plays['allPlays']
for idx in plays['scoringPlays']:
    p = all_plays[idx]
    half = '上' if p['about']['halfInning'] == 'top' else '下'
    print(f"  [{p['about']['inning']}局{half}] {p['result']['description']}")

sched = get('https://statsapi.mlb.com/api/v1/schedule?teamId=119&sportId=1&startDate=2026-09-25&endDate=2026-09-26&hydrate=probablePitcher')
for d in sched.get('dates', []):
    for g in d.get('games', []):
        print()
        print('GAME', d['date'], g['teams']['away']['team']['name'], '@', g['teams']['home']['team']['name'], g['status']['detailedState'], g.get('gameDate'))
        for side in ('away', 'home'):
            pp = g['teams'][side].get('probablePitcher', {})
            if pp:
                print(' ', side, 'probable:', pp.get('fullName'), pp.get('id'))
