# -*- coding: utf-8 -*-
"""Batch-13 数据重抓（修正后 ID）-> scripts\_batch13-data.json"""
import json, time
import urllib.request

BATCH = {
 'hunter-feduccia': 676439,
 'chuckie-robinson': 642020,
 'justin-dean': 681909,
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
    print('fetching', slug, pid, flush=True)
    person = get(f'https://statsapi.mlb.com/api/v1/people/{pid}')
    time.sleep(0.5)
    hist = get(f'https://statsapi.mlb.com/api/v1/people/{pid}/stats?stats=yearByYear&group=hitting&leagueListId=mlb_milb')
    time.sleep(0.5)
    h2025 = get(f'https://statsapi.mlb.com/api/v1/people/{pid}/stats?stats=season&group=hitting&season={YEAR}&sportIds=1')
    result[slug] = {'person': person, 'yearByYear': hist, f'hit{YEAR}_mlb': h2025}
    time.sleep(1)

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print('written', OUT)

# 打印概要供写作
for slug in BATCH:
    p = result[slug]['person']['people'][0]
    print('====', slug)
    print('name:', p.get('fullName'), '| born:', p.get('birthDate'), '| birthplace:', p.get('birthCity'), p.get('birthCountry'), '| ht/wt:', p.get('height'), p.get('weight'), '| bats/throws:', p.get('batSide', {}).get('code'), p.get('pitchHand', {}).get('code'), '| debut:', p.get('mlbDebutDate'))
    for split in result[slug][f'hit{YEAR}_mlb'].get('stats', [{}])[0].get('splits', []):
        print(f"hit2025_{split['team']['abbreviation']}:", json.dumps({k: split['stat'][k] for k in ['gamesPlayed','plateAppearances','atBats','runs','hits','doubles','triples','homeRuns','rbi','baseOnBalls','strikeOuts','stolenBases','caughtStealing','avg','obp','slg','ops','totalBases','hitByPitch'] if k in split['stat']}, ensure_ascii=False))
    seasons = []
    for st in result[slug]['yearByYear'].get('stats', []):
        if st.get('group', {}).get('displayName') != 'hitting':
            continue
        for s in st.get('splits', []):
            seasons.append((s['season'], s.get('league', {}).get('abbreviation'), s.get('team', {}).get('abbreviation'), s['stat'].get('gamesPlayed'), s['stat'].get('plateAppearances'), s['stat'].get('avg'), s['stat'].get('obp'), s['stat'].get('slg'), s['stat'].get('ops'), s['stat'].get('homeRuns'), s['stat'].get('rbi'), s['stat'].get('stolenBases'), s['stat'].get('baseOnBalls'), s['stat'].get('strikeOuts')))
    print('yearByYear:')
    for row in seasons:
        print(' ', row)
