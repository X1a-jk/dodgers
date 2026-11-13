# -*- coding: utf-8 -*-
"""Fetch 2025 full-season Dodgers transactions; extract batch-8 player entries."""
import json, os, time, urllib.request, urllib.parse, ssl

BASE = 'https://statsapi.mlb.com/api/v1'
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPSHandler(context=ssl.create_default_context()))

def get(path, params=None, retries=8):
    url = BASE + path
    if params:
        url += '?' + urllib.parse.urlencode(params)
    for i in range(retries):
        try:
            with opener.open(url, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(1.5 * (i + 1))

NAMES = ['García', 'Garcia', 'Trivino', 'Klein', 'Treinen', 'Henriquez', 'Henríquez']
out = []
for start, end in [('2025-03-01', '2025-08-01'), ('2025-08-01', '2025-11-10')]:
    d = get('/transactions', {'teamId': 119, 'startDate': start, 'endDate': end})
    txs = d.get('transactions', d) if isinstance(d, dict) else d
    for t in txs:
        desc = t.get('description', '')
        if any(n in desc for n in NAMES):
            out.append({'date': t.get('date'), 'type': t.get('type', {}).get('desc'), 'desc': desc})
    time.sleep(0.5)

for t in out:
    print(t['date'], '|', t['type'], '|', t['desc'])
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_batch8-transactions.json')
json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', p)
