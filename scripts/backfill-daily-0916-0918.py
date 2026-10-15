#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补录 2026-09-16 / 17 / 18 名单文件中的「比赛日报」章节（参考 9/15 写法）。
数据源：MLB feed/live（逐局比分、得分play、先发、胜败投）+ schedule（明日预告）。
"""
import importlib.util
import re
import sys
import requests

sys.stdout.reconfigure(encoding='utf-8')

# 复用 daily-report.py 的翻译函数
spec = importlib.util.spec_from_file_location('daily_report', r'D:\baseball\scripts\daily-report.py')
dr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dr)

API = 'https://statsapi.mlb.com/api/v1'
ROSTER_DIR = r'D:\baseball\roster'

GAMES = {
    '2026-09-15': 824466,
    '2026-09-16': 824467,
    '2026-09-17': 824464,
}

feed_cache = {}


def fetch_feed(pk):
    if pk not in feed_cache:
        j = requests.get(f'https://statsapi.mlb.com/api/v1.1/game/{pk}/feed/live', timeout=60).json()
        feed_cache[pk] = j['liveData']
    return feed_cache[pk]


def cjk_width(s):
    return sum(2 if ord(c) > 0x2E7F else 1 for c in s)


def pad_display(s, width):
    return s + ' ' * max(0, width - cjk_width(s))


def line_score_text(ld, away_name, home_name):
    ls = ld['linescore']
    innings = ls['innings']
    nums = [str(i['num']) for i in innings]
    header = '  ' + pad_display('Final', 8) + ' '.join(f'{n:>2}' for n in nums)
    header += '   R   H   E'
    rows = []
    for side, name in (('away', away_name), ('home', home_name)):
        cells = []
        for i in innings:
            r = i[side].get('runs')
            cells.append(f'{r:>2}' if r is not None else ' X')
        t = ls['teams'][side]
        rows.append('  ' + pad_display(name, 8) + ' '.join(cells)
                    + f"  {t['runs']:>2}  {t['hits']:>2}  {t['errors']:>2}")
    return '\n'.join([header] + rows)


def my_simplify(desc):
    """simplify_play_description + 滚地出局补刀"""
    m = re.match(r'(.+?) (?:grounds|grounded) out\b.*?([\w. ]+?) scores', desc)
    if m:
        return f'{m.group(1)} 滚地出局，{m.group(2).strip()} 得分'
    return dr.simplify_play_description(desc)


def scoring_plays_text(ld):
    out = []
    for p in ld['plays']['allPlays']:
        if not p['about'].get('isScoringPlay'):
            continue
        half = '上' if p['about']['halfInning'] == 'top' else '下'
        r = p['result']
        desc = my_simplify(r['description'])
        out.append(f"• {p['about']['inning']}局{half} — {desc}，比分 {r.get('awayScore')}-{r.get('homeScore')}")
    return out


def starter_info(ld, side):
    t = ld['boxscore']['teams'][side]
    pid = t['pitchers'][0]
    person = t['players']['ID' + str(pid)]
    st = person.get('seasonStats', {}).get('pitching', {})
    era = st.get('era', 'N/A')
    return person['person']['fullName'], f"{st.get('wins', 0)}-{st.get('losses', 0)}", era


def recap(date):
    """一场比赛的详细战报块（summary + 逐局比分 + 关键得分）"""
    ld = fetch_feed(GAMES[date])
    away = ld['boxscore']['teams']['away']['team']['name']
    home = ld['boxscore']['teams']['home']['team']['name']
    ar = ld['linescore']['teams']['away']['runs']
    hr = ld['linescore']['teams']['home']['runs']
    lad_side = 'away' if away == 'Los Angeles Dodgers' else 'home'
    lad_r, opp_r = (ar, hr) if lad_side == 'away' else (hr, ar)
    result = '胜' if lad_r > opp_r else '负'
    dec = ld.get('decisions', {})
    wp = (dec.get('winner') or {}).get('fullName', '')
    lp = (dec.get('loser') or {}).get('fullName', '')

    lines = [f'道奇 {lad_r}, {dr.translate_team_name(home if lad_side == "away" else away)} {opp_r}（{result}）']
    lines.append(f'胜投：{wp}　负投：{lp}')
    lines.append('')
    lines.append('逐局比分:')
    lines.append(line_score_text(ld, '道奇' if lad_side == 'away' else dr.translate_team_name(away),
                                 dr.translate_team_name(home) if lad_side == 'away' else '道奇'))
    plays = scoring_plays_text(ld)
    if plays:
        lines.append('')
        lines.append('关键得分：')
        lines.extend(plays[:8])
    return '\n'.join(lines)


def pitcher_season_line(name):
    """按名字查赛季战绩（用于明日预告的先发）"""
    j = requests.get(API + '/people', params={'names': name}, timeout=30).json()
    people = j.get('people', [])
    if not people:
        return name, '0-0', 'N/A'
    pid = people[0]['id']
    s = requests.get(API + f'/people/{pid}/stats', params={'stats': 'season', 'group': 'pitching'}, timeout=30).json()
    splits = (s.get('stats') or [{}])[0].get('splits', [])
    if not splits:
        return name, '0-0', 'N/A'
    st = splits[0]['stat']
    return name, f"{st.get('wins', 0)}-{st.get('losses', 0)}", st.get('era', 'N/A')


def preview_block(date, opp, is_home, beijing_time, venue, lad_sp, opp_sp):
    lines = []
    lines.append(f"道奇 {'vs' if is_home else '@'} {dr.translate_team_name(opp)}")
    lines.append(f'🕐 {beijing_time} (北京时间)')
    lines.append(f'🏟️ {venue}')
    lines.append('')
    lines.append('先发投手：')
    n1, w1, e1 = pitcher_season_line(lad_sp)
    n2, w2, e2 = pitcher_season_line(opp_sp)
    lines.append(f'  道奇: {n1} ({w1}, {e1} ERA)')
    lines.append(f"  {dr.translate_team_name(opp)}: {n2} ({w2}, {e2} ERA)")
    return '\n'.join(lines)


def build_report(date):
    L = [f'⚾ 道奇队日报 - {date}', '']
    # 昨晚赛果 = date 前一场（美国日期）
    prev_date = {'2026-09-16': '2026-09-15', '2026-09-17': '2026-09-16', '2026-09-18': '2026-09-17'}[date]
    L.append('📊 昨晚赛果')
    L.append('')
    L.append(recap(prev_date))
    L.append('')

    if date in ('2026-09-16', '2026-09-17'):
        L.append('🔥 今日赛果')
        L.append('')
        L.append(recap(date))
        L.append('')
        nxt = '2026-09-17' if date == '2026-09-16' else '2026-09-18'
        L.append('🔮 明日预告')
        L.append('')
        if nxt == '2026-09-17':
            L.append(preview_block(nxt, 'Cincinnati Reds', False, '00:40', 'Great American Ball Park',
                                   'Justin Wrobleski', 'Brady Singer'))
        else:
            L.append('9/18 休息日无比赛；下一场 9/19 回归主场迎战巨人')
        L.append('')
    else:
        L.append('🔮 今日预告')
        L.append('')
        L.append('今日无比赛安排（休息日，红人系列赛 8-2 收官后转场回洛杉矶）')
        L.append('')
        L.append('⚔️ 下一场：9/19 旧金山巨人 @ 道奇')
        L.append('')
        L.append(preview_block('2026-09-19', 'San Francisco Giants', True, '10:15',
                               'UNIQLO Field at Dodger Stadium', 'Tyler Glasnow', 'Cesar Perdomo'))
        L.append('')

    L.append('🏥 伤病更新')
    L.append('✅ 无新增伤病')
    L.append('')

    L.append('👥 人员变动')
    moves = {
        '2026-09-16': ['• Kris Bubic：从 IL-60 激活回归活跃名单',
                       '• Paul Gervase：下放至小联盟（Oklahoma City）',
                       '• Ryan Ward：被指定让渡（DFA），移出 40 人名单'],
        '2026-09-17': ['• Landon Knack：从小联盟上调（当日登板拿下胜投）',
                       '• Bobby Miller：下放至小联盟'],
        '2026-09-18': ['• ✅ 无人员变动'],
    }[date]
    L.extend(moves)
    L.append('')
    return '\n'.join(L)


def splice(date):
    path = ROSTER_DIR + f'\\{date}.md'
    text = open(path, encoding='utf-8').read()
    marker = '\n---\n\n## 比赛日报'
    assert marker in text, f'{path} 缺少比赛日报标记'
    text = text.split(marker)[0].rstrip()
    report = build_report(date)
    new = text + '\n\n---\n\n## 比赛日报\n\n' + report + '\n'
    open(path, 'w', encoding='utf-8').write(new)
    print(f'[OK] {path}')
    return new


s16 = splice('2026-09-16')
s17 = splice('2026-09-17')
s18 = splice('2026-09-18')
open(ROSTER_DIR + r'\dodgers-roster.md', 'w', encoding='utf-8').write(s18)
print('[OK] dodgers-roster.md')
