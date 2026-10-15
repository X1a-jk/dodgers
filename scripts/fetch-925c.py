import urllib.request, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get(u):
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

r = get('https://statsapi.mlb.com/api/v1/teams/119/roster?rosterType=40Man&season=2026')
print('=== 40MAN ===')
for p in r['roster']:
    print(f"{p['person']['fullName']}|{p.get('position',{}).get('abbreviation')}|{p.get('status',{}).get('code')}|{p.get('status',{}).get('description')}")

r2 = get('https://statsapi.mlb.com/api/v1/teams/119/roster?rosterType=fullSeason&season=2026')
