# -*- coding: utf-8 -*-
"""Career postseason year-by-year for batch6 players."""
import json, urllib.request, time

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

def getj(url, tries=8):
    last = None
    for i in range(tries):
        try:
            with opener.open(url, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            last = e
            time.sleep(2.0 * (i + 1))
    raise RuntimeError(str(last))

out = {}
for pid, name in [(607455, 'banda'), (605483, 'snell'), (656945, 'scott'), (681911, 'vesia'), (689017, 'knack')]:
    url = f'https://statsapi.mlb.com/api/v1/people/{pid}/stats?stats=yearByYearPostSeason,postSeason&group=pitching'
    d = getj(url)
    rows = []
    career = None
    for st in d.get('stats', []):
        typ = st.get('type', {}).get('displayName')
        for sp in st.get('splits', []):
            s = sp.get('stat', {})
            if typ == 'yearByYearPostSeason':
                rows.append({'season': sp.get('season'), 'g': s.get('gamesPlayed'), 'era': s.get('era'),
                             'ip': s.get('inningsPitched'), 'so': s.get('strikeOuts'), 'sv': s.get('saves'),
                             'w': s.get('wins'), 'l': s.get('losses'), 'gs': s.get('gamesStarted')})
            else:
                career = {'g': s.get('gamesPlayed'), 'era': s.get('era'), 'ip': s.get('inningsPitched'),
                          'so': s.get('strikeOuts'), 'sv': s.get('saves')}
    out[name] = {'years': rows, 'career': career}
    print(name, json.dumps(rows, ensure_ascii=False), flush=True)
    time.sleep(0.5)

json.dump(out, open(r'D:\baseball\scripts\_batch6-pscareer.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('done')
