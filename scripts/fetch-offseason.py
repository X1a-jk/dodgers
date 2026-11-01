# -*- coding: utf-8 -*-
"""
fetch-offseason.py — 休赛期转会中心数据抓取
生成 data/offseason.json：
  dodgers.moves      道奇相关操作流（按 typeDesc 分类，禁止按 typeCode —— DFA 撞车）
  dodgers.roster40   当前 40 人名单 + 与上次快照/赛季结束快照对比的新增/移除
  league.signings    全联盟大联盟合约签约 + 交易（排除道奇已收录的，标注原道奇球员）
  fa                 自由球员追踪（v1：pending / reSigned，从道奇流推导）

运营：无 cron，用户喊"抓一下转会"时运行本脚本。
用法：python fetch-offseason.py [--start 2026-10-28] [--no-league]
"""
import json
import os
import sys
import time
import urllib.request
import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'data', 'offseason.json')
SEASON_ROSTER = os.path.join(BASE, 'seasons', '2026', 'snapshots', 'season-roster.json')
TEAM_ID = 119
API = 'https://statsapi.mlb.com/api/v1'
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # 绕开本机失效代理 7892


def get_json(url, tries=4):
    last = None
    for i in range(tries):
        try:
            with opener.open(url, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:  # SSL EOF / 断连常见，重试
            last = e
            time.sleep(1.5 * (i + 1))
    raise RuntimeError('请求失败 %s: %s' % (url, last))


# ---------- 分类（按 typeDesc，绝不用 typeCode） ----------
def classify(desc):
    d = (desc or '').lower()
    if 'declared free agency' in d or 'elected free agency' in d:
        return 'declared_fa'
    if 'for assignment' in d:
        return 'dfa'
    if 'signed' in d and 'free agent' in d:
        return 'signed_milb' if 'minor league' in d else 'signed_mlb'
    if 'extension' in d:
        return 'extension'
    if 'released' in d:
        return 'released'
    if 'outright' in d:
        return 'outright'
    if 'traded' in d or 'trade' in d:
        return 'trade'
    if 'selected' in d:
        return 'selected'
    if 'contract purchased' in d:
        return 'contract_purchased'
    return 'other'


TX_CN = {
    'signed_mlb': '大联盟签约', 'signed_milb': '小联盟签约', 'extension': '续约',
    'declared_fa': '宣布自由球员', 'trade': '交易', 'dfa': '指定让渡',
    'released': '释出', 'outright': 'Outright 下放', 'selected': '40人名单保护',
    'contract_purchased': '合约购入', 'other': '其他',
}


def norm_move(t):
    person = t.get('person') or {}
    return {
        'id': t.get('id'),
        'name': person.get('fullName', '?'),
        'personId': person.get('id'),
        'date': t.get('effectiveDate') or t.get('date'),
        'type': classify(t.get('description') or t.get('typeDesc')),
        'typeCn': TX_CN.get(classify(t.get('description') or t.get('typeDesc')), t.get('typeDesc')),
        'desc': t.get('description', ''),
        'fromTeam': (t.get('fromTeam') or {}).get('name'),
        'toTeam': (t.get('toTeam') or {}).get('name'),
    }


def fetch_dodgers(start, end):
    url = '%s/transactions?teamId=%d&startDate=%s&endDate=%s' % (API, TEAM_ID, start, end)
    data = get_json(url)
    moves = [norm_move(t) for t in data.get('transactions', [])]
    # 去重（同一天同一 id 不会重复，但保险）+ 时间倒序
    seen, out = set(), []
    for m in sorted(moves, key=lambda x: (x['date'] or ''), reverse=True):
        if m['id'] in seen:
            continue
        seen.add(m['id'])
        out.append(m)
    return out


def fetch_league(start, end, dodger_ids, ex_names):
    url = '%s/transactions?sportId=1&startDate=%s&endDate=%s' % (API, start, end)
    data = get_json(url)
    keep = []
    for t in data.get('transactions', []):
        d = (t.get('typeDesc') or '').lower()
        desc = (t.get('description') or '').lower()
        is_mlb_signing = 'signed as free agent' in d and 'minor league' not in desc
        is_trade = 'trade' in d and (t.get('fromTeam') and t.get('toTeam'))
        if not (is_mlb_signing or is_trade):
            continue
        to_id = (t.get('toTeam') or {}).get('id')
        fr_id = (t.get('fromTeam') or {}).get('id')
        if to_id == TEAM_ID or fr_id == TEAM_ID:
            continue  # 道奇相关已收录
        person = t.get('person') or {}
        if not person.get('fullName'):
            continue  # 现金/待定对象对应记录，无人名，跳过
        keep.append({
            'id': t.get('id'),
            'name': person.get('fullName', '?'),
            'date': t.get('effectiveDate') or t.get('date'),
            'kind': 'trade' if is_trade else 'signing',
            'desc': t.get('description', ''),
            'fromTeam': (t.get('fromTeam') or {}).get('name'),
            'toTeam': (t.get('toTeam') or {}).get('name'),
            'exDodger': person.get('fullName') in ex_names,
        })
    # 同一交易 API 按球员各记一条且方向相反（Rayo: OAK->BOS / Eaton: BOS->OAK），
    # 按 date+无序两队合并
    merged = {}
    for it in keep:
        if it['kind'] == 'trade':
            key = (it['date'], frozenset([it['fromTeam'], it['toTeam']]))
            if key in merged:
                merged[key]['names'].append(it['name'])
                merged[key]['exDodger'] = merged[key]['exDodger'] or it['exDodger']
                continue
            it['names'] = [it['name']]
            merged[key] = it
        else:
            it['names'] = [it['name']]
            merged[(it['id'],)] = it
    keep = list(merged.values())
    for it in keep:
        it['name'] = ' / '.join(it.pop('names'))
    keep.sort(key=lambda x: (x['date'] or ''), reverse=True)
    return keep[:200]


def fetch_roster40():
    for season in ('2027', None):
        url = '%s/teams/%d/roster?rosterType=40Man' % (API, TEAM_ID)
        if season:
            url += '&season=%s' % season
        try:
            data = get_json(url)
            roster = data.get('roster', [])
            if roster:
                return sorted((r.get('person') or {}).get('fullName', '?') for r in roster)
        except Exception:
            pass
    return []


def main():
    start = '2026-10-28'
    league_on = True
    args = sys.argv[1:]
    if '--start' in args:
        start = args[args.index('--start') + 1]
    if '--no-league' in args:
        league_on = False
    end = datetime.date.today().isoformat()

    # 2026 道奇出场名单（标注"原道奇"用）
    ex_names = set()
    if os.path.exists(SEASON_ROSTER):
        sr = json.load(open(SEASON_ROSTER, encoding='utf-8'))
        ex_names = {p.get('name') for p in sr.get('players', [])}

    print('抓取道奇 transactions %s ~ %s ...' % (start, end))
    moves = fetch_dodgers(start, end)
    print('  %d 条' % len(moves))

    league = []
    if league_on:
        print('抓取全联盟重磅 ...')
        league = fetch_league(start, end, None, ex_names)
        print('  %d 条' % len(league))

    print('抓取 40 人名单 ...')
    roster = fetch_roster40()
    print('  %d 人' % len(roster))

    # 与上次快照对比（首次运行对比赛季结束名单）
    prev = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else None
    if prev and prev.get('dodgers', {}).get('roster40', {}).get('list'):
        base = set(prev['dodgers']['roster40']['list'])
        base_label = '上次抓取'
    else:
        base = ex_names if ex_names else set()
        base_label = '2026 出场名单（53 人，含非 40 人）'
    added = sorted(set(roster) - base)
    removed = sorted(base - set(roster))
    print('40 人对比（%s）：新增 %d，移除 %d' % (base_label, len(added), len(removed)))

    # FA 追踪（v1：从道奇流推导）
    declared = [m for m in moves if m['type'] == 'declared_fa']
    resigned_ids = set()
    fa = {'pending': [], 'reSigned': []}
    for m in declared:
        later = [x for x in moves if x['personId'] == m['personId']
                 and x['type'] in ('signed_mlb', 'signed_milb', 'extension')
                 and (x['date'] or '') >= (m['date'] or '')]
        if later:
            resigned_ids.add(m['personId'])
            fa['reSigned'].append({'name': m['name'], 'date': later[0]['date'], 'note': later[0]['desc']})
        else:
            fa['pending'].append({'name': m['name'], 'date': m['date']})
    fa['declaredCount'] = len(declared)

    out = {
        'generatedAt': datetime.datetime.now().isoformat(timespec='seconds'),
        'window': {'start': start, 'end': end},
        'dodgers': {
            'moves': moves,
            'roster40': {'count': len(roster), 'list': roster, 'added': added, 'removed': removed},
        },
        'league': {'signings': league},
        'fa': fa,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('已写入 %s' % OUT)
    print('汇总：签约 %d / 宣布FA %d / 交易 %d / 其他 %d' % (
        sum(1 for m in moves if m['type'].startswith('signed')),
        sum(1 for m in moves if m['type'] == 'declared_fa'),
        sum(1 for m in moves if m['type'] == 'trade'),
        sum(1 for m in moves if m['type'] not in ('signed_mlb', 'signed_milb', 'declared_fa', 'trade'))))


if __name__ == '__main__':
    main()
