# -*- coding: utf-8 -*-
"""校验三人 playerId + 用 /api/v1/transactions?playerId= 模式重抓交易记录"""
import json, time
import urllib.request

HDR = {'User-Agent': 'Mozilla/5.0'}
def get(url):
    req = urllib.request.Request(url, headers=HDR)
    return json.load(urllib.request.urlopen(req, timeout=40))

names = ['Hunter Feduccia', 'Chuckie Robinson', 'Justin Dean']
ids = {}
for n in names:
    d = get('https://statsapi.mlb.com/api/v1/people/search?names=' + urllib.parse.quote(n))
    ppl = d.get('people', [])
    for p in ppl:
        print(n, '->', p['id'], p.get('fullName'), '| active:', p.get('active'), '| pos:', p.get('primaryPosition', {}).get('abbreviation'))
    if ppl:
        ids[n.split()[-1].lower()] = ppl[0]['id']
    time.sleep(0.5)

# 重抓 2025 交易（playerId 模式）
out = {}
for key, pid in ids.items():
    try:
        d = get(f'https://statsapi.mlb.com/api/v1/transactions?playerId={pid}&startDate=01/01/2025&endDate=12/31/2025')
        rows = [(t.get('date'), t.get('description', '')[:150]) for t in d.get('transactions', [])]
        out[key] = rows
        print('---', key, pid, len(rows), 'transactions')
        for r in rows:
            print(r[0], '|', r[1])
    except Exception as e:
        print(key, 'ERR', str(e)[:80])
    time.sleep(0.5)

with open(r'D:\baseball\scripts\_batch13-transactions.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
