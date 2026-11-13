# -*- coding: utf-8 -*-
"""Fetch 2025 pitchArsenal for the batch-7 pitchers -> scripts\_batch7-arsenal.json"""
import json, os, time, urllib.request

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

PITCH_CN = {
    'FF': '四缝线速球', 'SI': '伸卡球', 'FC': '卡特球', 'SL': '滑球',
    'ST': '横扫滑球', 'CU': '曲球', 'KC': '曲球（指关节型）',
    'CH': '变速球', 'FS': '快速指叉球', 'FO': '分叉快速球', 'SV': '螺旋球',
}

IDS = {
    'justin-wrobleski': 680736,
    'kirby-yates': 489446,
    'roki-sasaki': 808963,
    'tony-gonsolin': 664062,
    'matt-sauer': 669422,
}

def get_json(url, tries=6):
    last = None
    for i in range(tries):
        try:
            with opener.open(url, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            last = e
            time.sleep(1.5 * (i + 1))
    raise RuntimeError(str(last))

out = {}
for slug, pid in IDS.items():
    url = f'https://statsapi.mlb.com/api/v1/people/{pid}/stats?stats=pitchArsenal&group=pitching&season=2025'
    d = get_json(url)
    rows = []
    for s in (d.get('stats') or [{}])[0].get('splits', []):
        st = s.get('stat', {})
        t = st.get('type', {})
        if not st.get('count'):
            continue
        rows.append({
            'code': t.get('code'), 'desc': t.get('description'),
            'cn': PITCH_CN.get(t.get('code'), t.get('description')),
            'count': st['count'],
            'pct': round(st.get('percentage', 0) * 100, 1),
            'avgSpeed': round(st.get('averageSpeed', 0), 1),
        })
    rows.sort(key=lambda x: -x['count'])
    out[slug] = rows
    print(slug, [(r['code'], r['pct'], r['avgSpeed']) for r in rows], flush=True)
    time.sleep(0.4)

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_batch7-arsenal.json')
json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', p)

