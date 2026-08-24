import json, urllib.request, re
from pathlib import Path

url = 'https://statsapi.mlb.com/api/v1/teams/119/roster?rosterType=40Man&season=2026'
data = json.loads(urllib.request.urlopen(url, timeout=20).read())
root = Path('D:/baseball/report')

def slugify(name):
    s = name.lower().replace(' ', '-').replace("'", '').replace('.', '')
    return re.sub(r'[^a-z0-9-]', '', s)

missing = []
for e in data['roster']:
    name = e['person']['fullName']
    slug = slugify(name)
    pos = e['position']['abbreviation']
    status = e['status']['code']
    if not (root / slug / f'{slug}-scouting-report.html').exists():
        missing.append((name, pos, status, e['person']['id']))

print(f'Missing reports: {len(missing)}')
for m in missing:
    print(f'- {m[0]} ({m[1]}) [{m[2]}] id={m[3]}')
