import requests, json, datetime
prev_mon='2026-08-02'
prev_sun='2026-08-10'
url=f'https://statsapi.mlb.com/api/v1/schedule?teamId=119&sportId=1&startDate={prev_mon}&endDate={prev_sun}'
r=requests.get(url).json()
for d in r['dates']:
    print(f"\n=== {d['date']} ===")
    for g in d['games']:
        if g['status']['abstractGameCode']=='F':
            home=g['teams']['home']
            away=g['teams']['away']
            print(f"  {g['gameDate']} | {away['team']['name']} {away.get('score','-')} @ {home['team']['name']} {home.get('score','-')} | {g['status']['detailedState']}")
