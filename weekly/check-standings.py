import requests, json
url='https://statsapi.mlb.com/api/v1/standings?leagueId=104&season=2026&teamId=119'
r=requests.get(url).json()
tr = r['records'][0]['teamRecords'][0]
print(json.dumps(tr, indent=2)[:3000])
print('\n--- keys ---')
print(tr.keys())
