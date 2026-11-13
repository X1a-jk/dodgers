# -*- coding: utf-8 -*-
"""确认 robinson MLB 出场归属 + 三人背号/头像"""
import json, os, time
import urllib.request

HDR = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
OUT = r'D:\baseball\seasons\2025\players'

def get(url, raw=False):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=HDR)
            data = urllib.request.urlopen(req, timeout=40).read()
            return data if raw else json.loads(data)
        except Exception as e:
            print('retry', attempt + 1, url[:70], str(e)[:60], flush=True)
            time.sleep(4)
    return None

# 1. robinson 2025 season split 明细
d = get('https://statsapi.mlb.com/api/v1/people/642020/stats?stats=season&group=hitting&season=2025&sportIds=1')
for split in d.get('stats', [{}])[0].get('splits', []):
    print('robinson split keys:', {k: split.get(k) for k in ['team', 'sport', 'league'] if split.get(k)}, '| G:', split['stat'].get('gamesPlayed'), 'PA:', split['stat'].get('plateAppearances'), 'R:', split['stat'].get('runs'))

# 2. 背号 + 头像
BATCH = {'hunter-feduccia': 676439, 'chuckie-robinson': 642020, 'justin-dean': 681909}
for slug, pid in BATCH.items():
    p = get(f'https://statsapi.mlb.com/api/v1/people/{pid}')['people'][0]
    print(slug, 'jersey:', p.get('primaryNumber'), '| name:', p.get('fullName'))
    img = get(f'https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_426,q_auto:best/v1/people/{pid}/headshot/67', raw=True)
    dst = os.path.join(OUT, slug, 'headshot.jpg')
    if img and len(img) > 8000:
        with open(dst, 'wb') as f:
            f.write(img)
        print(' ', slug, 'headshot', len(img), 'bytes')
    else:
        src = os.path.join(OUT, slug, 'headshot_2026.jpg')
        if os.path.exists(src):
            import shutil; shutil.copy(src, dst)
            print(' ', slug, 'copied 2026 headshot')
        else:
            print(' ', slug, 'NO HEADSHOT', len(img) if img else 0)
    time.sleep(1)
