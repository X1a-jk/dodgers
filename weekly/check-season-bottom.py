import requests

print('=== 赛季打者累计 (Bottom OPS, AB>=50) ===')
url = 'https://statsapi.mlb.com/api/v1/stats?stats=season&group=hitting&teamId=119&playerPool=all&season=2026&limit=300'
r = requests.get(url).json()
hitters = []
for s in r['stats'][0]['splits']:
    stats = s['stat']
    if stats['atBats'] < 50: continue
    hitters.append((s['player']['fullName'], stats['avg'], stats['obp'], stats['slg'], stats['ops'], stats['homeRuns'], stats['rbi'], stats['atBats']))
hitters.sort(key=lambda x: x[4])
for h in hitters[:6]:
    print(f"{h[0]}: {h[1]}/{h[2]}/{h[3]}, OPS {h[4]}, HR {h[5]}, RBI {h[6]}, AB {h[7]}")

print('\n=== 赛季投手累计 (Bottom ERA, IP>=20) ===')
url2 = 'https://statsapi.mlb.com/api/v1/stats?stats=season&group=pitching&teamId=119&playerPool=all&season=2026&limit=300'
r2 = requests.get(url2).json()
pitchers = []
for s in r2['stats'][0]['splits']:
    stats = s['stat']
    ip = float(stats['inningsPitched'])
    if ip < 20: continue
    pitchers.append((s['player']['fullName'], stats['era'], stats['whip'], stats['inningsPitched'], stats['strikeOuts'], stats['wins'], stats['losses']))
pitchers.sort(key=lambda x: x[1], reverse=True)
for p in pitchers[:6]:
    print(f"{p[0]}: ERA {p[1]}, WHIP {p[2]}, IP {p[3]}, K {p[4]}, {p[5]}-{p[6]}")
