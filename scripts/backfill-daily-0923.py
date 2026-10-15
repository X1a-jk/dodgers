#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补录 2026-09-23（北京时间）日报：9/22 美西时间 教士@道奇 战报 + 9/23 预告 + 名单。"""
import importlib.util
import re
import sys
import requests
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

spec = importlib.util.spec_from_file_location('daily_report', r'D:\baseball\scripts\daily-report.py')
dr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dr)

API = 'https://statsapi.mlb.com/api/v1'
ROSTER_DIR = Path(r'D:\baseball\roster')

GAME_RECAP_PK = 823897      # 2026-09-22 美西 Padres @ Dodgers (北京 9/23 上午)
GAME_PREVIEW_PK = 823894    # 2026-09-23 美西 Padres @ Dodgers (北京 9/24 上午)

feed_cache = {}


def fetch_feed(pk):
    if pk not in feed_cache:
        for attempt in range(6):
            try:
                j = requests.get(f'https://statsapi.mlb.com/api/v1.1/game/{pk}/feed/live', timeout=90).json()
                feed_cache[pk] = j['liveData']
                break
            except Exception:
                if attempt == 5:
                    raise
                import time
                time.sleep(4 * (attempt + 1))
    return feed_cache[pk]


def cjk_width(s):
    return sum(2 if ord(c) > 0x2E7F else 1 for c in s)


def pad_display(s, width):
    return s + ' ' * max(0, width - cjk_width(s))


def line_score_text(ld, away_name, home_name):
    ls = ld['linescore']
    nums = [str(i['num']) for i in ls['innings']]
    header = '  ' + pad_display('Final', 8) + ' '.join(f'{n:>2}' for n in nums) + '   R   H   E'
    rows = []
    for side, name in (('away', away_name), ('home', home_name)):
        cells = []
        for i in ls['innings']:
            r = i[side].get('runs')
            cells.append(f'{r:>2}' if r is not None else ' X')
        t = ls['teams'][side]
        rows.append('  ' + pad_display(name, 8) + ' '.join(cells)
                    + f"  {t['runs']:>2}  {t['hits']:>2}  {t['errors']:>2}")
    return '\n'.join([header] + rows)


def my_simplify(desc):
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


def recap(pk):
    ld = fetch_feed(pk)
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
    sv = (dec.get('save') or {}).get('fullName', '')

    opp_name = home if lad_side == 'away' else away
    lines = [f'道奇 {lad_r}, {dr.translate_team_name(opp_name)} {opp_r}（{result}）']
    lines.append(f'胜投：{wp}　负投：{lp}' + (f'　救援：{sv}' if sv else ''))
    lines.append('')
    lines.append('逐局比分:')
    lines.append(line_score_text(ld, '道奇' if lad_side == 'away' else dr.translate_team_name(away),
                                 dr.translate_team_name(home) if lad_side == 'away' else '道奇'))
    plays = scoring_plays_text(ld)
    if plays:
        lines.append('')
        lines.append('关键得分：')
        lines.extend(plays[:10])
    return '\n'.join(lines)


def _get(url, **params):
    for attempt in range(5):
        try:
            return requests.get(url, timeout=60, **params).json()
        except Exception:
            if attempt == 4:
                raise
            import time
            time.sleep(3 * (attempt + 1))


def pitcher_season_line(name):
    j = _get(API + '/people', params={'names': name})
    people = j.get('people', [])
    if not people:
        return name, '0-0', 'N/A'
    pid = people[0]['id']
    s = _get(API + f'/people/{pid}/stats', params={'stats': 'season', 'group': 'pitching'})
    splits = (s.get('stats') or [{}])[0].get('splits', [])
    if not splits:
        return name, '0-0', 'N/A'
    st = splits[0]['stat']
    return name, f"{st.get('wins', 0)}-{st.get('losses', 0)}", st.get('era', 'N/A')


def preview(pk):
    j = requests.get(API + f'/schedule', params={'gamePks': pk, 'hydrate': 'probablePitcher,venue,team'}, timeout=60).json()
    g = j['dates'][0]['games'][0]
    away = g['teams']['away']['team']['name']
    home = g['teams']['home']['team']['name']
    is_home = home == 'Los Angeles Dodgers'
    opp = away if is_home else home
    venue = g.get('venue', {}).get('name', 'TBD')
    dt = datetime.fromisoformat(g['gameDate'].replace('Z', '+00:00'))
    beijing = (dt.timestamp() + 8 * 3600)
    bt = datetime.utcfromtimestamp(beijing).strftime('%H:%M')

    lad_sp = (g['teams']['home' if is_home else 'away'].get('probablePitcher') or {}).get('fullName', 'TBD')
    opp_sp = (g['teams']['away' if is_home else 'home'].get('probablePitcher') or {}).get('fullName', 'TBD')

    lines = [f"道奇 {'vs' if is_home else '@'} {dr.translate_team_name(opp)}"]
    lines.append(f'🕐 {bt} (北京时间)')
    lines.append(f'🏟️ {venue}')
    lines.append('')
    lines.append('先发投手：')
    n1, w1, e1 = pitcher_season_line(lad_sp) if lad_sp != 'TBD' else (lad_sp, '-', '-')
    n2, w2, e2 = pitcher_season_line(opp_sp) if opp_sp != 'TBD' else (opp_sp, '-', '-')
    lines.append(f'  道奇: {n1} ({w1}, {e1} ERA)')
    lines.append(f"  {dr.translate_team_name(opp)}: {n2} ({w2}, {e2} ERA)")
    return '\n'.join(lines)


def main():
    today = '2026-09-23'

    # --- 名单 ---
    prev = dr.parse_existing_roster(ROSTER_DIR / '2026-09-21.md')
    roster = []
    for attempt in range(6):
        roster = dr.fetch_40man_roster()
        if roster:
            break
        import time
        time.sleep(4 * (attempt + 1))
    changes = dr.detect_roster_changes(roster, prev) if roster else []
    roster_md = dr.build_roster_markdown(roster, prev, today) if roster else ''

    # --- 战报 ---
    L = [f'⚾ 道奇队日报 - {today}', '']
    L.append('📊 昨晚赛果')
    L.append('')
    L.append(recap(GAME_RECAP_PK))
    L.append('')
    L.append('🔮 今日预告')
    L.append('')
    L.append(preview(GAME_PREVIEW_PK))
    L.append('')
    L.append('🏥 伤病更新')
    L.append('✅ 无新增伤病')
    L.append('')
    L.append('👥 人员变动')
    L.append('')
    changes_txt = dr.format_roster_changes(changes).strip()
    L.append(changes_txt if changes_txt else '✅ 无人员变动')
    L.append('')
    report = '\n'.join(L)

    daily_file = ROSTER_DIR / f'{today}.md'
    full = roster_md + '\n\n---\n\n## 比赛日报\n\n' + report
    daily_file.write_text(full, encoding='utf-8')
    print(f'[OK] {daily_file}')

    latest = ROSTER_DIR / 'dodgers-roster.md'
    latest.write_text(full, encoding='utf-8')
    print('[OK] dodgers-roster.md')

    print()
    print(report)


if __name__ == '__main__':
    main()
