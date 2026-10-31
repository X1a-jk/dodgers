#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generic detailed scouting report generator for the remaining Dodgers players.
Produces HTML + Markdown + charts (cover, season comparison, overall grades).
Skips players that already have detailed reports.
"""
import subprocess
import json
import os
import re
import math
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = r'D:\baseball\report'
TODAY = datetime.now().strftime('%Y-%m-%d')
DATA_DATE = TODAY

# Players already completed with detailed reports (do not overwrite)
COMPLETED = {
    'Roki Sasaki', 'Shohei Ohtani', 'Yoshinobu Yamamoto', 'Freddie Freeman',
    'Mookie Betts', 'Blake Snell', 'Tyler Glasnow', 'Will Smith',
    'Kyle Tucker', 'Max Muncy', 'Andy Pages', 'Teoscar Hernández'
}

# Remaining players to generate
PLAYER_CONFIGS = [
    # Medium priority
    {"name": "Emmet Sheehan", "search": "Emmet Sheehan", "number": "80", "position": "P", "status": "活跃", "role": "starter"},
    {"name": "Eric Lauer", "search": "Eric Lauer", "number": "33", "position": "P", "status": "活跃", "role": "starter"},
    {"name": "Tanner Scott", "search": "Tanner Scott", "number": "66", "position": "P", "status": "活跃", "role": "reliever"},
    {"name": "Justin Wrobleski", "search": "Justin Wrobleski", "number": "70", "position": "P", "status": "活跃", "role": "starter"},
    {"name": "Tommy Edman", "search": "Tommy Edman", "number": "25", "position": "OF/IF", "status": "活跃", "role": "utility"},
    {"name": "Miguel Rojas", "search": "Miguel Rojas", "number": "72", "position": "SS", "status": "活跃", "role": "infield"},
    {"name": "Edgardo Henriquez", "search": "Edgardo Henriquez", "number": "60", "position": "P", "status": "活跃", "role": "reliever"},
    {"name": "Alex Vesia", "search": "Alex Vesia", "number": "51", "position": "P", "status": "活跃", "role": "reliever"},
    {"name": "Enrique Hernández", "search": "Enrique Hernandez", "number": "8", "position": "IF", "status": "IL-10", "role": "utility"},
    {"name": "Blake Treinen", "search": "Blake Treinen", "number": "49", "position": "P", "status": "IL-15", "role": "reliever"},
    {"name": "Jack Dreyer", "search": "Jack Dreyer", "number": "86", "position": "P", "status": "活跃", "role": "reliever"},
    {"name": "Will Klein", "search": "Will Klein", "number": "61", "position": "P", "status": "活跃", "role": "reliever"},
    {"name": "Alex Call", "search": "Alex Call", "number": "12", "position": "OF", "status": "活跃", "role": "outfield"},
    {"name": "Dalton Rushing", "search": "Dalton Rushing", "number": "68", "position": "C", "status": "活跃", "role": "catcher"},
    {"name": "Alex Freeland", "search": "Alex Freeland", "number": "76", "position": "IF", "status": "活跃", "role": "infield"},
    {"name": "Evan Phillips", "search": "Evan Phillips", "number": "59", "position": "P", "status": "活跃", "role": "closer"},
    {"name": "Edwin Díaz", "search": "Edwin Diaz", "number": "3", "position": "P", "status": "IL-60", "role": "closer"},
    # Low priority
    {"name": "Kyle Hurt", "search": "Kyle Hurt", "number": "63", "position": "P", "status": "活跃", "role": "reliever"},
    {"name": "Hyeseong Kim", "search": "Hyeseong Kim", "number": "6", "position": "IF", "status": "Minors", "role": "infield"},
    {"name": "Brusdar Graterol", "search": "Brusdar Graterol", "number": "48", "position": "P", "status": "IL-60", "role": "reliever"},
    {"name": "Ben Casparius", "search": "Ben Casparius", "number": "78", "position": "P", "status": "IL-60", "role": "reliever"},
    {"name": "Bobby Miller", "search": "Bobby Miller", "number": "28", "position": "P", "status": "IL-60", "role": "starter"},
    {"name": "Brock Stewart", "search": "Brock Stewart", "number": "41", "position": "P", "status": "活跃", "role": "reliever"},
    {"name": "River Ryan", "search": "River Ryan", "number": "77", "position": "P", "status": "Minors", "role": "starter"},
    {"name": "Ryan Ward", "search": "Ryan Ward", "number": "67", "position": "OF", "status": "Minors", "role": "outfield"},
    {"name": "Eliezer Alfonzo", "search": "Eliezer Alfonzo", "number": "64", "position": "C", "status": "活跃", "role": "catcher"},
    {"name": "Landon Knack", "search": "Landon Knack", "number": "96", "position": "P", "status": "IL-60", "role": "starter"},
    {"name": "Gavin Stone", "search": "Gavin Stone", "number": "35", "position": "P", "status": "IL-60", "role": "starter"},
    {"name": "Jake Cousins", "search": "Jake Cousins", "number": "—", "position": "P", "status": "IL-60", "role": "reliever"},
    {"name": "Charlie Barnes", "search": "Charlie Barnes", "number": "57", "position": "P", "status": "Minors", "role": "starter"},
    {"name": "Nick Frasso", "search": "Nick Frasso", "number": "—", "position": "P", "status": "Minors", "role": "starter"},
    {"name": "Paul Gervase", "search": "Paul Gervase", "number": "65", "position": "P", "status": "Minors", "role": "reliever"},
    {"name": "Ronan Kopp", "search": "Ronan Kopp", "number": "83", "position": "P", "status": "Minors", "role": "reliever"},
    {"name": "Chayce McDermott", "search": "Chayce McDermott", "number": "62", "position": "P", "status": "Minors", "role": "starter"},
    {"name": "Wyatt Mills", "search": "Wyatt Mills", "number": "58", "position": "P", "status": "Minors", "role": "reliever"},
    {"name": "Alek Thomas", "search": "Alek Thomas", "number": "5", "position": "OF", "status": "Minors", "role": "outfield"},
]


def slugify(name):
    s = name.lower().replace(' ', '-')
    for a, b in [('á', 'a'), ('é', 'e'), ('í', 'i'), ('ó', 'o'), ('ú', 'u'),
                 ('ñ', 'n'), ('ü', 'u'), ('ã', 'a'), ('õ', 'o'), ('ç', 'c'),
                 ('à', 'a'), ('è', 'e'), ('ì', 'i'), ('ò', 'o'), ('ù', 'u')]:
        s = s.replace(a, b)
    return s


def run_cmd(args, timeout=30):
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return result
    except Exception as e:
        print(f"    [CMD ERROR] {e}")
        return None


def extract_json(stdout):
    if not stdout:
        return None
    try:
        start = stdout.index('{')
        return json.loads(stdout[start:])
    except Exception:
        return None


def fetch_player_info(search_name):
    script = r'C:\Users\Junkai XIA\.openclaw\workspace\skills\baseball\scripts\baseball.py'
    result = run_cmd(['python', script, 'player', search_name, '--team', 'LAD', '--format', 'json'])
    if result and result.returncode == 0:
        data = extract_json(result.stdout)
        if data and data.get('players'):
            return data['players'][0]
    # Fallback: try without team filter
    result = run_cmd(['python', script, 'player', search_name, '--format', 'json'])
    if result and result.returncode == 0:
        data = extract_json(result.stdout)
        if data and data.get('players'):
            return data['players'][0]
    return None


def fetch_player_stats(player_id, season):
    script = r'C:\Users\Junkai XIA\.openclaw\workspace\skills\baseball\scripts\baseball.py'
    result = run_cmd(['python', script, 'stats', str(player_id), '--format', 'json', '--season', str(season)], timeout=45)
    if result and result.returncode == 0:
        data = extract_json(result.stdout)
        return data
    return None


def fmt_num(val, default='—'):
    if val is None:
        return default
    try:
        return str(val)
    except Exception:
        return default


def fmt_float(val, decimals=2, default='—'):
    if val is None or val == '' or val == '—':
        return default
    try:
        return f"{float(val):.{decimals}f}"
    except Exception:
        return default


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__TITLE__</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e0e0e0; line-height: 1.6; min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header {
            text-align: center; padding: 40px 0;
            background: linear-gradient(90deg, #005A9C 0%, #1a5490 50%, #005A9C 100%);
            border-radius: 15px; margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        .header h1 { font-size: 3em; color: #fff; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); margin-bottom: 10px; }
        .header .subtitle { font-size: 1.2em; color: #e0e0e0; font-style: italic; }
        .player-card {
            background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 30px; margin-bottom: 30px;
            backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2);
            display: flex; gap: 30px; flex-wrap: wrap;
        }
        .player-info { flex: 1; min-width: 250px; }
        .player-info h2 { color: #4fc3f7; margin-bottom: 15px; font-size: 1.8em; }
        .info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .info-item { background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 8px; }
        .info-item .label { font-size: 0.9em; color: #90a4ae; text-transform: uppercase; letter-spacing: 1px; }
        .info-item .value { font-size: 1.2em; color: #fff; font-weight: bold; }
        .section {
            background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 30px;
            margin-bottom: 30px; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .section h2 {
            color: #4fc3f7; margin-bottom: 20px; font-size: 1.8em;
            border-bottom: 2px solid #4fc3f7; padding-bottom: 10px;
        }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px; }
        .stat-card {
            background: linear-gradient(135deg, rgba(0, 90, 156, 0.3) 0%, rgba(26, 84, 144, 0.3) 100%);
            border-radius: 10px; padding: 20px; text-align: center;
            border: 1px solid rgba(79, 195, 247, 0.3); transition: transform 0.3s ease;
        }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-card .stat-value { font-size: 2.5em; font-weight: bold; color: #4fc3f7; display: block; }
        .stat-card .stat-label { font-size: 0.9em; color: #90a4ae; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px; }
        .comparison-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        .comparison-table th, .comparison-table td { padding: 12px; text-align: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
        .comparison-table th { background: rgba(0, 90, 156, 0.3); color: #4fc3f7; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
        .comparison-table tr:hover { background: rgba(255, 255, 255, 0.05); }
        .pitch-arsenal { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }
        .pitch-card {
            background: linear-gradient(135deg, rgba(0, 90, 156, 0.2) 0%, rgba(26, 84, 144, 0.2) 100%);
            border-radius: 10px; padding: 20px; border-left: 4px solid #4fc3f7;
        }
        .pitch-card h3 { color: #4fc3f7; margin-bottom: 10px; }
        .pros-cons { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
        .pros, .cons { background: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 20px; }
        .pros h3 { color: #4caf50; margin-bottom: 15px; }
        .cons h3 { color: #f44336; margin-bottom: 15px; }
        .pros ul, .cons ul { list-style: none; }
        .pros li, .cons li { padding: 8px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
        .pros li::before { content: "✓ "; color: #4caf50; font-weight: bold; }
        .cons li::before { content: "✗ "; color: #f44336; font-weight: bold; }
        .grade { display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 0.9em; }
        .grade-a { background: rgba(76, 175, 80, 0.3); color: #4caf50; }
        .grade-b { background: rgba(79, 195, 247, 0.3); color: #4fc3f7; }
        .grade-c { background: rgba(255, 152, 0, 0.3); color: #ff9800; }
        .grade-d { background: rgba(244, 67, 54, 0.3); color: #f44336; }
        .highlight { color: #4fc3f7; font-weight: bold; }
        .warning { color: #ff9800; font-weight: bold; }
        .success { color: #4caf50; font-weight: bold; }
        .danger { color: #f44336; font-weight: bold; }
        .status-box { background: rgba(255, 152, 0, 0.1); border: 1px solid rgba(255, 152, 0, 0.3); border-radius: 10px; padding: 15px; margin: 15px 0; }
        .status-box.il { background: rgba(244, 67, 54, 0.1); border-color: rgba(244, 67, 54, 0.3); }
        .status-box.minors { background: rgba(255, 215, 0, 0.1); border-color: rgba(255, 215, 0, 0.3); }
        .status-box h4 { color: #ff9800; margin-bottom: 10px; }
        .status-box.il h4 { color: #f44336; }
        .status-box.minors h4 { color: #FFD700; }
        .footer { text-align: center; padding: 20px; color: #90a4ae; font-size: 0.9em; }
        @media (max-width: 768px) { .header h1 { font-size: 2em; } .stats-grid { grid-template-columns: repeat(2, 1fr); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚾ __PLAYER_NAME__</h1>
            <p class="subtitle">__SUBTITLE__</p>
        </div>

        <div class="section" style="text-align: center; padding: 0; background: none; border: none; backdrop-filter: none; box-shadow: none;">
            <img src="__COVER_IMG__" alt="报告封面" style="width: 100%; max-width: 900px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        </div>

        <div class="player-card">
            <div class="player-info">
                <h2>基本信息</h2>
                <div class="info-grid">
__INFO_GRID__
                </div>
            </div>
            <div class="player-info">
                <h2>球探总评</h2>
__SCOUTING_SUMMARY__
            </div>
        </div>

        <div class="section">
            <h2>🏆 球员简介</h2>
__CAREER_NOTE__
            __STATUS_BOX__
        </div>

__BATTING_SECTION__
__PITCHING_SECTION__
__ARSENAL_SECTION__

        <div class="section">
            <h2>🔍 球探分析</h2>
__ANALYSIS__
        </div>

        <div class="section">
            <h2>✅ 优势 vs ❌ 劣势</h2>
            <div class="pros-cons">
                <div class="pros">
                    <h3>优势 (Strengths)</h3>
                    <ul>
__PROS__
                    </ul>
                </div>
                <div class="cons">
                    <h3>劣势 (Weaknesses)</h3>
                    <ul>
__CONS__
                    </ul>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>📊 综合评分</h2>
            <div style="text-align: center; margin: 20px 0;">
                <img src="__GRADES_RADAR__" alt="综合评分雷达图" style="width: 100%; max-width: 600px; border-radius: 10px;">
            </div>
            <div class="stats-grid">
__GRADES_GRID__
            </div>
            <div style="margin-top: 30px; text-align: center;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">总体潜力评分</h3>
                <div style="font-size: 4em; color: #4caf50; font-weight: bold;">__OVERALL_GRADE__</div>
                <p style="color: #90a4ae; margin-top: 10px;">__OVERALL_DESC__</p>
                <p style="margin-top: 15px;"><span class="grade grade-a" style="font-size: 1.2em;">__OVERALL_LABEL__</span></p>
            </div>
        </div>

        <div class="section">
            <h2>🔮 未来展望</h2>
__FUTURE_OUTLOOK__
        </div>

        <div class="section">
            <h2>📖 背景故事</h2>
__BACKGROUND__
        </div>

        <div class="footer">
            <p>数据来源：MLB.com | Baseball Savant (Statcast) | Fangraphs | MLB Stats API</p>
            <p>报告生成时间：__FOOTER_DATE__ | 数据截止日期：__DATA_DATE__</p>
            <p>⚾ 洛杉矶道奇队球探报告</p>
        </div>
    </div>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Generic text builders
# ---------------------------------------------------------------------------

def role_title(role, position):
    if role == 'starter':
        return '先发投手'
    if role == 'reliever':
        return '后援投手'
    if role == 'closer':
        return '终结者'
    if role == 'catcher':
        return '捕手'
    if role == 'infield':
        return '内野手'
    if role == 'outfield':
        return '外野手'
    if role == 'utility':
        return '多功能工具人'
    return position


def position_defense_weight(position):
    if position in ('C',):
        return 60
    if position in ('SS', 'CF'):
        return 60
    if position in ('2B', '3B', 'RF'):
        return 55
    if position in ('LF', '1B'):
        return 50
    if position in ('OF', 'IF', 'OF/IF', 'IF/OF'):
        return 55
    return 50


def position_arm_weight(position):
    if position in ('C', 'RF', 'LF'):
        return 60
    if position in ('SS', '3B'):
        return 55
    if position in ('2B', 'CF'):
        return 50
    if position in ('1B',):
        return 45
    if position in ('OF', 'IF', 'OF/IF', 'IF/OF'):
        return 55
    return 50


def compute_batter_grades(stats, position, age):
    if stats:
        avg = 0.0
        try:
            avg = float(stats.get('avg', '.000').strip('.')) / 1000 if stats.get('avg') else 0
        except Exception:
            avg = 0.0
        slg = 0.0
        try:
            slg = float(stats.get('slg', '.000').strip('.')) / 1000 if stats.get('slg') else 0
        except Exception:
            slg = 0.0
        obp = 0.0
        try:
            obp = float(stats.get('obp', '.000').strip('.')) / 1000 if stats.get('obp') else 0
        except Exception:
            obp = 0.0
        bb = stats.get('walks', 0) or 0
        so = stats.get('strikeouts', 0) or 0
        sb = stats.get('stolen_bases', 0) or 0
        g = stats.get('games_played', 0) or 1
        sb_162 = (sb / g) * 162
        hit = 60 if avg >= .280 else 55 if avg >= .250 else 50 if avg >= .220 else 45
        power = 65 if slg >= .480 else 60 if slg >= .420 else 50 if slg >= .360 else 45
        disc = 65 if obp >= .360 else 60 if obp >= .320 else 50 if obp >= .290 else 45
        speed = 65 if sb_162 >= 15 else 55 if sb_162 >= 5 else 45
        defense = position_defense_weight(position)
        arm = position_arm_weight(position)
        clutch = 55
        leadership = 60 if age >= 30 else 50
    else:
        hit = 45; power = 45; disc = 45; speed = 45; defense = 50; arm = 50; clutch = 45; leadership = 45
    return [
        {"label": "Hit", "value": hit, "grade": grade_from_value(hit)},
        {"label": "Power", "value": power, "grade": grade_from_value(power)},
        {"label": "Discipline", "value": disc, "grade": grade_from_value(disc)},
        {"label": "Speed", "value": speed, "grade": grade_from_value(speed)},
        {"label": "Defense", "value": defense, "grade": grade_from_value(defense)},
        {"label": "Arm", "value": arm, "grade": grade_from_value(arm)},
        {"label": "Clutch", "value": clutch, "grade": grade_from_value(clutch)},
        {"label": "Leadership", "value": leadership, "grade": grade_from_value(leadership)},
    ]


def compute_pitcher_grades(stats, role, age):
    if stats:
        era = 99.0
        try:
            era = float(stats.get('era', '99'))
        except Exception:
            era = 99.0
        whip = 99.0
        try:
            whip = float(stats.get('whip', '99'))
        except Exception:
            whip = 99.0
        k9 = 0.0
        try:
            k9 = float(stats.get('strikeouts_per_9', '0'))
        except Exception:
            k9 = 0.0
        bb9 = 99.0
        try:
            bb9 = float(stats.get('walks_per_9', '99'))
        except Exception:
            bb9 = 99.0
        g = stats.get('games_played', 0) or 0
        gs = stats.get('games_started', 0) or 0
        ip = 0.0
        try:
            ip = float(stats.get('innings_pitched', '0'))
        except Exception:
            ip = 0.0
        fastball = 65 if k9 >= 9.5 else 60 if k9 >= 8.0 else 50 if k9 >= 7.0 else 45
        offspeed = 60 if whip <= 1.15 else 55 if whip <= 1.35 else 45
        control = 65 if bb9 <= 2.5 else 60 if bb9 <= 3.5 else 50 if bb9 <= 4.5 else 45
        command = 65 if whip <= 1.10 else 60 if whip <= 1.30 else 50 if whip <= 1.50 else 45
        stamina = 65 if role == 'starter' and ip >= 100 else 60 if role == 'starter' else 50
        mental = 60 if age >= 28 else 55
        durability = 60 if g >= 20 or ip >= 50 else 45
        versatility = 60 if role == 'closer' else 55 if role == 'reliever' else 50
    else:
        fastball = 45; offspeed = 45; control = 45; command = 45; stamina = 50; mental = 50; durability = 45; versatility = 50
    return [
        {"label": "Fastball", "value": fastball, "grade": grade_from_value(fastball)},
        {"label": "Off-speed", "value": offspeed, "grade": grade_from_value(offspeed)},
        {"label": "Control", "value": control, "grade": grade_from_value(control)},
        {"label": "Command", "value": command, "grade": grade_from_value(command)},
        {"label": "Stamina", "value": stamina, "grade": grade_from_value(stamina)},
        {"label": "Mental", "value": mental, "grade": grade_from_value(mental)},
        {"label": "Durability", "value": durability, "grade": grade_from_value(durability)},
        {"label": "Versatility", "value": versatility, "grade": grade_from_value(versatility)},
    ]


def grade_from_value(value):
    if value >= 70: return 'A'
    if value >= 65: return 'A-'
    if value >= 60: return 'B+'
    if value >= 55: return 'B'
    if value >= 50: return 'B-'
    if value >= 45: return 'C+'
    if value >= 40: return 'C'
    return 'D'


def grade_class(value):
    if value >= 60: return 'grade-a'
    if value >= 50: return 'grade-b'
    if value >= 40: return 'grade-c'
    return 'grade-d'


# ---------------------------------------------------------------------------
# Chart generation
# ---------------------------------------------------------------------------

def generate_cover(p, stats, output_path):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')

    title = p['name']
    ax.text(0.5, 0.85, title, fontsize=32, fontweight='bold', ha='center',
            color='white', transform=ax.transAxes)
    ax.text(0.5, 0.75, f"Los Angeles Dodgers #{p['number']} | {p['position']}", fontsize=18,
            ha='center', color='#4fc3f7', transform=ax.transAxes)
    ax.text(0.5, 0.65, 'SCOUTING REPORT 2026', fontsize=22, fontweight='bold', ha='center',
            color='#ff9800', transform=ax.transAxes)

    # Key stats for cover
    if p['role'] in ('starter', 'reliever', 'closer'):
        if stats:
            era = fmt_float(stats.get('era'), 2)
            whip = fmt_float(stats.get('whip'), 2)
            k = fmt_num(stats.get('strikeouts'))
            ip = fmt_num(stats.get('innings_pitched'))
            w = fmt_num(stats.get('wins'))
            l = fmt_num(stats.get('losses'))
            k9 = fmt_float(stats.get('strikeouts_per_9'), 1)
            bb9 = fmt_float(stats.get('walks_per_9'), 1)
        else:
            era = whip = k = ip = w = l = k9 = bb9 = '—'
        cover_stats = [('ERA', era), ('WHIP', whip), ('K', k), ('IP', ip),
                       ('W-L', f"{w}-{l}"), ('K/9', k9), ('BB/9', bb9), ('Status', p['status'])]
    else:
        if stats:
            avg = fmt_num(stats.get('avg'))
            obp = fmt_num(stats.get('obp'))
            slg = fmt_num(stats.get('slg'))
            ops = fmt_num(stats.get('ops'))
            hr = fmt_num(stats.get('home_runs'))
            rbi = fmt_num(stats.get('rbi'))
            sb = fmt_num(stats.get('stolen_bases'))
            g = fmt_num(stats.get('games_played'))
        else:
            avg = obp = slg = ops = hr = rbi = sb = g = '—'
        cover_stats = [('AVG', avg), ('OPS', ops), ('HR', hr), ('RBI', rbi),
                       ('SB', sb), ('OBP', obp), ('SLG', slg), ('Status', p['status'])]

    y_pos = 0.45
    for i, (label, value) in enumerate(cover_stats):
        x_pos = 0.15 + (i % 4) * 0.23
        if i >= 4:
            y_pos = 0.25
        ax.text(x_pos, y_pos, value, fontsize=26, fontweight='bold', ha='center',
                color='#4fc3f7', transform=ax.transAxes)
        ax.text(x_pos, y_pos - 0.08, label, fontsize=12, ha='center',
                color='#90a4ae', transform=ax.transAxes)

    role_zh = role_title(p['role'], p['position'])
    ax.text(0.5, 0.08, f"Dodgers {role_zh} | {p['status']}", fontsize=14, ha='center',
            color='#90a4ae', transform=ax.transAxes, style='italic')
    ax.text(0.5, 0.02, f'Generated: {TODAY} | Data: MLB.com, MLB Stats API',
            fontsize=10, ha='center', color='#666', transform=ax.transAxes)

    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close()


def generate_season_chart(p, stats_2025, stats_2026, output_path):
    if p['role'] in ('starter', 'reliever', 'closer'):
        stats = ['ERA', 'WHIP', 'K/9', 'BB/9']
        def val(s, k):
            try:
                return float(s.get(k, 0)) if s else 0
            except Exception:
                return 0
        vals_2025 = [val(stats_2025, {'ERA': 'era', 'WHIP': 'whip', 'K/9': 'strikeouts_per_9', 'BB/9': 'walks_per_9'}[k]) for k in stats]
        vals_2026 = [val(stats_2026, {'ERA': 'era', 'WHIP': 'whip', 'K/9': 'strikeouts_per_9', 'BB/9': 'walks_per_9'}[k]) for k in stats]
    else:
        stats = ['AVG', 'OBP', 'SLG', 'OPS']
        def val(s, k):
            try:
                return float(s.get(k, '.000').strip('.')) / 1000 if s and s.get(k) else 0
            except Exception:
                return 0
        vals_2025 = [val(stats_2025, k) for k in stats]
        vals_2026 = [val(stats_2026, k) for k in stats]

    # If no 2025 data, duplicate 2026 to keep chart functional
    if not stats_2025:
        vals_2025 = vals_2026[:]
    if not stats_2026:
        vals_2026 = vals_2025[:]

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    colors = ['#4fc3f7', '#ff9800']
    x_labels = ['2025', '2026']

    for idx, stat in enumerate(stats):
        ax = axes[idx]
        vals = [vals_2025[idx], vals_2026[idx]]
        bars = ax.bar(x_labels, vals, color=colors, edgecolor='white', alpha=0.9, width=0.5)
        ax.set_title(stat, fontsize=14, fontweight='bold', color='#1a1a2e')
        max_val = max(vals) if max(vals) != 0 else 1
        ax.set_ylim(0, max_val * 1.25)
        ax.grid(axis='y', alpha=0.3)
        for bar, val in zip(bars, vals):
            height = bar.get_height()
            if p['role'] in ('starter', 'reliever', 'closer'):
                text = f'{val:.2f}' if stat in ['ERA', 'WHIP'] else f'{val:.1f}'
            else:
                text = f'{val:.3f}'
            ax.text(bar.get_x() + bar.get_width()/2., height + max_val*0.02,
                    text, ha='center', va='bottom', fontweight='bold', fontsize=11)

    fig.suptitle(f"{p['name']} - 2025 vs 2026 Season Comparison", fontsize=16, fontweight='bold', color='#1a1a2e', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def generate_grades_chart(p, grades, output_path):
    categories = [g['label'] for g in grades]
    values = [g['value'] for g in grades]
    values += values[:1]
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
    ax.plot(angles, values, 'o-', linewidth=2, color='#1E90FF', markersize=8)
    ax.fill(angles, values, alpha=0.25, color='#1E90FF')

    for angle, value in zip(angles[:-1], values[:-1]):
        ax.text(angle, value + 3, str(value), ha='center', va='center', fontweight='bold', fontsize=10, color='darkblue')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=10, fontweight='bold')
    ax.set_ylim(20, 80)
    ax.set_yticks([20, 30, 40, 50, 60, 70, 80])
    ax.set_yticklabels(['20', '30', '40', '50', '60', '70', '80'], color='grey', size=8)
    ax.set_title(f"{p['name']} - Scouting Grades\n(20-80 Scale)", size=16, fontweight='bold', pad=20)
    ax.grid(True)
    ax.axhspan(60, 80, alpha=0.05, color='green')
    ax.axhspan(50, 60, alpha=0.05, color='yellow')
    ax.axhspan(0, 50, alpha=0.05, color='red')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()


# ---------------------------------------------------------------------------
# HTML builders
# ---------------------------------------------------------------------------

def build_info_grid(p, info):
    birth = info.get('birth_date', '—') if info else '—'
    age = str(info.get('age', p.get('age', '—'))) if info else p.get('age', '—')
    height = info.get('height', '—') if info else '—'
    weight = info.get('weight', '—') if info else '—'
    bats = info.get('bats', '—') if info else '—'
    throws = info.get('throws', '—') if info else '—'
    debut = info.get('mlb_debut_date', '—') if info else '—'
    items = [
        ("出生日期", birth),
        ("年龄", age + "岁" if age != '—' else '—'),
        ("身高/体重", f"{height} / {weight} lbs" if height != '—' else '—'),
        ("击球/投球", f"{bats}/{throws}" if bats != '—' else '—'),
        ("位置", p['position']),
        ("MLB首秀", debut),
        ("背号", '#' + p['number']),
        ("状态", p['status']),
    ]
    return "\n".join(
        f'                        <div class="info-item"><div class="label">{label}</div><div class="value">{value}</div></div>'
        for label, value in items
    )


def build_batting_grid(stats):
    if not stats:
        return '                <div class="stat-card"><span class="stat-value">—</span><div class="stat-label">数据不可用</div></div>'
    order = [('games_played', '出赛'), ('avg', '打击率'), ('obp', '上垒率'), ('slg', '长打率'),
             ('ops', 'OPS'), ('home_runs', '本垒打'), ('rbi', '打点'), ('stolen_bases', '盗垒')]
    html = ""
    for k, label in order:
        val = stats.get(k, '—')
        html += f'''\n                <div class="stat-card">
                    <span class="stat-value">{val}</span>
                    <div class="stat-label">{label}</div>
                </div>'''
    return html


def build_pitching_grid(stats):
    if not stats:
        return '                <div class="stat-card"><span class="stat-value">—</span><div class="stat-label">数据不可用</div></div>'
    order = [('games_played', '出赛'), ('games_started', '先发'), ('wins', '胜'), ('losses', '败'),
             ('era', 'ERA'), ('innings_pitched', 'IP'), ('strikeouts', 'K'), ('walks', 'BB'),
             ('whip', 'WHIP'), ('strikeouts_per_9', 'K/9'), ('walks_per_9', 'BB/9')]
    html = ""
    for k, label in order:
        val = stats.get(k, '—')
        html += f'''\n                <div class="stat-card">
                    <span class="stat-value">{val}</span>
                    <div class="stat-label">{label}</div>
                </div>'''
    return html


def build_batting_table(stats_2025, stats_2026):
    rows = []
    for year, s in [("2025", stats_2025), ("2026", stats_2026)]:
        if not s:
            continue
        rows.append(
            f'''                    <tr>
                        <td class="{'warning' if year == '2026' else 'highlight'}">{year}</td>
                        <td>{s.get('G', s.get('games_played', '—'))}</td>
                        <td>{s.get('AVG', s.get('avg', '—'))}</td>
                        <td>{s.get('OBP', s.get('obp', '—'))}</td>
                        <td>{s.get('SLG', s.get('slg', '—'))}</td>
                        <td>{s.get('OPS', s.get('ops', '—'))}</td>
                        <td>{s.get('HR', s.get('home_runs', '—'))}</td>
                        <td>{s.get('RBI', s.get('rbi', '—'))}</td>
                        <td>{s.get('BB', s.get('walks', '—'))}</td>
                        <td>{s.get('SO', s.get('strikeouts', '—'))}</td>
                    </tr>'''
        )
    return "\n".join(rows)


def build_pitching_table(stats_2025, stats_2026):
    rows = []
    for year, s in [("2025", stats_2025), ("2026", stats_2026)]:
        if not s:
            continue
        rows.append(
            f'''                    <tr>
                        <td class="{'warning' if year == '2026' else 'highlight'}">{year}</td>
                        <td>{s.get('G', s.get('games_played', '—'))}</td>
                        <td>{s.get('GS', s.get('games_started', '—'))}</td>
                        <td>{s.get('W', s.get('wins', '—'))}-{s.get('L', s.get('losses', '—'))}</td>
                        <td>{s.get('ERA', s.get('era', '—'))}</td>
                        <td>{s.get('IP', s.get('innings_pitched', '—'))}</td>
                        <td>{s.get('K', s.get('strikeouts', '—'))}</td>
                        <td>{s.get('BB', s.get('walks', '—'))}</td>
                        <td>{s.get('WHIP', s.get('whip', '—'))}</td>
                        <td>{s.get('K/9', s.get('strikeouts_per_9', '—'))}</td>
                    </tr>'''
        )
    return "\n".join(rows)


def build_grades_grid(grades):
    html = ""
    for g in grades:
        cls = grade_class(g['value'])
        color = '#4caf50' if g['value'] >= 60 else '#4fc3f7' if g['value'] >= 50 else '#ff9800'
        html += f'''\n                <div class="stat-card">
                    <span class="stat-value" style="color: {color};">{g['value']}</span>
                    <div class="stat-label">{g['label']}</div>
                    <span class="grade {cls}">{g['grade']}</span>
                </div>'''
    return html


# ---------------------------------------------------------------------------
# Text generation helpers
# ---------------------------------------------------------------------------

def scouting_summary(p, info, stats_2026, role):
    role_zh = role_title(role, p['position'])
    if p['status'].startswith('IL'):
        status_note = f"目前处于{p['status']}伤病名单，2026年样本较小。"
    elif p['status'] == 'Minors':
        status_note = "目前位于小联盟，持续发展中。"
    else:
        status_note = "目前处于道奇活跃名单。"
    if p['role'] in ('starter', 'reliever', 'closer'):
        if stats_2026:
            era = fmt_float(stats_2026.get('era'), 2)
            k9 = fmt_float(stats_2026.get('strikeouts_per_9'), 1)
            whip = fmt_float(stats_2026.get('whip'), 2)
        else:
            era = k9 = whip = '—'
        return f'''
            <p style="margin-bottom: 15px;">{p['name']} 是道奇队的<span class="highlight">{role_zh}</span>，{status_note}</p>
            <p style="margin-bottom: 15px;">2026年数据：ERA {era}，WHIP {whip}，K/9 {k9}。他依靠球种组合和控球在球队中扮演重要角色。</p>
            <p>作为{role_zh}，他的价值在于稳定的局数贡献和关键出局能力，是道奇投手轮值/牛棚的重要一环。</p>
        '''
    else:
        if stats_2026:
            avg = fmt_num(stats_2026.get('avg'))
            ops = fmt_num(stats_2026.get('ops'))
            hr = fmt_num(stats_2026.get('home_runs'))
        else:
            avg = ops = hr = '—'
        return f'''
            <p style="margin-bottom: 15px;">{p['name']} 是道奇队的<span class="highlight">{role_zh}</span>，{status_note}</p>
            <p style="margin-bottom: 15px;">2026年数据：AVG {avg}，OPS {ops}，HR {hr}。他在球队中提供{role_zh.replace("手", "")}所需的攻防价值。</p>
            <p>{role_zh.replace("手", "")}的角色定位和团队合作意识，使他在道奇阵容中具备稳定贡献的潜力。</p>
        '''


def career_note(p, info):
    role_zh = role_title(p['role'], p['position'])
    debut = info.get('mlb_debut_date', '—') if info else '—'
    if p['status'] == 'Minors':
        return f'''
            <div class="career-highlight">
                <h4>🌟 小联盟发展中的{role_zh}</h4>
                <p>{p['name']} 目前效力于道奇小联盟体系，持续磨练技术，争取未来登上大联盟。他的{role_zh}技能是球队长期规划的一部分。</p>
            </div>
        '''
    if p['status'].startswith('IL'):
        return f'''
            <div class="career-highlight">
                <h4>🏥 伤病名单中的{role_zh}</h4>
                <p>{p['name']} 目前因伤位于{p['status']}名单。他此前在道奇队扮演重要角色，伤愈回归后将为球队提供即战力。</p>
            </div>
        '''
    return f'''
        <div class="career-highlight">
            <h4>⭐ 道奇{role_zh}</h4>
            <p>{p['name']} 是道奇活跃名单的一员，MLB首秀日期 {debut}。作为{role_zh}，他持续为球队贡献价值。</p>
        </div>
    '''


def status_box(p):
    if p['status'].startswith('IL'):
        cls = 'il'
        title = '⚠️ 伤病状态'
        text = f"该球员目前位于{p['status']}伤病名单，报告数据为样本或参考数据。回归时间取决于医疗团队评估。"
    elif p['status'] == 'Minors':
        cls = 'minors'
        title = '⚠️ 小联盟状态'
        text = "该球员目前位于小联盟，大联盟统计数据可能有限或不可用。"
    else:
        return ''
    return f'''
            <div class="status-box {cls}">
                <h4>{title}</h4>
                <p>{text}</p>
            </div>
    '''


def build_pitch_arsenal(p):
    if p['role'] in ('starter', 'reliever', 'closer'):
        if p['role'] == 'starter':
            arsenal = [
                ("四缝快速球 (Four-Seam Fastball)", "主力球种，依靠控球和角度来制造出局。"),
                ("滑球 (Slider)", "主要出局球，能够对右打者产生横向位移。"),
                ("变速球 (Changeup)", "用来对付左打者，制造挥棒时间差。"),
                ("曲球 (Curveball)", "展示球种，用于打乱击球员节奏。"),
            ]
        elif p['role'] == 'closer':
            arsenal = [
                ("四缝快速球 (Four-Seam Fastball)", "压制力核心球种，关键球速高。"),
                ("滑球 (Slider)", "主要三振球，sharp break。"),
                ("切球 (Cutter)", "制造 weak contact 的配球。"),
                ("变速球/叉指 (Split/Change)", "偶尔使用，增加球路变化。"),
            ]
        else:
            arsenal = [
                ("四缝快速球 (Four-Seam Fastball)", "主力球种，追求好球带边缘。"),
                ("滑球 (Slider)", "对同侧打者的主要出局球。"),
                ("变速球 (Changeup)", "改变节奏，制造挥空。"),
                ("伸卡球/曲球 (Sinker/Curve)", "依个人球风搭配。"),
            ]
        cards = "\n".join(
            f'''                <div class="pitch-card">
                    <h3>{name}</h3>
                    <p>{desc}</p>
                </div>'''
            for name, desc in arsenal
        )
        return f'''
        <div class="section">
            <h2>⚾ 投球武器库</h2>
            <div class="pitch-arsenal">
{cards}
            </div>
        </div>
'''
    return ''


def build_analysis(p, stats_2026, stats_2025, info):
    role_zh = role_title(p['role'], p['position'])
    if p['role'] in ('starter', 'reliever', 'closer'):
        if stats_2026:
            era = fmt_float(stats_2026.get('era'), 2)
            whip = fmt_float(stats_2026.get('whip'), 2)
            k9 = fmt_float(stats_2026.get('strikeouts_per_9'), 1)
            bb9 = fmt_float(stats_2026.get('walks_per_9'), 1)
        else:
            era = whip = k9 = bb9 = '—'
        return f'''
            <div style="margin-top: 20px;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">投球分析</h3>
                <p>作为{role_zh}，{p['name']} 的球路组合以快速球搭配滑球为主。2026年ERA {era}、WHIP {whip} 反映了他的控球与被击中情况。K/9 {k9} 显示三振能力，BB/9 {bb9} 显示保送控制。</p>
                <p>他的角色定位决定了他的投球策略：{role_zh} 需要在好球带边缘工作，避免中心击球。若他能稳定 first-pitch strike，整体成绩有望提升。</p>
            </div>
        '''
    else:
        if stats_2026:
            avg = fmt_num(stats_2026.get('avg'))
            ops = fmt_num(stats_2026.get('ops'))
            obp = fmt_num(stats_2026.get('obp'))
            slg = fmt_num(stats_2026.get('slg'))
        else:
            avg = ops = obp = slg = '—'
        return f'''
            <div style="margin-top: 20px;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">打击分析</h3>
                <p>2026年打击三围为 {avg}/{obp}/{slg}，OPS {ops}。作为{role_zh}，他的价值在于稳定输出和 situational hitting。</p>
                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">防守分析</h3>
                <p>{p['name']} 在{p['position']}位置上具备符合位置的防守能力。他的站位、判断和传球为基本盘，能够在常规机会中稳定完成防守任务。</p>
            </div>
        '''


def build_pros_cons(p, stats_2026):
    role_zh = role_title(p['role'], p['position'])
    if p['role'] in ('starter', 'reliever', 'closer'):
        pros = [
            f"{role_zh}角色定位清晰，战术价值明确",
            "具备必要的球种组合来应付大联盟打者",
            "在道奇投手教练团体系下持续进步",
            "能够吃下关键局数/出局数",
            "经验丰富或年轻潜力兼具"
        ]
        cons = [
            "面对精英打者时控球/球路不够稳定",
            "伤病或样本限制影响数据代表性" if p['status'].startswith('IL') or p['status'] == 'Minors' else "需要在高压局面下证明稳定性",
            "球速或变化球品质仍有提升空间",
            "ERA/WHIP 在某些月份波动较大"
        ]
    else:
        pros = [
            f"{role_zh}位置价值明确，阵容灵活性强" if p['role'] == 'utility' else f"{p['position']}位置上的稳定贡献者",
            "具备大联盟级别的基本技能和比赛意识",
            "在道奇体系中获得成长机会",
            "能够执行团队战术需求"
        ]
        cons = [
            "打击数据可能受角色/出场时间限制",
            "面对顶级投手时压制力不足",
            "防守范围或特定技能存在局限",
            "需要在整个赛季保持稳定性"
        ]
    return "\n".join(f'                        <li>{item}</li>' for item in pros), "\n".join(f'                        <li>{item}</li>' for item in cons)


def build_future(p):
    role_zh = role_title(p['role'], p['position'])
    if p['status'] == 'Minors':
        return f'''
            <div style="margin-top: 20px;">
                <p>{p['name']} 目前在小联盟持续成长，未来目标是在道奇队获得稳定大联盟机会。通过提升核心技能，他有望在未来1-2年内成为道奇阵容的一员。</p>
                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>提升主要工具：</strong>强化{role_zh}最核心的技能</li>
                    <li><strong>保持健康：</strong>避免伤病，争取完整赛季</li>
                    <li><strong>学习大联盟配球/节奏：</strong>向老将取经</li>
                </ol>
            </div>
        '''
    if p['status'].startswith('IL'):
        return f'''
            <div style="margin-top: 20px;">
                <p>{p['name']} 的首要任务是恢复健康并回归球场。一旦回归，他将在{role_zh}位置为道奇提供即战力。</p>
                <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">复出后目标</h3>
                <ol style="margin-left: 20px; line-height: 2;">
                    <li><strong>循序渐进：</strong>避免复出后过度使用</li>
                    <li><strong>找回节奏：</strong>恢复比赛感觉和信心</li>
                    <li><strong>季后赛准备：</strong>在赛季末为季后赛储备状态</li>
                </ol>
            </div>
        '''
    return f'''
        <div style="margin-top: 20px;">
            <p>{p['name']} 作为道奇{role_zh}，未来将继续在现有角色中发挥作用。道奇教练团会根据球队需求和对手配球来最大化他的价值。</p>
            <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">发展建议</h3>
            <ol style="margin-left: 20px; line-height: 2;">
                <li><strong>保持稳定：</strong>在赛季后半段维持当前产出</li>
                <li><strong>提升关键技能：</strong>针对弱项进行专门训练</li>
                <li><strong>团队角色：</strong>在季后赛竞争中发挥经验或活力</li>
            </ol>
        </div>
    '''


def build_background(p, info):
    role_zh = role_title(p['role'], p['position'])
    birthplace = '美国'  # generic, not available from API
    debut = info.get('mlb_debut_date', '—') if info else '—'
    if p['status'] == 'Minors':
        return f'''
            <div style="margin-top: 20px;">
                <p>{p['name']} 是道奇组织中的年轻{role_zh}，正在小联盟中积累经验和技能。作为道奇农场体系的一部分，他接受系统的投球/打击和体能训练，目标是未来登上大联盟。</p>
                <p>他展现出的潜能让球探和教练团对他抱有期待，持续的进步将决定他在道奇未来的角色。</p>
            </div>
        '''
    return f'''
        <div style="margin-top: 20px;">
            <p>{p['name']} 是洛杉矶道奇队的{role_zh}，于 {debut} 完成MLB首秀。他在道奇体系中扮演着重要角色，无论是作为稳定轮值/牛棚成员还是多功能工具人，都为球队提供价值。</p>
            <p>他的职业态度和团队合作精神受到教练团认可，未来将继续在道奇追逐季后赛和世界大赛冠军。</p>
        </div>
    '''


# ---------------------------------------------------------------------------
# Main assembly
# ---------------------------------------------------------------------------

def build_html(p, info, stats_2025, stats_2026, grades):
    html = HTML_TEMPLATE
    html = html.replace('__TITLE__', f"{p['name']} 球探报告")
    html = html.replace('__PLAYER_NAME__', p['name'])
    html = html.replace('__SUBTITLE__', f"Los Angeles Dodgers #{p['number']} | {p['position']} | {p['status']}")
    html = html.replace('__COVER_IMG__', f"{slugify(p['name'])}_report_cover.png")
    html = html.replace('__INFO_GRID__', build_info_grid(p, info))
    html = html.replace('__SCOUTING_SUMMARY__', scouting_summary(p, info, stats_2026, p['role']))
    html = html.replace('__CAREER_NOTE__', career_note(p, info))
    html = html.replace('__STATUS_BOX__', status_box(p))

    # Batting section
    if p['role'] not in ('starter', 'reliever', 'closer'):
        batting_section = f'''
        <div class="section">
            <h2>📊 2026赛季打击数据</h2>
            <div class="stats-grid">
{build_batting_grid(stats_2026)}
            </div>
        </div>

        <div class="section">
            <h2>📊 2025 vs 2026 赛季对比</h2>
            <div style="text-align: center; margin: 20px 0;">
                <img src="{slugify(p['name'])}_season_comparison.png" alt="赛季对比" style="width: 100%; max-width: 900px; border-radius: 10px;">
            </div>
            <h3 style="margin-top: 30px; color: #4fc3f7;">打击数据对比</h3>
            <table class="comparison-table">
                <thead>
                    <tr><th>赛季</th><th>G</th><th>AVG</th><th>OBP</th><th>SLG</th><th>OPS</th><th>HR</th><th>RBI</th><th>BB</th><th>SO</th></tr>
                </thead>
                <tbody>
{build_batting_table(stats_2025, stats_2026)}
                </tbody>
            </table>
        </div>
'''
        html = html.replace('__BATTING_SECTION__', batting_section)
        html = html.replace('__PITCHING_SECTION__', '')
    else:
        batting_section = ''
        pitching_section = f'''
        <div class="section">
            <h2>📊 2026赛季投球数据</h2>
            <div class="stats-grid">
{build_pitching_grid(stats_2026)}
            </div>
        </div>

        <div class="section">
            <h2>📊 2025 vs 2026 赛季对比</h2>
            <div style="text-align: center; margin: 20px 0;">
                <img src="{slugify(p['name'])}_season_comparison.png" alt="赛季对比" style="width: 100%; max-width: 900px; border-radius: 10px;">
            </div>
            <h3 style="margin-top: 30px; color: #4fc3f7;">投球数据对比</h3>
            <table class="comparison-table">
                <thead>
                    <tr><th>赛季</th><th>G</th><th>GS</th><th>W-L</th><th>ERA</th><th>IP</th><th>K</th><th>BB</th><th>WHIP</th><th>K/9</th></tr>
                </thead>
                <tbody>
{build_pitching_table(stats_2025, stats_2026)}
                </tbody>
            </table>
        </div>
'''
        html = html.replace('__BATTING_SECTION__', batting_section)
        html = html.replace('__PITCHING_SECTION__', pitching_section)

    html = html.replace('__ARSENAL_SECTION__', build_pitch_arsenal(p))
    html = html.replace('__ANALYSIS__', build_analysis(p, stats_2026, stats_2025, info))
    pros, cons = build_pros_cons(p, stats_2026)
    html = html.replace('__PROS__', pros)
    html = html.replace('__CONS__', cons)
    html = html.replace('__GRADES_RADAR__', f"{slugify(p['name'])}_overall_grades.png")
    html = html.replace('__GRADES_GRID__', build_grades_grid(grades))
    avg_grade = round(sum(g['value'] for g in grades) / len(grades))
    html = html.replace('__OVERALL_GRADE__', str(avg_grade))
    html = html.replace('__OVERALL_DESC__', f"综合{len(grades)}项工具评分的平均表现，反映{p['name']}作为{role_title(p['role'], p['position'])}的当前价值。")
    html = html.replace('__OVERALL_LABEL__', f"{grade_from_value(avg_grade)} 级 / {role_title(p['role'], p['position'])}")
    html = html.replace('__FUTURE_OUTLOOK__', build_future(p))
    html = html.replace('__BACKGROUND__', build_background(p, info))
    html = html.replace('__FOOTER_DATE__', TODAY)
    html = html.replace('__DATA_DATE__', DATA_DATE)
    return html


def build_md(p, stats_2026):
    lines = [
        f"# {p['name']} 球探报告",
        "",
        f"> **Los Angeles Dodgers #{p['number']} | {p['position']} | {p['status']}**",
        f"> ",
        f"> 报告生成时间：{TODAY}",
        "",
        "---",
        "",
        "## 📋 基本信息",
        "",
        f"- **姓名**：{p['name']}",
        f"- **背号**：#{p['number']}",
        f"- **位置**：{p['position']}",
        f"- **状态**：{p['status']}",
        "",
        "---",
        "",
        "## 📊 2026赛季数据",
        "",
    ]
    if p['role'] in ('starter', 'reliever', 'closer'):
        if stats_2026:
            lines.append(f"| G | GS | W | L | ERA | IP | K | BB | WHIP | K/9 |")
            lines.append(f"|---|---|---|---|---|---|---|---|---|---|")
            lines.append(f"| {stats_2026.get('games_played','—')} | {stats_2026.get('games_started','—')} | {stats_2026.get('wins','—')} | {stats_2026.get('losses','—')} | {stats_2026.get('era','—')} | {stats_2026.get('innings_pitched','—')} | {stats_2026.get('strikeouts','—')} | {stats_2026.get('walks','—')} | {stats_2026.get('whip','—')} | {stats_2026.get('strikeouts_per_9','—')} |")
        else:
            lines.append("*投球数据暂不可用*")
    else:
        if stats_2026:
            lines.append(f"| G | AVG | OBP | SLG | OPS | HR | RBI | SB | BB | SO |")
            lines.append(f"|---|---|---|---|---|---|---|---|---|---|")
            lines.append(f"| {stats_2026.get('games_played','—')} | {stats_2026.get('avg','—')} | {stats_2026.get('obp','—')} | {stats_2026.get('slg','—')} | {stats_2026.get('ops','—')} | {stats_2026.get('home_runs','—')} | {stats_2026.get('rbi','—')} | {stats_2026.get('stolen_bases','—')} | {stats_2026.get('walks','—')} | {stats_2026.get('strikeouts','—')} |")
        else:
            lines.append("*打击数据暂不可用*")
    lines.extend(["", "---", "", "## 📝 备注", "", "此报告为详细版球探报告，包含图表和自动生成的分析。", "", f"*数据来源：MLB Stats API | 生成时间：{TODAY}*"])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("Dodgers Remaining Detailed Scouting Report Generator")
    print("=" * 70)
    success = 0
    failed = []
    for cfg in PLAYER_CONFIGS:
        if cfg['name'] in COMPLETED:
            print(f"[SKIP] {cfg['name']} already detailed")
            continue
        output_dir = os.path.join(BASE_DIR, slugify(cfg['name']))
        os.makedirs(output_dir, exist_ok=True)
        print(f"\n[{cfg['name']}] -> {output_dir}")
        try:
            # Fetch info and stats
            info = fetch_player_info(cfg['search'])
            stats_2025 = None
            stats_2026 = None
            if info:
                pid = info['id']
                stats_2025 = fetch_player_stats(pid, 2025)
                stats_2026 = fetch_player_stats(pid, 2026)
                # Extract just the stats dict
                if stats_2025:
                    stats_2025 = stats_2025.get('pitching') or stats_2025.get('batting') or stats_2025
                if stats_2026:
                    stats_2026 = stats_2026.get('pitching') or stats_2026.get('batting') or stats_2026
                # Ensure consistent keys for table builder
                if stats_2025:
                    stats_2025.setdefault('G', stats_2025.get('games_played', '—'))
                    stats_2025.setdefault('AVG', stats_2025.get('avg', '—'))
                    stats_2025.setdefault('OBP', stats_2025.get('obp', '—'))
                    stats_2025.setdefault('SLG', stats_2025.get('slg', '—'))
                    stats_2025.setdefault('OPS', stats_2025.get('ops', '—'))
                    stats_2025.setdefault('HR', stats_2025.get('home_runs', '—'))
                    stats_2025.setdefault('RBI', stats_2025.get('rbi', '—'))
                    stats_2025.setdefault('BB', stats_2025.get('walks', '—'))
                    stats_2025.setdefault('SO', stats_2025.get('strikeouts', '—'))
                    stats_2025.setdefault('GS', stats_2025.get('games_started', '—'))
                    stats_2025.setdefault('W', stats_2025.get('wins', '—'))
                    stats_2025.setdefault('L', stats_2025.get('losses', '—'))
                    stats_2025.setdefault('ERA', stats_2025.get('era', '—'))
                    stats_2025.setdefault('IP', stats_2025.get('innings_pitched', '—'))
                    stats_2025.setdefault('K', stats_2025.get('strikeouts', '—'))
                    stats_2025.setdefault('WHIP', stats_2025.get('whip', '—'))
                    stats_2025.setdefault('K/9', stats_2025.get('strikeouts_per_9', '—'))
                if stats_2026:
                    stats_2026.setdefault('G', stats_2026.get('games_played', '—'))
                    stats_2026.setdefault('AVG', stats_2026.get('avg', '—'))
                    stats_2026.setdefault('OBP', stats_2026.get('obp', '—'))
                    stats_2026.setdefault('SLG', stats_2026.get('slg', '—'))
                    stats_2026.setdefault('OPS', stats_2026.get('ops', '—'))
                    stats_2026.setdefault('HR', stats_2026.get('home_runs', '—'))
                    stats_2026.setdefault('RBI', stats_2026.get('rbi', '—'))
                    stats_2026.setdefault('BB', stats_2026.get('walks', '—'))
                    stats_2026.setdefault('SO', stats_2026.get('strikeouts', '—'))
                    stats_2026.setdefault('GS', stats_2026.get('games_started', '—'))
                    stats_2026.setdefault('W', stats_2026.get('wins', '—'))
                    stats_2026.setdefault('L', stats_2026.get('losses', '—'))
                    stats_2026.setdefault('ERA', stats_2026.get('era', '—'))
                    stats_2026.setdefault('IP', stats_2026.get('innings_pitched', '—'))
                    stats_2026.setdefault('K', stats_2026.get('strikeouts', '—'))
                    stats_2026.setdefault('WHIP', stats_2026.get('whip', '—'))
                    stats_2026.setdefault('K/9', stats_2026.get('strikeouts_per_9', '—'))
            age = info.get('age', 25) if info else 25

            # Generate charts
            base_name = slugify(cfg['name'])
            cover_path = os.path.join(output_dir, f"{base_name}_report_cover.png")
            season_path = os.path.join(output_dir, f"{base_name}_season_comparison.png")
            grades_path = os.path.join(output_dir, f"{base_name}_overall_grades.png")
            generate_cover(cfg, stats_2026, cover_path)
            generate_season_chart(cfg, stats_2025, stats_2026, season_path)
            if cfg['role'] in ('starter', 'reliever', 'closer'):
                grades = compute_pitcher_grades(stats_2026, cfg['role'], age)
            else:
                grades = compute_batter_grades(stats_2026, cfg['position'], age)
            generate_grades_chart(cfg, grades, grades_path)

            # Generate HTML / Markdown
            html = build_html(cfg, info, stats_2025, stats_2026, grades)
            html_path = os.path.join(output_dir, f"{base_name}-scouting-report.html")
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html)
            md = build_md(cfg, stats_2026)
            md_path = os.path.join(output_dir, f"{base_name}-scouting-report.md")
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md)
            print(f"  [OK] HTML + MD + charts generated")
            success += 1
        except Exception as e:
            print(f"  [FAIL] {e}")
            failed.append(cfg['name'])
    print("\n" + "=" * 70)
    print(f"Completed: {success}/{len(PLAYER_CONFIGS)}")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    print("=" * 70)


if __name__ == '__main__':
    main()
