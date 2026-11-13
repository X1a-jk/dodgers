# -*- coding: utf-8 -*-
"""Batch12 fetch (hitters): LAD-specific season splits + yearByYear + postseason + person."""
import json, os, time, urllib.request, urllib.parse, ssl

BASE = 'https://statsapi.mlb.com/api/v1'
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPSHandler(context=ssl.create_default_context()))

BOX = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_ps-boxscores-2025.json'), encoding='utf-8'))

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

def team_season_stats(pid, group, season, team_id=119):
    d = get('/people/%d/stats' % pid, {'stats': 'season', 'group': group, 'season': season})
    agg = {}
    for st in d.get('stats', []):
        if st.get('group', {}).get('displayName') != group:
            continue
        for split in st.get('splits', []):
            if split.get('team', {}).get('id') != team_id:
                continue
            s = split.get('stat', {})
            for k, v in s.items():
                if isinstance(v, (int, float)):
                    agg[k] = agg.get(k, 0) + v
                elif k not in agg:
                    agg[k] = v
    return agg or None

def year_by_year(pid, group):
    d = get('/people/%d/stats' % pid, {'stats': 'yearByYear', 'group': group})
    rows = []
    for st in d.get('stats', []):
        for s in st.get('splits', []):
            t = s.get('team', {})
            if t.get('name'):
                rows.append({'season': s.get('season'), 'team': t.get('name'),
                             'stat': {k: v for k, v in s.get('stat', {}).items()
                                      if k in ('gamesPlayed', 'plateAppearances', 'avg', 'obp', 'slg', 'ops', 'homeRuns', 'rbi', 'stolenBases', 'strikeOuts', 'baseOnBalls', 'hits', 'doubles', 'triples', 'runs', 'totalBases', 'atBats')}})
    return rows

def postseason_agg(pid):
    out = {}
    for bid, bx in BOX.items():
        for side in ['away', 'home']:
            team = bx.get('teams', {}).get(side, {})
            if team.get('team', {}).get('id') != 119:
                continue
            for p in team.get('players', {}).values():
                if p.get('person', {}).get('id') != pid:
                    continue
                st = p.get('stats', {}).get('batting')
                if not st:
                    continue
                agg = out.setdefault('batting', {'gamesPlayed': 0, 'atBats': 0, 'hits': 0, 'homeRuns': 0, 'rbi': 0, 'runs': 0, 'strikeOuts': 0, 'baseOnBalls': 0, 'stolenBases': 0, 'doubles': 0, 'triples': 0})
                agg['gamesPlayed'] += 1
                for k in agg:
                    if k != 'gamesPlayed':
                        v = st.get(k)
                        if isinstance(v, (int, float)):
                            agg[k] += v
                agg.setdefault('games', []).append({'gamePk': bid, 'summary': st.get('summary')})
    for g, a in out.items():
        ab = a['atBats']
        a['avg'] = round(a['hits'] / ab, 3) if ab else None
    return out

PLAYERS = [
    (621035, 'chris-taylor', 'Chris Taylor'),
    (665923, 'esteury-ruiz', 'Esteury Ruiz'),
    (671083, 'buddy-kennedy', 'Buddy Kennedy'),
    (592696, 'eddie-rosario', 'Eddie Rosario'),
]

if __name__ == '__main__':
    result = {}
    for pid, slug, name in PLAYERS:
        print('fetching', slug, flush=True)
        try:
            result[slug] = {
                'person': get('/people/%d' % pid).get('people', [{}])[0],
                'hit2025_lad': team_season_stats(pid, 'hitting', 2025),
                'hit2024_lad': team_season_stats(pid, 'hitting', 2024),
                'hit2025_any': team_season_stats(pid, 'hitting', 2025, team_id=None) if False else None,
                'history': year_by_year(pid, 'hitting'),
                'postseason': postseason_agg(pid),
            }
        except Exception as e:
            result[slug] = {'error': str(e)}
            print('ERROR', slug, e, flush=True)
        time.sleep(0.4)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_batch12-data.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print('written', out)
