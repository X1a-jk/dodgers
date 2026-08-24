import requests, json
s = requests.Session()
s.trust_env = False
ids = [808963, 675660]
for pid in ids:
    r = s.get(f'https://statsapi.mlb.com/api/v1/people/{pid}?hydrate=stats(type=season,season=2026,group=pitching)')
    data = r.json()
    p = data['people'][0]
    stats = p.get('stats', [])
    print('---', p['fullName'])
    if stats and stats[0].get('splits'):
        print(json.dumps(stats[0]['splits'][0]['stat'], ensure_ascii=False, indent=2))
    else:
        print('no stats')
