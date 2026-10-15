import urllib.request, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get(u):
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

pk = 823895
g = get(f'https://statsapi.mlb.com/api/v1/game/{pk}/boxscore')
d = g.get('decisions', {})
print('WP:', d.get('winner', {}).get('fullName'))
print('LP:', d.get('loser', {}).get('fullName'))
print('SV:', d.get('save', {}).get('fullName'))

plays = get(f'https://statsapi.mlb.com/api/v1/game/{pk}/playByPlay')
allp = plays['allPlays']
for idx in plays['scoringPlays']:
    p = allp[idx]
    if p['about']['inning'] == 8 and p['about']['halfInning'] == 'bottom':
        print('8局下得分play完整描述:', p['result']['description'])
        print('rbi:', p['result'].get('rbi'), 'awayScore:', p['result'].get('awayScore'), 'homeScore:', p['result'].get('homeScore'))
