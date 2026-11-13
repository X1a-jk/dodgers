# -*- coding: utf-8 -*-
"""Fetch Dodgers transactions 2025-10-26..2025-11-02 (postseason end window)."""
import json, os, time, urllib.request, urllib.parse

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

def get(path, params=None, tries=6):
    url = 'https://statsapi.mlb.com/api/v1' + path
    if params:
        url += '?' + urllib.parse.urlencode(params)
    last = None
    for i in range(tries):
        try:
            with opener.open(url, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            last = e
            time.sleep(1.5 * (i + 1))
    raise RuntimeError(str(last))

out = []
for start, end in [('2025-10-26', '2025-10-29'), ('2025-10-30', '2025-11-02')]:
    d = get('/transactions', {'teamId': 119, 'startDate': start, 'endDate': end})
    out.extend(d.get('transactions', []))
    time.sleep(0.4)

names = ['Banda', 'Snell', 'Scott', 'Vesia', 'Knack', 'Wrobleski']
for t in out:
    desc = t.get('description', '')
    if any(n in desc for n in names):
        print(t.get('date'), '|', desc)

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_batch6-transactions.json')
json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('total transactions:', len(out), '->', p)
