# -*- coding: utf-8 -*-
"""Batch8 fix: team-specific 2025 season splits (Dodgers id=119) + proper postseason aggregation (outs/ER)."""
import json, os, time, urllib.request, urllib.parse, ssl

BASE = 'https://statsapi.mlb.com/api/v1'
ctx = ssl.create_default_context()
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPSHandler(context=ctx))

BOX = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_ps-boxscores-2025.json'), encoding='utf-8'))
DATA = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_batch8-data.json'), encoding='utf-8'))

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
    """Sum all season splits belonging to the given team (handles mid-season trades)."""
    d = get('/people/%d/stats' % pid, {'stats': 'season', 'group': group, 'season': season})
    agg = {}
    for st in d.get('stats', []):
        if st.get('group', {}).get('displayName') != group:
            continue
        for split in st.get('splits', []):
            t = split.get('team', {})
            if t.get('id') != team_id:
                continue
            s = split.get('stat', {})
            for k, v in s.items():
                if isinstance(v, (int, float)):
                    agg[k] = agg.get(k, 0) + v
                elif k not in agg:
                    agg[k] = v
    return agg or None

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
                st = p.get('stats', {}).get('pitching')
                if not st:
                    continue
                agg = out.setdefault('pitching', {'gamesPlayed': 0, 'outs': 0, 'earnedRuns': 0})
                agg['gamesPlayed'] += 1
                agg['outs'] += st.get('outs', 0)
                agg['earnedRuns'] += st.get('earnedRuns', 0)
                for k in ('strikeOuts', 'baseOnBalls', 'hits', 'homeRuns', 'runs', 'wins', 'losses', 'saves', 'holds', 'blownSaves', 'saveOpportunities', 'inheritedRunners', 'inheritedRunnersScored', 'numberOfPitches'):
                    v = st.get(k)
                    if isinstance(v, (int, float)):
                        agg[k] = agg.get(k, 0) + v
    for g, a in out.items():
        ip = a['outs'] / 3.0
        a['inningsPitched'] = round(ip, 1)
        a['era'] = round(a['earnedRuns'] * 9 / ip, 2) if ip else None
        a['k9'] = round(a.get('strikeOuts', 0) * 27 / a['outs'], 2) if a['outs'] else None
        a['bb9'] = round(a.get('baseOnBalls', 0) * 27 / a['outs'], 2) if a['outs'] else None
    return out

IDS = {'luis-garcia': 472610, 'blake-treinen': 595014, 'lou-trivino-iii': 642152,
       'edgardo-henriquez': 683618, 'will-klein': 694361}

for slug, pid in IDS.items():
    d25 = team_season_stats(pid, 'pitching', 2025)
    d24 = team_season_stats(pid, 'pitching', 2024)
    ps = postseason_agg(pid)
    DATA[slug]['pit2025_lad'] = d25
    DATA[slug]['pit2024_lad'] = d24
    DATA[slug]['postseason'] = ps
    def brief(s):
        if not s: return None
        return {k: s.get(k) for k in ('gamesPlayed','era','whip','inningsPitched','strikeOuts','baseOnBalls','hits','homeRuns','wins','losses','saves','holds','blownSaves','saveOpportunities')}
    print(slug, 'LAD2025:', brief(d25))
    print(slug, 'LAD2024:', brief(d24))
    print(slug, 'PS:', json.dumps(ps, ensure_ascii=False))
    time.sleep(0.4)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_batch8-data.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(DATA, f, ensure_ascii=False, indent=1)
print('written', out)
