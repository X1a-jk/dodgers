import urllib.request, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get(u):
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

pk = 823895
box = get(f'https://statsapi.mlb.com/api/v1/game/{pk}/boxscore')
linescore = get(f'https://statsapi.mlb.com/api/v1/game/{pk}/linescore')
decisions = box.get('teams', {})
innings = linescore['innings']
teams = linescore['teams']
print('INNINGS')
for inn in innings:
    a = inn['away'].get('runs'); h = inn['home'].get('runs')
    print(f"  {inn['num']}: away={a} home={h}")
print('TEAM STATS')
for side in ('away', 'home'):
    t = teams[side]
    print(side, t.get('team', {}).get('name'), 'R:', t.get('runs'), 'H:', t.get('hits'), 'E:', t.get('errors'))
print()
decisions = linescore.get('decisions', {})
print('WP:', decisions.get('winner', {}).get('fullName'))
print('LP:', decisions.get('loser', {}).get('fullName'))
sv = decisions.get('save')
if sv:
    print('SV:', sv.get('fullName'))
print()
print('PITCHERS')
for side in ('away', 'home'):
    print(side.upper(), box['teams'][side]['team']['name'])
    for pid, p in box['teams'][side]['players'].items():
        stats = p.get('stats', {}).get('pitching')
        if stats and stats.get('inningsPitched'):
            print(f"  {p['person']['fullName']}: {stats['inningsPitched']} IP, {stats['hits']} H, {stats['runs']} R, {stats['earnedRuns']} ER, {stats['baseOnBalls']} BB, {stats['strikeOuts']} K, ERA {stats.get('era')}")
print()
print('BATTERS (LA)')
for pid, p in box['teams']['home']['players'].items():
    st = p.get('stats', {}).get('batting')
    if st and st.get('atBats', 0) > 0:
        hr = f", HR {st['homeRuns']}" if st.get('homeRuns') else ''
        print(f"  {p['person']['fullName']}: {st['hits']}/{st['atBats']}, R {st.get('runs',0)}, RBI {st.get('rbi',0)}, BB {st.get('baseOnBalls',0)}, K {st.get('strikeOuts',0)}{hr}")
