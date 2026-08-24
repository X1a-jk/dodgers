import urllib.request, json, ssl
url='https://statsapi.mlb.com/api/v1.1/game/823910/feed/live'
ctx=ssl.create_default_context()
req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
https=urllib.request.HTTPSHandler(context=ctx)
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}), https)
with opener.open(req, timeout=60) as resp:
    data=json.loads(resp.read().decode('utf-8'))
out='D:\\baseball\\scripts\\game_823910.json'
with open(out,'w',encoding='utf-8') as f:
    json.dump(data,f,ensure_ascii=False,indent=2)
print('saved', out)
print('keys', list(data.keys()))
sp=data.get('liveData',{}).get('plays',{}).get('scoringPlays',[])
print('scoringPlays count', len(sp))
