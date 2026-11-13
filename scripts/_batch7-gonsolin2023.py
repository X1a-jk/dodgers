# -*- coding: utf-8 -*-
"""Fetch Gonsolin 2023 season stats (for 2023vs2025 comparison)."""
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

url = 'https://statsapi.mlb.com/api/v1/people/664062/stats?stats=season&group=pitching&season=2023'
d = getj(url)
for st in d.get('stats', []):
    for sp in st.get('splits', []):
        s = sp.get('stat', {})
        out = {k: s.get(k) for k in ['gamesPlayed','gamesStarted','wins','losses','era','whip','inningsPitched','strikeOuts','baseOnBalls','hits','homeRuns','earnedRuns','strikeoutsPer9Inn','walksPer9Inn','homeRunsPer9']}
        print(json.dumps(out, ensure_ascii=False))
