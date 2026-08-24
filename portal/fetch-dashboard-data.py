#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抓取道奇队数据大屏所需数据，保存为 dashboard-data.json。
运行方式：
    python D:\\baseball\\portal\\fetch-dashboard-data.py
"""
import json
import os
import re
import shutil
from datetime import datetime, timedelta
from pathlib import Path

import statsapi

TEAM_ID = 119  # Dodgers
SEASON = datetime.now().year
BASE_DIR = Path(r"D:\baseball")
OUTPUT_FILE = BASE_DIR / "portal" / "dashboard-data.json"
WEEKLY_DIR = BASE_DIR / "weekly"


def safe_get(func, default=None):
    try:
        return func()
    except Exception as e:
        print(f"[WARN] {e}")
        return default


def fetch_standings():
    """获取道奇队战绩与排名"""
    standings = statsapi.get('standings', {
        'season': SEASON,
        'sportIds': 1,
        'leagueId': 104
    })
    for record in standings.get('records', []):
        for team_record in record.get('teamRecords', []):
            if team_record['team']['id'] == TEAM_ID:
                rec = team_record.get('leagueRecord', {})
                return {
                    'wins': rec.get('wins', 0),
                    'losses': rec.get('losses', 0),
                    'pct': rec.get('pct', '.000'),
                    'gamesPlayed': team_record.get('gamesPlayed', 0),
                    'divisionRank': team_record.get('divisionRank', '-'),
                    'leagueRank': team_record.get('leagueRank', '-'),
                    'sportRank': team_record.get('sportRank', '-'),
                    'gamesBack': team_record.get('gamesBack', '-'),
                    'wildCardGamesBack': team_record.get('wildCardGamesBack', '-'),
                    'streak': team_record.get('streak', {}),
                    'homeRecord': _get_split_record(team_record, 'home'),
                    'awayRecord': _get_split_record(team_record, 'away'),
                    'lastUpdated': team_record.get('lastUpdated', ''),
                }
    return {}


def _get_split_record(team_record, split_type):
    """从 splitRecords 中提取主客场战绩"""
    for sr in team_record.get('records', {}).get('splitRecords', []):
        if sr.get('type') == split_type:
            return f"{sr.get('wins', 0)}-{sr.get('losses', 0)}"
    return '-'


def fetch_schedule(days=7):
    """获取接下来 N 天的赛程"""
    today = datetime.now()
    start = today.strftime('%Y-%m-%d')
    end = (today + timedelta(days=days)).strftime('%Y-%m-%d')
    schedule = statsapi.get('schedule', {
        'teamId': TEAM_ID,
        'sportId': 1,
        'startDate': start,
        'endDate': end,
        'hydrate': 'probablePitcher'
    })
    games = []
    for d in schedule.get('dates', []):
        for g in d.get('games', []):
            is_home = g['teams']['home']['team']['id'] == TEAM_ID
            opponent = g['teams']['away' if is_home else 'home']['team']
            status = g.get('status', {})
            game_info = {
                'gamePk': g.get('gamePk'),
                'date': d['date'],
                'time': g.get('gameDate', ''),
                'status': status.get('abstractGameState', 'Scheduled'),
                'detailedStatus': status.get('detailedState', 'Scheduled'),
                'isHome': is_home,
                'opponent': {
                    'id': opponent.get('id'),
                    'name': opponent.get('name', ''),
                    'abbreviation': _team_abbrev(opponent.get('name', '')),
                },
                'venue': g.get('venue', {}).get('name', ''),
            }
            # probable pitcher
            if is_home:
                pp = g.get('teams', {}).get('home', {}).get('probablePitcher', {})
                opp_pp = g.get('teams', {}).get('away', {}).get('probablePitcher', {})
            else:
                pp = g.get('teams', {}).get('away', {}).get('probablePitcher', {})
                opp_pp = g.get('teams', {}).get('home', {}).get('probablePitcher', {})
            if pp:
                game_info['probablePitcher'] = pp.get('fullName', '')
            if opp_pp:
                game_info['opponentProbablePitcher'] = opp_pp.get('fullName', '')
            # scores if final
            if status.get('abstractGameState') == 'Final':
                if is_home:
                    game_info['dodgersScore'] = g['teams']['home'].get('score', '-')
                    game_info['opponentScore'] = g['teams']['away'].get('score', '-')
                    game_info['result'] = _result(g['teams']['home']['score'], g['teams']['away']['score'])
                else:
                    game_info['dodgersScore'] = g['teams']['away'].get('score', '-')
                    game_info['opponentScore'] = g['teams']['home'].get('score', '-')
                    game_info['result'] = _result(g['teams']['away']['score'], g['teams']['home']['score'])
            games.append(game_info)
    return games


def _result(our_score, their_score):
    if our_score > their_score:
        return 'W'
    elif our_score < their_score:
        return 'L'
    return 'T'


def _team_abbrev(full_name):
    """简陋的球队简称映射"""
    mapping = {
        'Los Angeles Dodgers': 'LAD',
        'Pittsburgh Pirates': 'PIT',
        'Colorado Rockies': 'COL',
        'Milwaukee Brewers': 'MIL',
        'Kansas City Royals': 'KC',
        'San Diego Padres': 'SD',
        'San Francisco Giants': 'SF',
        'Arizona Diamondbacks': 'ARI',
        'New York Mets': 'NYM',
        'Atlanta Braves': 'ATL',
        'Philadelphia Phillies': 'PHI',
        'Miami Marlins': 'MIA',
        'Washington Nationals': 'WSH',
    }
    return mapping.get(full_name, full_name.split()[-1])


def fetch_last7_hitters():
    """获取最近 7 天打者数据"""
    today = datetime.now()
    week_ago = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    today_str = today.strftime('%Y-%m-%d')
    stats = statsapi.get('stats', {
        'stats': 'byDateRange',
        'season': SEASON,
        'group': 'hitting',
        'teamId': TEAM_ID,
        'startDate': week_ago,
        'endDate': today_str,
        'limit': 200
    })
    players = []
    if stats.get('stats'):
        for s in stats['stats'][0].get('splits', []):
            stat = s.get('stat', {})
            players.append({
                'name': s['player'].get('fullName', ''),
                'playerId': s['player'].get('id'),
                'games': stat.get('gamesPlayed', 0),
                'avg': stat.get('avg', '.000'),
                'obp': stat.get('obp', '.000'),
                'slg': stat.get('slg', '.000'),
                'ops': stat.get('ops', '.000'),
                'hr': stat.get('homeRuns', 0),
                'rbi': stat.get('rbi', 0),
                'sb': stat.get('stolenBases', 0),
                'so': stat.get('strikeOuts', 0),
                'bb': stat.get('baseOnBalls', 0),
                'pa': stat.get('plateAppearances', 0),
            })
    return players


def fetch_pitching_season():
    """获取投手赛季累计数据（用于轮值和牛棚）"""
    stats = statsapi.get('stats', {
        'stats': 'season',
        'season': SEASON,
        'group': 'pitching',
        'teamId': TEAM_ID,
        'limit': 200
    })
    pitchers = []
    if stats.get('stats'):
        for s in stats['stats'][0].get('splits', []):
            stat = s.get('stat', {})
            pitchers.append({
                'name': s['player'].get('fullName', ''),
                'playerId': s['player'].get('id'),
                'w': stat.get('wins', 0),
                'l': stat.get('losses', 0),
                'era': stat.get('era', '-.--'),
                'whip': stat.get('whip', '-.--'),
                'ip': stat.get('inningsPitched', '0'),
                'so': stat.get('strikeOuts', 0),
                'bb': stat.get('baseOnBalls', 0),
                'sv': stat.get('saves', 0),
                'hld': stat.get('holds', 0),
                'gs': stat.get('gamesStarted', 0),
                'k9': stat.get('strikeoutsPer9Inn', '-.--'),
                'bb9': stat.get('walksPer9Inn', '-.--'),
                'games': stat.get('gamesPlayed', 0),
            })
    return pitchers


def extract_weekly_redblack():
    """从最新周报中提取红榜/黑榜速览（匹配 Markdown 表格格式）"""
    try:
        files = sorted(WEEKLY_DIR.glob('*.md'), reverse=True)
        if not files:
            return {}
        latest = files[0]
        md = latest.read_text(encoding='utf-8')
        result = {
            'file': latest.name,
            'date': '',
            'weekRecord': '',
            'red': [],
            'black': [],
        }
        # 提取数据周期或日期
        m = re.search(r'数据周期：(\d{4}-\d{2}-\d{2} ~ \d{4}-\d{2}-\d{2})', md)
        if m:
            result['date'] = m.group(1)
        # 提取上周战绩
        m = re.search(r'\*\*上周战绩\*\*\s*\|\s*([^|]+)\|', md)
        if m:
            result['weekRecord'] = m.group(1).strip()

        def parse_table(section_title):
            """从 section 标题后解析 Markdown 表格行"""
            pattern = re.compile(
                r'###\s*' + re.escape(section_title) + r'.*?\n\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\s*\n\|[-:\|\s]+\|\s*\n(.*?)(?=###|##|<!-|\Z)',
                re.DOTALL
            )
            m = pattern.search(md)
            if not m:
                return []
            rows = []
            for line in m.group(1).strip().split('\n'):
                line = line.strip()
                if not line.startswith('|'):
                    continue
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if len(cells) < 5:
                    continue
                rank, player, position, data, analysis = cells[0], cells[1], cells[2], cells[3], cells[4]
                # 去掉 player 中的 Markdown 加粗
                player = re.sub(r'\*\*([^*]+)\*\*', r'\1', player).strip()
                rows.append({'name': player, 'note': f"{position} · {data}", 'detail': analysis})
            return rows

        result['red'] = parse_table('🔥 红榜')
        result['black'] = parse_table('🥶 黑榜')
        return result
    except Exception as e:
        print(f"[WARN] 周报解析失败: {e}")
        return {}


def write_json_atomic(path: Path, data: dict) -> bool:
    """原子写入：先写临时文件，成功后再替换；失败时保留旧 checkpoint。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix('.tmp')
    if path.exists():
        backup_path = path.with_suffix('.json.bak')
        try:
            shutil.copy2(path, backup_path)
        except Exception as e:
            print(f'[WARN] 备份旧数据失败: {e}')
    try:
        temp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        temp_path.replace(path)
        return True
    except Exception as e:
        print(f'[ERR] 写入数据失败: {e}')
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)
        return False


def load_existing_dashboard(path: Path) -> dict:
    """尝试读取现有 dashboard 数据作为 fallback。"""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None


def build_dashboard_data():
    data = {
        'generatedAt': datetime.now().isoformat(),
        'season': SEASON,
        'team': {
            'id': TEAM_ID,
            'name': 'Los Angeles Dodgers',
            'abbreviation': 'LAD',
        },
        'standings': safe_get(fetch_standings, {}),
        'schedule': safe_get(lambda: fetch_schedule(days=14), []),
        'last7Hitters': safe_get(fetch_last7_hitters, []),
        'seasonPitchers': safe_get(fetch_pitching_season, []),
        'weekly': safe_get(extract_weekly_redblack, {}),
    }
    return data


def main():
    print("[INFO] 正在抓取道奇数据大屏数据...")
    try:
        data = build_dashboard_data()
        if write_json_atomic(OUTPUT_FILE, data):
            print(f"[OK] 已保存 {OUTPUT_FILE}")
            print(f"     战绩: {data.get('standings', {}).get('wins', 0)}-{data.get('standings', {}).get('losses', 0)}")
            print(f"     未来赛程: {len(data.get('schedule', []))} 场")
            print(f"     最近7天热棒: {len(data.get('last7Hitters', []))} 人")
            print(f"     投手赛季数据: {len(data.get('seasonPitchers', []))} 人")
        else:
            print("[WARN] 写入新数据失败，保留上一次 checkpoint")
    except Exception as e:
        print(f"[ERR] 抓取数据失败: {e}")
        existing = load_existing_dashboard(OUTPUT_FILE)
        if existing:
            print(f"[OK] 保留旧 checkpoint（生成时间: {existing.get('generatedAt', '未知')}）")


if __name__ == '__main__':
    main()
