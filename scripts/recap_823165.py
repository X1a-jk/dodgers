import urllib.request, json

url = 'https://statsapi.mlb.com/api/v1.1/game/823165/feed/live'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
d = json.load(urllib.request.urlopen(req, timeout=30))

plays = d['liveData']['plays']['allPlays']
sp = d['liveData']['plays'].get('scoringPlays', [])

print('SCORING PLAYS:')
for i in sp:
    p = plays[i]
    res = p['result']
    ab = p['about']
    half = 'Top' if ab['halfInning'] == 'top' else 'Bot'
    print(f"  {half} {ab['inning']}: {res['description']} [{res.get('awayScore')}-{res.get('homeScore')}]")

print()
print('DECISIONS:', json.dumps(d['liveData'].get('decisions', {}), ensure_ascii=False))
print('VENUE:', d['gameData']['venue']['name'])

# Box score: batting and pitching highlights
bs = d['liveData']['boxscore']['teams']
for side in ['away', 'home']:
    t = bs[side]['team']['name']
    print(f"\n=== {t} batting ===")
    for pid, st in bs[side]['players'].items():
        b = st.get('stats', {}).get('batting', {})
        if not b.get('gamesPlayed'):
            continue
        note = st.get('stats', {}).get('batting', {})
        pos = ','.join(p['abbreviation'] for p in st.get('allPositions', [])) or '-'
        print(f"  {st['person']['fullName']} ({pos}): {b.get('hits','-')}H, {b.get('homeRuns','-')}HR, {b.get('rbi','-')}RBI, {b.get('baseOnBalls','-')}BB, {b.get('strikeOuts','-')}K, AVG {b.get('avg','-')}, AB {b.get('atBats','-')}")
    print(f"=== {t} pitching ===")
    for pid, st in bs[side]['players'].items():
        p = st.get('stats', {}).get('pitching', {})
        if not p.get('inningsPitched'):
            continue
        pos = ','.join(pp['abbreviation'] for pp in st.get('allPositions', []))
        note = ''
        if p.get('wins'): note += ' W'
        if p.get('losses'): note += ' L'
        if p.get('saves'): note += ' SV'
        if p.get('holds'): note += f" H{p['holds']}"
        print(f"  {st['person']['fullName']} ({pos}): {p.get('inningsPitched')}IP, {p.get('hits','-')}H, {p.get('runs','-')}R/{p.get('earnedRuns','-')}ER, {p.get('baseOnBalls','-')}BB, {p.get('strikeOuts','-')}K, ERA {p.get('era','-')}{note}")
