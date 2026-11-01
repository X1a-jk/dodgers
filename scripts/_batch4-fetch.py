# -*- coding: utf-8 -*-
"""第4批：抓个人数据 + 缓存全部季后赛 boxscore（只抓一次），离线聚合"""
import json, os, time, urllib.request, urllib.parse, ssl

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
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(2 * (i + 1))

def season_stats(pid, group, season):
    """返回指定赛季的道奇(teamId=119) split；多队球员过滤主队，单队球员 total 与队 split 相同。
    教训：该端点对无该赛季数据的球员会回退返回其它赛季/多队 total，必须校验 split.team.id 与 gamesPlayed 合理性"""
    d = get('/people/%d/stats' % pid, {'stats': 'season', 'group': group, 'season': season})
    fallback = None
    for st in d.get('stats', []):
        if st.get('group', {}).get('displayName') != group:
            continue
        for split in st.get('splits', []):
            if split.get('season') and int(split['season']) != season:
                continue
            tid = (split.get('team') or {}).get('id')
            if tid == 119:
                return split.get('stat', {})
            if tid is None:
                fallback = split.get('stat', {})
    return fallback

def person(pid):
    return get('/people/%d' % pid).get('people', [{}])[0]

PLAYERS = [
    (690976, 'alex-freeland', 'Alex Freeland', 'hitting'),
    (669743, 'alex-call', 'Alex Call', 'hitting'),
    (666163, 'ben-rortvedt', 'Ben Rortvedt', 'hitting'),
    (605131, 'austin-barnes', 'Austin Barnes', 'hitting'),
    (681546, 'james-outman', 'James Outman', 'hitting'),
]

if __name__ == '__main__':
    result = {}
    for pid, slug, name, group in PLAYERS:
        entry = {
            'person': person(pid),
            'stats2025': season_stats(pid, group, 2025),
            'stats2024': season_stats(pid, group, 2024),
            'group': group, 'pid': pid,
        }
        result[slug] = entry
        print('person', slug, flush=True)
        time.sleep(0.3)

    # 季后赛 boxscore 缓存（只抓一次）
    cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_ps-boxscores-2025.json')
    if os.path.exists(cache_path):
        boxscores = json.load(open(cache_path, encoding='utf-8'))
    else:
        d = get('/schedule', {'sportId': 1, 'teamId': 119, 'gameTypes': 'F,D,L,W',
                              'startDate': '2025-09-26', 'endDate': '2025-11-15'})
        boxscores = {}
        for date in d.get('dates', []):
            for game in date.get('games', []):
                if game.get('status', {}).get('abstractGameState') != 'Final':
                    continue
                pk = game.get('gamePk')
                boxscores[str(pk)] = get('/game/%d/boxscore' % pk)
                print('box', pk, flush=True)
                time.sleep(0.2)
        json.dump(boxscores, open(cache_path, 'w', encoding='utf-8'), ensure_ascii=False)
    print('boxscore cache:', len(boxscores), flush=True)

    # 离线聚合
    for slug, entry in result.items():
        pid, group = entry['pid'], entry['group']
        out = {}
        for bx in boxscores.values():
            for side in ['away', 'home']:
                team = bx.get('teams', {}).get(side, {})
                if team.get('team', {}).get('id') != 119:
                    continue
                for p in team.get('players', {}).values():
                    if p.get('person', {}).get('id') != pid:
                        continue
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
        entry['postseason'] = out
        print('ps agg', slug, flush=True)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_batch4-data.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print('written', out)
