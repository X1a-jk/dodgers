# -*- coding: utf-8 -*-
"""Fetch 2025+2024 season data, person info, career, and 2025 postseason stats for a list of players."""
import json, os, sys, time, urllib.request, urllib.parse, ssl

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
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(2 * (i + 1))

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

def postseason(pid):
    """Aggregate 2025 postseason (gameTypes F,D,L,W) hitting+pitching from boxscores."""
    out = {}
    d = get('/schedule', {'sportId': 1, 'teamId': 119, 'gameTypes': 'F,D,L,W',
                          'startDate': '2025-09-26', 'endDate': '2025-11-15'})
    for date in d.get('dates', []):
        for game in date.get('games', []):
            if game.get('status', {}).get('abstractGameState') != 'Final':
                continue
            bid = game.get('gamePk')
            bx = get('/game/%d/boxscore' % bid)
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
    (669242, 'tommy-edman', 'Tommy Edman'),
    (500743, 'miguel-rojas', 'Miguel Rojas'),
    (571771, 'enrique-hernandez', 'Enrique Hernández'),
    (687221, 'dalton-rushing', 'Dalton Rushing'),
    (808975, 'hyeseong-kim', 'Hyeseong Kim'),
]

if __name__ == '__main__':
    result = {}
    for pid, slug, name in PLAYERS:
        print('fetching', slug, flush=True)
        entry = {
            'person': person(pid),
            'hit2025': season_stats(pid, 'hitting', 2025),
            'hit2024': season_stats(pid, 'hitting', 2024),
            'pit2025': None, 'pit2024': None,
            'career_hit': career_stats(pid, 'hitting'),
            'career_pit': career_stats(pid, 'pitching'),
            'postseason': postseason(pid),
        }
        result[slug] = entry
        time.sleep(0.5)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_batch3-data.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print('written', out)
