# -*- coding: utf-8 -*-
"""Batch-13（收官批）数据抓取：hunter-feduccia / chuckie-robinson / justin-dean -> scripts\_batch13-data.json"""
import json, time
import urllib.request
from datetime import datetime

BATCH = {
 'hunter-feduccia': 683798,
 'chuckie-robinson': 675944,
 'justin-dean': 682782,
}
YEAR = 2025
HDR = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
OUT = r'D:\baseball\scripts\_batch13-data.json'

def get(url):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=HDR)
            return json.load(urllib.request.urlopen(req, timeout=40))
        except Exception as e:
            print('retry', attempt + 1, url[:60], str(e)[:60], flush=True)
            time.sleep(4)
    return None

result = {}
for slug, pid in BATCH.items():
    print('fetching', slug, flush=True)
    person = get(f'https://statsapi.mlb.com/api/v1/people/{pid}')
    time.sleep(0.5)
    hist = get(f'https://statsapi.mlb.com/api/v1/people/{pid}/stats?stats=yearByYear&group=hitting&leagueListId=mlb_milb')
    time.sleep(0.5)
    h2025 = get(f'https://statsapi.mlb.com/api/v1/people/{pid}/stats?stats=season&group=hitting&season={YEAR}&sportIds=1')
    time.sleep(0.5)
    trans = get(f'https://statsapi.mlb.com/api/v1/people/{pid}/transactions?startDate=01/01/{YEAR}&endDate=12/31/{YEAR}')
    result[slug] = {
        'person': person, 'yearByYear': hist, f'hit{YEAR}_mlb': h2025, 'transactions': trans,
    }
    time.sleep(1)

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print('written', OUT)
