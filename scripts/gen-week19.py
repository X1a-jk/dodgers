import requests, json

prev_mon = '2026-08-03'
prev_sun = '2026-08-09'
mon = '2026-08-10'
sun = '2026-08-16'

print('=== 上周赛程 ===')
url = f'https://statsapi.mlb.com/api/v1/schedule?teamId=119&sportId=1&startDate={prev_mon}&endDate={prev_sun}'
r = requests.get(url).json()
wins = 0
losses = 0
for date in r['dates']:
    for g in date['games']:
        dodgers_home = g['teams']['home']['team']['id'] == 119
        if dodgers_home:
            dodgers_score = g['teams']['home'].get('score', 0)
            opp_score = g['teams']['away'].get('score', 0)
            opp = g['teams']['away']['team']['name']
        else:
            dodgers_score = g['teams']['away'].get('score', 0)
            opp_score = g['teams']['home'].get('score', 0)
            opp = g['teams']['home']['team']['name']
        result = 'W' if dodgers_score > opp_score else 'L'
        if result == 'W': wins += 1
        else: losses += 1
        print(f"{g['gameDate'][:10]} {result} {dodgers_score}-{opp_score} @ {opp}")
print(f'上周战绩: {wins}-{losses}')

print('\n=== 本周赛程 ===')
url2 = f'https://statsapi.mlb.com/api/v1/schedule?teamId=119&sportId=1&startDate={mon}&endDate={sun}'
r2 = requests.get(url2).json()
for date in r2['dates']:
    for g in date['games']:
        opp = g['teams']['home']['team']['name'] if g['teams']['away']['team']['id']==119 else g['teams']['away']['team']['name']
        loc = 'home' if g['teams']['home']['team']['id']==119 else 'away'
        print(f"{g['gameDate'][:10]} {g['gameDate'][11:16]} vs {opp} ({loc})")

print('\n=== 当周打者数据 ===')
url3 = f'https://statsapi.mlb.com/api/v1/stats?stats=byDateRange&group=hitting&startDate={prev_mon}&endDate={prev_sun}&teamId=119&playerPool=all'
r3 = requests.get(url3).json()
for s in r3['stats'][0]['splits']:
    p = s['player']
    stats = s['stat']
    print(f"{p['fullName']}: {stats['avg']}/{stats['obp']}/{stats['slg']}, PA {stats['plateAppearances']}, HR {stats['homeRuns']}, RBI {stats['rbi']}, SO {stats['strikeOuts']}, BB {stats['baseOnBalls']}")

print('\n=== 当周投手数据 ===')
url4 = f'https://statsapi.mlb.com/api/v1/stats?stats=byDateRange&group=pitching&startDate={prev_mon}&endDate={prev_sun}&teamId=119&playerPool=all'
r4 = requests.get(url4).json()
for s in r4['stats'][0]['splits']:
    p = s['player']
    stats = s['stat']
    print(f"{p['fullName']}: IP {stats['inningsPitched']}, ERA {stats['era']}, WHIP {stats['whip']}, K {stats['strikeOuts']}, BB {stats['baseOnBalls']}, Games {stats['gamesPlayed']}, GS {stats.get('gamesStarted',0)}")

print('\n=== 团队赛季数据 ===')
url5 = 'https://statsapi.mlb.com/api/v1/standings?leagueId=104&season=2026'
r5 = requests.get(url5).json()
team_rec = None
for rec_group in r5['records']:
    for tr in rec_group['teamRecords']:
        if tr['team']['id'] == 119:
            team_rec = tr
            break
    if team_rec: break
if team_rec:
    rec = team_rec['leagueRecord']
    print(f"赛季战绩: {rec['wins']}-{rec['losses']}")
    print(f"胜率: {rec['pct']}")
    print(f"排名: 国联西区第 {team_rec['divisionRank']} 名")
    print(f"近10场: {team_rec['records']['splitRecords'][8]['wins']}-{team_rec['records']['splitRecords'][8]['losses']}")
else:
    print('未找到道奇队战绩')

print('\n=== 赛季打者累计 (Top OPS) ===')
url6 = 'https://statsapi.mlb.com/api/v1/stats?stats=season&group=hitting&teamId=119&playerPool=all&season=2026&limit=300'
r6 = requests.get(url6).json()
hitters = []
for s in r6['stats'][0]['splits']:
    stats = s['stat']
    if stats['atBats'] < 50: continue
    hitters.append((s['player']['fullName'], stats['avg'], stats['obp'], stats['slg'], stats['ops'], stats['homeRuns'], stats['rbi'], stats['atBats']))
hitters.sort(key=lambda x: x[4], reverse=True)
for h in hitters[:8]:
    print(f"{h[0]}: {h[1]}/{h[2]}/{h[3]}, OPS {h[4]}, HR {h[5]}, RBI {h[6]}, AB {h[7]}")

print('\n=== 赛季投手累计 (ERA) ===')
url7 = 'https://statsapi.mlb.com/api/v1/stats?stats=season&group=pitching&teamId=119&playerPool=all&season=2026&limit=300'
r7 = requests.get(url7).json()
pitchers = []
for s in r7['stats'][0]['splits']:
    stats = s['stat']
    ip = float(stats['inningsPitched'])
    if ip < 20: continue
    pitchers.append((s['player']['fullName'], stats['era'], stats['whip'], stats['inningsPitched'], stats['strikeOuts'], stats['wins'], stats['losses']))
pitchers.sort(key=lambda x: x[1])
for p in pitchers[:6]:
    print(f"{p[0]}: ERA {p[1]}, WHIP {p[2]}, IP {p[3]}, K {p[4]}, {p[5]}-{p[6]}")

print('\n=== 伤病名单 ===')
url8 = 'https://statsapi.mlb.com/api/v1/teams/119/roster?rosterType=40Man&season=2026'
try:
    r8 = requests.get(url8).json()
    injuries = []
    for p in r8['roster']:
        status = p.get('status',{}).get('code','')
        if status in ['IL10', 'IL15', 'IL60', 'D10', 'D15', 'D60']:
            injuries.append((p['person']['fullName'], status, p.get('position',{}).get('abbreviation','')))
    if injuries:
        for name, status, pos in injuries:
            print(f"{name} ({pos}): {status}")
    else:
        print('无活跃伤病名单球员')
except Exception as e:
    print('Error:', e)
