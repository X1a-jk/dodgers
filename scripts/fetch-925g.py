import urllib.request, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get(u):
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

pk = 823895
plays = get(f'https://statsapi.mlb.com/api/v1/game/{pk}/playByPlay')
for p in plays['allPlays']:
    if p['about']['inning'] == 8 and p['about']['halfInning'] == 'bottom':
        for r in p.get('runners', []):
            print('runner:', r['details'].get('runner', {}).get('fullName') if r['details'].get('runner') else '?',
                  '| movement:', r.get('movement', {}),
                  '| details event:', r.get('details', {}).get('event'),
                  '| earned:', r.get('details', {}).get('isEarned'),
                  '| rbi:', r.get('details', {}).get('rbi'))
        print('---')
