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

# ---------- 中文化 ----------
TEAM_CN = {
    'Los Angeles Dodgers': '道奇', 'Arizona Diamondbacks': '响尾蛇', 'Atlanta Braves': '勇士',
    'Baltimore Orioles': '金莺', 'Boston Red Sox': '红袜', 'Chicago Cubs': '小熊',
    'Chicago White Sox': '白袜', 'Cincinnati Reds': '红人', 'Cleveland Guardians': '守护者',
    'Colorado Rockies': '洛矶', 'Detroit Tigers': '老虎', 'Houston Astros': '太空人',
    'Kansas City Royals': '皇家', 'Los Angeles Angels': '天使', 'Miami Marlins': '马林鱼',
    'Milwaukee Brewers': '酿酒人', 'Minnesota Twins': '双城', 'New York Mets': '大都会',
    'New York Yankees': '洋基', 'Athletics': '运动家', 'Philadelphia Phillies': '费城人',
    'Pittsburgh Pirates': '海盗', 'San Diego Padres': '教士', 'San Francisco Giants': '巨人',
    'Seattle Mariners': '水手', 'St. Louis Cardinals': '红雀', 'Tampa Bay Rays': '光芒',
    'Texas Rangers': '游骑兵', 'Toronto Blue Jays': '蓝鸟', 'Washington Nationals': '国民',
}

POS_CN = {
    'RHP': '右投', 'LHP': '左投', 'P': '投手', 'C': '捕手', '1B': '一垒手', '2B': '二垒手',
    '3B': '三垒手', 'SS': '游击手', 'LF': '左外野手', 'CF': '中外野手', 'RF': '右外野手',
    'OF': '外野手', 'IF': '内野手', 'INF': '内野手', 'DH': '指定打击', 'UT': '工具人', 'TWP': '二刀流',
}


def _t(name):
    return TEAM_CN.get(name, name)


def _pos_abbr(tok):
    return POS_CN.get(tok, tok)


def parse_pos(desc):
    """从描述开头提取位置缩写，如 'LHP Kris Bubic elected...' -> ('LHP', 'Kris Bubic')"""
    import re
    m = re.match(r'^([A-Z]{1,3})\s+([A-Z][a-zA-Z\'\-]+(?: [A-Z][a-zA-Z\'\-]+)+)', desc or '')
    if m and m.group(1) in POS_CN:
        return m.group(1), m.group(2)
    return None, None


def cn_desc(desc):
    """把官方英文操作描述改写为中文；不认识的格式原样返回。"""
    import re
    d = desc or ''
    m = re.match(r"^(.*?) signed free agent ([A-Z]{1,3}) ([^ ]+(?: [^ ]+)*?) to a (?:minor|major) league contract", d)
    if m:
        lvl = '小联盟' if 'minor' in d else '大联盟'
        return '%s以%s合约签下%s %s' % (_t(m.group(1)), lvl, _pos_abbr(m.group(2)), m.group(3))
    m = re.match(r"^([A-Z]{1,3}) ([^ ]+(?: [^ ]+)*?) (?:elected|declared) free agency", d)
    if m:
        return '%s %s 选择成为自由球员，可与任何球队签约' % (_pos_abbr(m.group(1)), m.group(2))
    m = re.match(r"^(.*?) traded ([A-Z]{1,3}) ([^ ]+(?: [^ ]+)*?) to (.*?) for (?:cash considerations|cash)", d)
    if m:
        return '%s将%s %s交易至%s，换取现金' % (_t(m.group(1)), _pos_abbr(m.group(2)), m.group(3), _t(m.group(4)))
    m = re.match(r"^(.*?) traded ([A-Z]{1,3}) ([^ ]+(?: [^ ]+)*?) to (.*?) for ([A-Z]{1,3}) ([^ ]+(?: [^ ]+)*?)$", d)
    if m:
        return '%s将%s %s交易至%s，换回%s %s' % (_t(m.group(1)), _pos_abbr(m.group(2)), m.group(3), _t(m.group(4)), _pos_abbr(m.group(5)), m.group(6).rstrip('.'))
    m = re.match(r"^(.*?) designated ([A-Z]{1,3}) ([^ ]+(?: [^ ]+)*?) for assignment", d)
    if m:
        return '%s指定让渡%s %s（7 天内可交易、下放或释出）' % (_t(m.group(1)), _pos_abbr(m.group(2)), m.group(3))
    m = re.match(r"^(.*?) released ([A-Z]{1,3}) ([^ ]+(?: [^ ]+)*?)$", d)
    if m:
        return '%s释出%s %s' % (_t(m.group(1)), _pos_abbr(m.group(2)), m.group(3))
    m = re.match(r"^(.*?) selected the contract of ([A-Z]{1,3}) ([^ ]+(?: [^ ]+)*?) from (.*?)$", d)
    if m:
        return '%s从%s调入%s %s，进入 40 人名单' % (_t(m.group(1)), _t(m.group(4)), _pos_abbr(m.group(2)), m.group(3))
    m = re.match(r"^(.*?) sent ([A-Z]{1,3}) ([^ ]+(?: [^ ]+)*?) outright to (.*?)$", d)
    if m:
        return '%s将%s %s直接下放至%s（不占 40 人名额）' % (_t(m.group(1)), _pos_abbr(m.group(2)), m.group(3), _t(m.group(4)))
    m = re.match(r"^(.*?) (?:activated|recalled) ([A-Z]{1,3}) ([^ ]+(?: [^ ]+)*?) (?:from|of) (.*?)$", d)
    if m:
        return '%s从%s激活/上调%s %s' % (_t(m.group(1)), _t(m.group(4)), _pos_abbr(m.group(2)), m.group(3))
    m = re.match(r"^(.*?) (?:optioned|assigned) ([A-Z]{1,3}) ([^ ]+(?: [^ ]+)*?) to (.*?)$", d)
    if m:
        return '%s将%s %s下放至%s' % (_t(m.group(1)), _pos_abbr(m.group(2)), m.group(3), _t(m.group(4)))
    return d


def norm_move(t):
    person = t.get('person') or {}
    desc = t.get('description', '')
    pos, _ = parse_pos(desc)
    return {
        'id': t.get('id'),
        'name': person.get('fullName', '?'),
        'personId': person.get('id'),
        'date': t.get('effectiveDate') or t.get('date'),
        'type': classify(desc or t.get('typeDesc')),
        'typeCn': TX_CN.get(classify(desc or t.get('typeDesc')), t.get('typeDesc')),
        'desc': desc,
        'cn': cn_desc(desc),
        'pos': pos,
        'posCn': _pos_abbr(pos) if pos else None,
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
        desc = t.get('description', '')
        pos, _ = parse_pos(desc)
        keep.append({
            'id': t.get('id'),
            'name': person.get('fullName', '?'),
            'date': t.get('effectiveDate') or t.get('date'),
            'kind': 'trade' if is_trade else 'signing',
            'desc': desc,
            'cn': cn_desc(desc),
            'pos': pos,
            'posCn': _pos_abbr(pos) if pos else None,
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

    # FA 追踪（v1：从道奇流推导），附位置与 2026 赛季数据
    sr_by_name = {}
    if os.path.exists(SEASON_ROSTER):
        sr = json.load(open(SEASON_ROSTER, encoding='utf-8'))
        sr_by_name = {p.get('name'): p for p in sr.get('players', [])}

    def _fa_card(m):
        p = sr_by_name.get(m['name']) or {}
        raw_pos = p.get('pos')
        pit_pos = raw_pos in ('P', 'RHP', 'LHP', 'TWP')
        bat = p.get('bat') or {}
        pit = p.get('pit') or {}
        card = {'name': m['name'], 'date': m['date'], 'posCn': POS_CN.get(raw_pos, raw_pos)}
        if pit_pos or (pit and not bat):
            card['stats'] = '%s 场 · ERA %s · %s K' % (p.get('g', '-'), pit.get('era', '-'), pit.get('so', '-'))
        elif bat:
            card['stats'] = '打击率 %s · %s 轰 · %s 打点 · %s 盗垒' % (bat.get('avg', '-'), bat.get('hr', '-'), bat.get('rbi', '-'), bat.get('sb', '-'))
        return card

    declared = [m for m in moves if m['type'] == 'declared_fa']
    fa = {'pending': [], 'reSigned': []}
    for m in declared:
        later = [x for x in moves if x['personId'] == m['personId']
                 and x['type'] in ('signed_mlb', 'signed_milb', 'extension')
                 and (x['date'] or '') >= (m['date'] or '')]
        if later:
            fa['reSigned'].append(dict(_fa_card(m), note=later[0]['cn'] or later[0]['desc']))
        else:
            fa['pending'].append(_fa_card(m))
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
