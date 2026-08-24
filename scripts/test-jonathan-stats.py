import json, urllib.request
pid = 642546
url = f"https://statsapi.mlb.com/api/v1/people/{pid}?hydrate=stats(group=[hitting,pitching],type=[season],season=2026)"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.loads(resp.read())
person = data['people'][0]
print('stats keys:', person.keys())
for g in person.get('stats', []):
    print('group:', g['group']['displayName'])
    for sp in g.get('splits', []):
        print('stat:', sp.get('stat'))
