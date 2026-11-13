# -*- coding: utf-8 -*-
"""2025 Dodgers fullSeason roster -> jersey numbers for batch9; MLBAM headshots for those missing."""
import json, urllib.request, time, os, shutil

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

def fetch(url, tries=8):
    last = None
    for i in range(tries):
        try:
            with opener.open(url, timeout=30) as r:
                return r.read()
        except Exception as e:
            last = e
            time.sleep(2.0 * (i + 1))
    raise RuntimeError(str(last))

IDS = {
    'michael-kopech': 656629,
    'alexis-diaz': 664747,
    'noah-davis': 663562,
    'bobby-miller': 676272,
    'evan-phillips': 623465,
}
IDS_INV = {v: k for k, v in IDS.items()}

raw = fetch('https://statsapi.mlb.com/api/v1/teams/119/roster/fullSeason?season=2025')
d = json.loads(raw.decode('utf-8'))
for p in d.get('roster', []):
    pid = p.get('person', {}).get('id')
    if pid in IDS_INV:
        print(IDS_INV[pid], 'jersey:', p.get('jerseyNumber'))

for slug, pid in IDS.items():
    dst = rf'D:\baseball\seasons\2025\players\{slug}\headshot.jpg'
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    src = rf'D:\baseball\seasons\2026\players\{slug}\headshot.jpg'
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(slug, 'copied 2026 headshot')
        continue
    u = f'https://img.mlbstatic.com/mlb-photos/image/upload/v1/people/{pid}/headshot/67/current'
    try:
        data = fetch(u)
    except Exception as e:
        print(slug, 'HEADSHOT FAILED', e)
        continue
    with open(dst, 'wb') as f:
        f.write(data)
    print(slug, 'headshot', len(data), 'bytes')
    time.sleep(0.5)
