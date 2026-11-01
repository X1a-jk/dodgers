# -*- coding: utf-8 -*-
"""第4批补充：2024全季数据（跨队total）+ 完整bio + 2025道奇交易记录"""
import json, os, time, urllib.request, urllib.parse, ssl

BASE = 'https://statsapi.mlb.com/api/v1'
ctx = ssl.create_default_context()
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPSHandler(context=ctx))

def get(path, params=None, retries=4):
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
            time.sleep(2 * (i + 1))

def season_total(pid, group, season):
    """取该赛季跨队 total split（team 为 None 的那条）；没有则取第一队 split"""
    d = get('/people/%d/stats' % pid, {'stats': 'season', 'group': group, 'season': season})
    first = None
    for st in d.get('stats', []):
        if st.get('group', {}).get('displayName') != group:
            continue
        for split in st.get('splits', []):
            if split.get('season') and int(split['season']) != season:
                continue
            if (split.get('team') or {}).get('id') is None:
                return split.get('stat', {})
            if first is None:
                first = split.get('stat', {})
    return first

PIDS = {'alex-freeland': 690976, 'alex-call': 669743, 'ben-rortvedt': 666163,
        'austin-barnes': 605131, 'james-outman': 681546}

out = {'players': {}, 'transactions': []}
for slug, pid in PIDS.items():
    p = get('/people/%d' % pid).get('people', [{}])[0]
    out['players'][slug] = {
        'bio_full': p,
        'hit2024_total': season_total(pid, 'hitting', 2024),
        'pit2024_total': season_total(pid, 'pitching', 2024),
    }
    keep = {k: p.get(k) for k in ('id','fullName','birthDate','birthCity','birthStateProvince','birthCountry','height','weight','primaryNumber','mlbDebutDate','draftYear','batSide','pitchHand','primaryPosition')}
    print(slug, keep.get('primaryNumber'), keep.get('draftYear'), flush=True)
    time.sleep(0.3)

# 2025 道奇交易记录（3-10月，看这五人的来路）
d = get('/transactions', {'teamId': 119, 'startDate': '2025-03-01', 'endDate': '2025-10-31', 'sportId': 1})
names = {'Alex Freeland','Alex Call','Ben Rortvedt','Austin Barnes','James Outman'}
for t in d.get('transactions', []):
    desc = t.get('description', '')
    if any(n in desc for n in names):
        out['transactions'].append({'date': t.get('date'), 'desc': desc, 'type': t.get('type', {}).get('desc')})
        print(t.get('date'), desc[:120], flush=True)
    time.sleep(0)

f = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_batch4-extra.json')
json.dump(out, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', f)
