# -*- coding: utf-8 -*-
"""Batch7 fetch: 2025 postseason from cached boxscores; person/season/career from network."""
import json, os, time, urllib.request, urllib.parse, ssl

BASE = 'https://statsapi.mlb.com/api/v1'
ctx = ssl.create_default_context()
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPSHandler(context=ctx))

BOX = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_ps-boxscores-2025.json'), encoding='utf-8'))

def get(path, params=None, retries=6):
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

def season_stats(pid, group, season):
    d = get('/people/%d/stats' % pid, {'stats': 'season', 'group': group, 'season': season})
    for st in d.get('stats', []):
        if st.get('group', {}).get('displayName') != group:
            continue
        for split in st.get('splits', []):
            return split.get('stat', {})
    return None

def career_stats(pid, group):
    d = get('/people/%d/stats' % pid, {'stats': 'career', 'group': group})
    for st in d.get('stats', []):
        if st.get('group', {}).get('displayName') == group:
            for split in st.get('splits', []):
                return split.get('stat', {})
    return None

def person(pid):
    d = get('/people/%d' % pid)
    return d.get('people', [{}])[0]

def postseason_cached(pid):
    out = {}
    for bid, bx in BOX.items():
        for side in ['away', 'home']:
            team = bx.get('teams', {}).get(side, {})
            if team.get('team', {}).get('id') != 119:
                continue
            for p in team.get('players', {}).values():
                if p.get('person', {}).get('id') != pid:
                    continue
                for group in ['batting', 'pitching']:
                    st = p.get('stats', {}).get(group)
                    if not st:
                        continue
                    agg = out.setdefault(group, {'gamesPlayed': 0})
                    agg['gamesPlayed'] += 1
                    for k, v in st.items():
                        if k in ('note', 'gamesStarted', 'gamesPitched'):
                            continue
                        if isinstance(v, (int, float)):
                            agg[k] = agg.get(k, 0) + v
    return out

PLAYERS = [
    (680736, 'justin-wrobleski', 'Justin Wrobleski'),
    (489446, 'kirby-yates', 'Kirby Yates'),
    (808963, 'roki-sasaki', 'Roki Sasaki'),
    (664062, 'tony-gonsolin', 'Tony Gonsolin'),
    (669422, 'matt-sauer', 'Matt Sauer'),
]

if __name__ == '__main__':
    result = {}
    for pid, slug, name in PLAYERS:
        print('fetching', slug, flush=True)
        try:
            result[slug] = {
                'person': person(pid),
                'pit2025': season_stats(pid, 'pitching', 2025),
                'pit2024': season_stats(pid, 'pitching', 2024),
                'career_pit': career_stats(pid, 'pitching'),
                'postseason': postseason_cached(pid),
            }
        except Exception as e:
            result[slug] = {'error': str(e)}
            print('ERROR', slug, e, flush=True)
        time.sleep(0.4)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_batch7-data.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print('written', out)

