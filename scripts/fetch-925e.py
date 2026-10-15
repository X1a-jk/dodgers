import urllib.request, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get(u):
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

pk = 823895
plays = get(f'https://statsapi.mlb.com/api/v1/game/{pk}/playByPlay')
for p in plays['allPlays']:
    if p['about']['inning'] == 8 and p['about']['halfInning'] == 'bottom':
        print(p['result']['description'], '| runs:', p['result'].get('runs'), 'rbi:', p['result'].get('rbi'), '| H:', p['result'].get('homeScore'), 'A:', p['result'].get('awayScore'))
