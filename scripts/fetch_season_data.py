import statsapi
import sys
sys.stdout = open('D:/baseball/scripts/season_output.txt', 'w', encoding='utf-8')

print('=== 赛季打者数据 ===')
hitters = statsapi.get('stats', {'teamId': 119, 'group': 'hitting', 'stats': 'season', 'season': 2026, 'playerPool': 'all'})
for s in hitters.get('stats', []):
    for split in s.get('splits', []):
        p = split['player']
        stats = split['stat']
        name = p['fullName']
        pos = split.get('position', {}).get('abbreviation', '')
        avg = stats.get('avg', '.000')
        obp = stats.get('obp', '.000')
        slg = stats.get('slg', '.000')
        ops = stats.get('ops', '.000')
        hr = stats.get('homeRuns', 0)
        rbi = stats.get('rbi', 0)
        pa = stats.get('plateAppearances', 0)
        g = stats.get('gamesPlayed', 0)
        so = stats.get('strikeOuts', 0)
        bb = stats.get('baseOnBalls', 0)
        print(f"{name} ({pos}): {avg}/{obp}/{slg} OPS {ops}, {hr}HR, {rbi}RBI, {pa}PA, {g}G, {so}K/{bb}BB")

print('\n=== 赛季投手数据 ===')
pitchers = statsapi.get('stats', {'teamId': 119, 'group': 'pitching', 'stats': 'season', 'season': 2026, 'playerPool': 'all'})
for s in pitchers.get('stats', []):
    for split in s.get('splits', []):
        p = split['player']
        stats = split['stat']
        name = p['fullName']
        era = stats.get('era', '0.00')
        whip = stats.get('whip', '0.00')
        ip = stats.get('inningsPitched', '0')
        gs = stats.get('gamesStarted', 0)
        g = stats.get('gamesPlayed', 0)
        so = stats.get('strikeOuts', 0)
        bb = stats.get('baseOnBalls', 0)
        h = stats.get('hits', 0)
        er = stats.get('earnedRuns', 0)
        w = stats.get('wins', 0)
        l = stats.get('losses', 0)
        print(f"{name}: {ip}IP, ERA {era}, WHIP {whip}, {w}-{l}, {g}G/{gs}GS, {so}K/{bb}BB, {h}H, {er}ER")
