import urllib.request, json, ssl
import os
ctx=ssl.create_default_context()
https=urllib.request.HTTPSHandler(context=ctx)
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}), https)

def fetch(url):
    req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    with opener.open(req, timeout=60) as resp:
        return json.loads(resp.read().decode('utf-8'))

base='https://statsapi.mlb.com/api/v1/teams/119/roster'
active=fetch(base+'?rosterType=active&season=2026')
full=fetch(base+'?rosterType=40Man&season=2026')
out='D:\\baseball\\scripts\\roster_data.json'
with open(out,'w',encoding='utf-8') as f:
    json.dump({'active':active,'full':full}, f, ensure_ascii=False, indent=2)
print('saved', out)
print('active count', len(active.get('roster',[])))
print('40man count', len(full.get('roster',[])))
print('sample statuses')
seen=set()
for r in full.get('roster',[]):
    seen.add(r['status']['description'])
print(seen)
