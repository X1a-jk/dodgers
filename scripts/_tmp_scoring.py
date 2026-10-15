import urllib.request, json
pk=823905
data=json.loads(urllib.request.urlopen(f'https://statsapi.mlb.com/api/v1.1/game/{pk}/feed/live', timeout=30).read().decode())
for p in data['liveData']['plays'].get('scoringPlays',[]):
    play=data['liveData']['plays']['allPlays'][p]
    res=play['result']; about=play['about']
    if about['halfInning']=='bottom':
        print(about['inning'], '局下半:', res.get('description',''))
print('--- 9th top ---')
for play in data['liveData']['plays']['allPlays']:
    about=play['about']
    if about['inning']==9 and about['halfInning']=='top':
        print(about.get('startOuts'),'->',about.get('endOuts'),'outs:', play['result'].get('event',''), '-', play['result'].get('description','')[:120])
