import statsapi
import sys
sys.stdout = open('D:/baseball/scripts/week20_output.txt', 'w', encoding='utf-8')

prev_mon = '2026-08-10'
prev_sun = '2026-08-16'
this_mon = '2026-08-17'
this_sun = '2026-08-23'

print('=== 上周赛程 ===')
sched = statsapi.get('schedule', {'teamId': 119, 'sportId': 1, 'startDate': prev_mon, 'endDate': prev_sun})
for date in sched.get('dates', []):
    for game in date['games']:
        home = game['teams']['home']['team']['name']
        away = game['teams']['away']['team']['name']
        home_score = game['teams']['home'].get('score', '-')
        away_score = game['teams']['away'].get('score', '-')
        status = game['status']['detailedState']
        if home == 'Los Angeles Dodgers':
            print(f"{date['date']} vs {away.split()[-1]}: {home_score}-{away_score} ({status})")
        else:
            print(f"{date['date']} @ {home.split()[-1]}: {away_score}-{home_score} ({status})")

print('\n=== 本周赛程 ===')
sched2 = statsapi.get('schedule', {'teamId': 119, 'sportId': 1, 'startDate': this_mon, 'endDate': this_sun})
for date in sched2.get('dates', []):
    for game in date['games']:
        home = game['teams']['home']['team']['name']
        away = game['teams']['away']['team']['name']
        time = game['gameDate']
        if home == 'Los Angeles Dodgers':
            print(f"{date['date']} vs {away.split()[-1]}: {time}")
        else:
            print(f"{date['date']} @ {home.split()[-1]}: {time}")

print('\n=== 当周打者数据 ===')
hitters = statsapi.get('stats', {'teamId': 119, 'group': 'hitting', 'stats': 'byDateRange', 'startDate': prev_mon, 'endDate': prev_sun, 'season': 2026, 'playerPool': 'all'})
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

print('\n=== 当周投手数据 ===')
pitchers = statsapi.get('stats', {'teamId': 119, 'group': 'pitching', 'stats': 'byDateRange', 'startDate': prev_mon, 'endDate': prev_sun, 'season': 2026, 'playerPool': 'all'})
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
        print(f"{name}: {ip}IP, ERA {era}, WHIP {whip}, {g}G/{gs}GS, {so}K/{bb}BB, {h}H, {er}ER")

print('\n=== 球队战绩 ===')
team = statsapi.get('teams', {'teamIds': 119})
for t in team['teams']:
    print(f"W-L: {t['record']['wins']}-{t['record']['losses']}")
    print(f"Division rank: {t['divisionRank']}")
    print(f"League rank: {t['leagueRank']}")
    print(f"Sport rank: {t['sportRank']}")
