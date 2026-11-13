# -*- coding: utf-8 -*-
"""Fetch 2025 Dodgers transactions in 10-day windows (avoid truncation); filter batch-10 names."""
import json, os, time, urllib.request, urllib.parse, ssl, datetime

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

NAMES = ['Gómez', 'Gomez', 'Stratton', 'Ureña', 'Urena', 'Little', 'Loutos']
out = []
d0 = datetime.date(2024, 11, 1)
end = datetime.date(2025, 11, 10)
while d0 < end:
    d1 = min(d0 + datetime.timedelta(days=10), end)
    d = get('/transactions', {'teamId': 119, 'startDate': str(d0), 'endDate': str(d1)})
    txs = d.get('transactions', d) if isinstance(d, dict) else d
    for t in txs:
        desc = t.get('description', '')
        if any(n in desc for n in NAMES):
            out.append({'date': t.get('date'), 'desc': desc})
    d0 = d1
    time.sleep(0.3)

seen = set()
for t in out:
    key = (t['date'], t['desc'])
    if key in seen:
        continue
    seen.add(key)
    print(t['date'], '|', t['desc'])
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_batch10-transactions.json')
json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', p)
