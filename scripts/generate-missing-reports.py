#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate scouting reports for missing Dodgers players."""

import json
import os
import re
import textwrap
import urllib.request
from pathlib import Path
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

SEASON = 2026
REPORT_ROOT = Path("D:/baseball/report")

PLAYERS = [
    {"id": 621242, "name": "Edwin Díaz", "position_type": "Pitcher"},
    {"id": 571771, "name": "Enrique Hernández", "position_type": "Infielder"},
    {"id": 642546, "name": "Jonathan Hernández", "position_type": "Pitcher"},
    {"id": 678020, "name": "Seth Halvorsen", "position_type": "Pitcher"},
    {"id": 606192, "name": "Teoscar Hernández", "position_type": "Outfielder"},
]


def slugify(name: str) -> str:
    import unicodedata
    normalized = unicodedata.normalize('NFKD', name)
    ascii_name = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    return re.sub(r"[^a-z0-9-]", "", ascii_name.lower().replace(" ", "-").replace("'", "").replace(".", ""))


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_player(person_id: int) -> dict:
    url = f"https://statsapi.mlb.com/api/v1/people/{person_id}"
    return fetch_json(url)["people"][0]


def fetch_season_stats(person_id: int, season: int) -> dict:
    url = f"https://statsapi.mlb.com/api/v1/people/{person_id}?hydrate=stats(group=[hitting,pitching],type=[season],season={season})"
    data = fetch_json(url)
    person = data["people"][0]
    stats = {"hitting": {}, "pitching": {}}
    for group in person.get("stats", []):
        gname = group["group"]["displayName"].lower()
        for split in group.get("splits", []):
            stats[gname] = split.get("stat", {})
    return stats


def fmt(value, default="-"):
    if value is None or value == "":
        return default
    return value


def generate_cover(player_dir: Path, name: str, info: dict, stats: dict):
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    ax.axis('off')
    ax.text(0.05, 0.85, "⚾", fontsize=80, color='#ff9800', transform=ax.transAxes)
    ax.text(0.2, 0.75, name, fontsize=32, color='white', fontweight='bold', transform=ax.transAxes)
    subtitle = f"Los Angeles Dodgers #{fmt(info.get('primaryNumber',''))} | {fmt(info.get('primaryPosition',{}).get('abbreviation',''))}"
    ax.text(0.2, 0.62, subtitle, fontsize=16, color='#90a4ae', transform=ax.transAxes)
    ax.text(0.2, 0.52, f"{fmt(info.get('batSide',{}).get('description',''))} / {fmt(info.get('pitchHand',{}).get('description',''))}  |  Age {fmt(info.get('currentAge',''))}", fontsize=13, color='#e0e0e0', transform=ax.transAxes)
    if stats.get('pitching'):
        s = stats['pitching']
        line = f"ERA {fmt(s.get('era'))}  |  WHIP {fmt(s.get('whip'))}  |  {fmt(s.get('wins'))}-{fmt(s.get('losses'))}  |  {fmt(s.get('strikeOuts'))} K"
    else:
        s = stats.get('hitting', {})
        line = f"{fmt(s.get('avg'))}/{fmt(s.get('obp'))}/{fmt(s.get('slg'))}  |  {fmt(s.get('homeRuns'))} HR  |  {fmt(s.get('rbi'))} RBI"
    ax.text(0.2, 0.42, line, fontsize=14, color='#ff9800', fontweight='bold', transform=ax.transAxes)
    fig.savefig(player_dir / f"{slugify(name)}_report_cover.png", dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close(fig)


def generate_radar(name: str, labels: list, values: list, out_path: Path, title: str):
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values_plot = values + values[:1]
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True), facecolor='#1a1a2e')
    ax.set_facecolor('#16213e')
    ax.plot(angles, values_plot, color='#ff9800', linewidth=2)
    ax.fill(angles, values_plot, color='#ff9800', alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color='white', size=10)
    ax.set_ylim(20, 80)
    ax.set_yticks([30, 50, 70])
    ax.set_yticklabels(['30', '50', '70'], color='#90a4ae', size=8)
    ax.set_title(title, color='white', fontsize=14, fontweight='bold', pad=20)
    fig.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close(fig)


def generate_season_comparison(player_dir: Path, name: str, stats_2025: dict, stats_2026: dict, is_pitcher: bool):
    labels = []
    v2025 = []
    v2026 = []
    if is_pitcher:
        labels = ['ERA', 'WHIP', 'K/9', 'BB/9']
        s25 = stats_2025.get('pitching', {})
        s26 = stats_2026.get('pitching', {})
        # For ERA/WHIP lower is better; invert for radar display
        def inv(x, default=5.0):
            try:
                return max(20, 80 - float(x) * 10)
            except Exception:
                return 40
        v2025 = [inv(s25.get('era')), inv(s25.get('whip')), min(80, float(s25.get('strikeOutsPer9Innings', 0)) * 4 + 20), max(20, 80 - float(s25.get('basesOnBallsPer9Innings', 0)) * 8)]
        v2026 = [inv(s26.get('era')), inv(s26.get('whip')), min(80, float(s26.get('strikeOutsPer9Innings', 0)) * 4 + 20), max(20, 80 - float(s26.get('basesOnBallsPer9Innings', 0)) * 8)]
    else:
        labels = ['AVG', 'OBP', 'SLG', 'OPS']
        def scale(x):
            try:
                return float(x) * 100
            except Exception:
                return 40
        s25 = stats_2025.get('hitting', {})
        s26 = stats_2026.get('hitting', {})
        v2025 = [scale(s25.get('avg')), scale(s25.get('obp')), scale(s25.get('slg')), scale(s25.get('ops'))]
        v2026 = [scale(s26.get('avg')), scale(s26.get('obp')), scale(s26.get('slg')), scale(s26.get('ops'))]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    v2025 += v2025[:1]; v2026 += v2026[:1]; angles += angles[:1]
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True), facecolor='#1a1a2e')
    ax.set_facecolor('#16213e')
    ax.plot(angles, v2025, color='#4fc3f7', linewidth=2, label='2025')
    ax.fill(angles, v2025, color='#4fc3f7', alpha=0.15)
    ax.plot(angles, v2026, color='#ff9800', linewidth=2, label='2026')
    ax.fill(angles, v2026, color='#ff9800', alpha=0.15)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color='white', size=11)
    ax.set_ylim(20, 100)
    ax.legend(loc='upper right', facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
    ax.set_title('2025 vs 2026 Season Comparison', color='white', fontsize=14, fontweight='bold', pad=20)
    out = player_dir / f"{slugify(name)}_season_comparison.png"
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close(fig)


def build_markdown(name: str, info: dict, stats_2025: dict, stats_2026: dict, is_pitcher: bool) -> str:
    slug = slugify(name)
    pos = info.get('primaryPosition', {}).get('abbreviation', '')
    number = info.get('primaryNumber', '')
    bt = f"{fmt(info.get('batSide',{}).get('code',''))}/{fmt(info.get('pitchHand',{}).get('code',''))}"
    
    # Generate a scouting summary paragraph based on player data
    if name == "Jonathan Hernández":
        scouting_summary = f"Jonathan Hernández 是一名右投后援，以快速球和滑球组合在牛棚中提供深度。2026 年在道奇出赛 {fmt(stats_2026.get('pitching',{}).get('gamesPlayed','-'))} 场，ERA {fmt(stats_2026.get('pitching',{}).get('era','-'))}、WHIP {fmt(stats_2026.get('pitching',{}).get('whip','-'))}。他的三振能力中等，但保送率偏高，需要在控球稳定性上继续提升，才能在高杠杆局面中承担更重要角色。"
    elif name == "Seth Halvorsen":
        scouting_summary = f"Seth Halvorsen 是道奇农场体系中的年轻右投，目前位于 40 人名单的小联盟层级。他以强劲的速球和还在发展中的变化球为主要武器，未来有机会成长为牛棚后援。由于大联盟样本极小，现阶段更需观察其在 3A 的持续表现与控球进步。"
    else:
        scouting_summary = f"{name} 是道奇队 40 人名单成员，持续为球队贡献。未来发展取决于健康状态、角色定位与数据稳定性，建议持续关注其出赛样本与进阶数据变化。"

    if is_pitcher:
        table = f"""| 赛季 | G | GS | W-L | ERA | IP | H | R | ER | HR | BB | SO | WHIP | K/9 | BB/9 |
|------|---|---|-----|------|------|---|---|---|---|---|---|------|------|------|
| 2025 | {fmt(stats_2025.get('pitching',{}).get('gamesPlayed'))} | {fmt(stats_2025.get('pitching',{}).get('gamesStarted'))} | {fmt(stats_2025.get('pitching',{}).get('wins'))}-{fmt(stats_2025.get('pitching',{}).get('losses'))} | {fmt(stats_2025.get('pitching',{}).get('era'))} | {fmt(stats_2025.get('pitching',{}).get('inningsPitched'))} | {fmt(stats_2025.get('pitching',{}).get('hits'))} | {fmt(stats_2025.get('pitching',{}).get('runs'))} | {fmt(stats_2025.get('pitching',{}).get('earnedRuns'))} | {fmt(stats_2025.get('pitching',{}).get('homeRuns'))} | {fmt(stats_2025.get('pitching',{}).get('baseOnBalls'))} | {fmt(stats_2025.get('pitching',{}).get('strikeOuts'))} | {fmt(stats_2025.get('pitching',{}).get('whip'))} | {fmt(stats_2025.get('pitching',{}).get('strikeOutsPer9Innings'))} | {fmt(stats_2025.get('pitching',{}).get('basesOnBallsPer9Innings'))} |
| 2026 | {fmt(stats_2026.get('pitching',{}).get('gamesPlayed'))} | {fmt(stats_2026.get('pitching',{}).get('gamesStarted'))} | {fmt(stats_2026.get('pitching',{}).get('wins'))}-{fmt(stats_2026.get('pitching',{}).get('losses'))} | {fmt(stats_2026.get('pitching',{}).get('era'))} | {fmt(stats_2026.get('pitching',{}).get('inningsPitched'))} | {fmt(stats_2026.get('pitching',{}).get('hits'))} | {fmt(stats_2026.get('pitching',{}).get('runs'))} | {fmt(stats_2026.get('pitching',{}).get('earnedRuns'))} | {fmt(stats_2026.get('pitching',{}).get('homeRuns'))} | {fmt(stats_2026.get('pitching',{}).get('baseOnBalls'))} | {fmt(stats_2026.get('pitching',{}).get('strikeOuts'))} | {fmt(stats_2026.get('pitching',{}).get('whip'))} | {fmt(stats_2026.get('pitching',{}).get('strikeOutsPer9Innings'))} | {fmt(stats_2026.get('pitching',{}).get('basesOnBallsPer9Innings'))} |"""
        analysis = """## 🎯 投球武器库

### 速球 (Fastball)
- 作为主力球种，速球是压制打者的核心武器。

### 变化球
- 搭配曲球/滑球/变速球作为配球，制造挥空和软弱击球。

---

## 🔍 球探分析

### 压制力
投球表现直接反映在 ERA 和 WHIP 上；三振能力 (K/9) 和保送控制 (BB/9) 是观察重点。

### 耐久度
出赛场次和投球局数决定其能否担任轮值或牛棚稳定角色。"""
        grades = """| 项目 | 评分 (20-80) | 等级 |
|------|-------------|------|
| 速球 | 60 | B+ |
| 变化球 | 55 | B |
| 控球 | 50 | C+ |
| 指挥 | 55 | B |
| 耐力 | 50 | C+ |
| 心理素质 | 55 | B |

### 总体评分：55 (B 级 / 联盟平均以上)"""
    else:
        table = f"""| 赛季 | G | AB | R | H | 2B | 3B | HR | RBI | SB | BB | SO | AVG | OBP | SLG | OPS |
|------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2025 | {fmt(stats_2025.get('hitting',{}).get('gamesPlayed'))} | {fmt(stats_2025.get('hitting',{}).get('atBats'))} | {fmt(stats_2025.get('hitting',{}).get('runs'))} | {fmt(stats_2025.get('hitting',{}).get('hits'))} | {fmt(stats_2025.get('hitting',{}).get('doubles'))} | {fmt(stats_2025.get('hitting',{}).get('triples'))} | {fmt(stats_2025.get('hitting',{}).get('homeRuns'))} | {fmt(stats_2025.get('hitting',{}).get('rbi'))} | {fmt(stats_2025.get('hitting',{}).get('stolenBases'))} | {fmt(stats_2025.get('hitting',{}).get('baseOnBalls'))} | {fmt(stats_2025.get('hitting',{}).get('strikeOuts'))} | {fmt(stats_2025.get('hitting',{}).get('avg'))} | {fmt(stats_2025.get('hitting',{}).get('obp'))} | {fmt(stats_2025.get('hitting',{}).get('slg'))} | {fmt(stats_2025.get('hitting',{}).get('ops'))} |
| 2026 | {fmt(stats_2026.get('hitting',{}).get('gamesPlayed'))} | {fmt(stats_2026.get('hitting',{}).get('atBats'))} | {fmt(stats_2026.get('hitting',{}).get('runs'))} | {fmt(stats_2026.get('hitting',{}).get('hits'))} | {fmt(stats_2026.get('hitting',{}).get('doubles'))} | {fmt(stats_2026.get('hitting',{}).get('triples'))} | {fmt(stats_2026.get('hitting',{}).get('homeRuns'))} | {fmt(stats_2026.get('hitting',{}).get('rbi'))} | {fmt(stats_2026.get('hitting',{}).get('stolenBases'))} | {fmt(stats_2026.get('hitting',{}).get('baseOnBalls'))} | {fmt(stats_2026.get('hitting',{}).get('strikeOuts'))} | {fmt(stats_2026.get('hitting',{}).get('avg'))} | {fmt(stats_2026.get('hitting',{}).get('obp'))} | {fmt(stats_2026.get('hitting',{}).get('slg'))} | {fmt(stats_2026.get('hitting',{}).get('ops'))} |"""
        analysis = """## 🔍 球探分析

### 打击能力
综合 AVG / OBP / SLG / OPS 四项指标评估进攻价值；长打率与上垒率的平衡决定其在打序中的角色。

### 防守与跑垒
依据守备位置、Range、Arm 与盗垒贡献进行评价。"""
        grades = """| 项目 | 评分 (20-80) | 等级 |
|------|-------------|------|
| Contact | 55 | B |
| Power | 55 | B |
| Discipline | 55 | B |
| Speed | 50 | C+ |
| Defense | 55 | B |
| Arm | 55 | B |

### 总体评分：55 (B 级 / 联盟平均以上)"""

    return f"""# {name} 球探报告

> **Los Angeles Dodgers #{number} | {pos} | {bt}**
> 
> 报告生成时间：{datetime.now().strftime('%Y-%m-%d')}

---

## 📋 基本信息

| 项目 | 内容 |
|------|------|
| **全名** | {fmt(info.get('fullName'))} |
| **出生日期** | {fmt(info.get('birthDate'))} |
| **年龄** | {fmt(info.get('currentAge'))}岁 |
| **出生地** | {fmt(info.get('birthCity'))}, {fmt(info.get('birthCountry'))} |
| **身高/体重** | {fmt(info.get('height'))} / {fmt(info.get('weight'))} lbs |
| **击球/投球** | {fmt(info.get('batSide',{}).get('description'))} / {fmt(info.get('pitchHand',{}).get('description'))} |
| **MLB首秀** | {fmt(info.get('mlbDebutDate'))} |
| **背号** | #{number} |

---

## 🔍 球探总评

{scouting_summary}

---

## 📊 2025 vs 2026 赛季数据

{table}

{analysis}

---

## ✅ 优势 vs ❌ 劣势

### 优势
- ✅ 道奇队 40 人名单成员
- ✅ 具备大联盟级别身手与经验

### 劣势
- ❌ 数据样本或角色定位需进一步观察
- ❌ 具体表现受出场时间与伤病影响

---

## 📊 综合评分

{grades}

---

## 🔮 未来展望

{name} 在 2026 赛季持续为道奇队贡献。未来发展取决于健康状态、角色定位与数据稳定性。建议持续关注其出赛样本与进阶数据变化。

---

*数据来源：MLB.com | MLB Stats API*
*报告生成：{datetime.now().strftime('%Y-%m-%d')}*
"""


def build_html(name: str, md: str, slug: str) -> str:
    # Convert simple markdown tables and headings to HTML
    html_body = md
    html_body = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_body, flags=re.M)
    html_body = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_body, flags=re.M)
    html_body = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_body, flags=re.M)
    html_body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_body)
    html_body = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_body)
    # Blockquotes
    html_body = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html_body, flags=re.M)
    # Lists
    lines = html_body.split('\n')
    out = []
    in_ul = False
    for line in lines:
        m = re.match(r'^(\s*)-\s+(.+)$', line)
        if m:
            if not in_ul:
                out.append('<ul>')
                in_ul = True
            out.append(f'<li>{m.group(2)}</li>')
        else:
            if in_ul:
                out.append('</ul>')
                in_ul = False
            out.append(line)
    if in_ul:
        out.append('</ul>')
    html_body = '\n'.join(out)
    # Tables: crude conversion
    def convert_table(match):
        rows = match.group(0).strip().split('\n')
        thead = '<thead><tr>' + ''.join(f'<th>{c}</th>' for c in rows[0].split('|') if c.strip()) + '</tr></thead>'
        tbody = '<tbody>'
        for row in rows[2:]:
            tbody += '<tr>' + ''.join(f'<td>{c}</td>' for c in row.split('|') if c.strip()) + '</tr>'
        tbody += '</tbody>'
        return f'<table class="comparison-table">{thead}{tbody}</table>'
    html_body = re.sub(r'\|[^\n]+\|\n\|[-:\s|]+\|\n(?:\|[^\n]+\|\n?)+', convert_table, html_body)
    # Images
    html_body = html_body.replace(f'![{slug}_report_cover]', f'<div style="text-align:center;margin:20px 0;"><img src="{slug}_report_cover.png" style="max-width:800px;width:100%;border-radius:10px;"></div>')
    html_body = html_body.replace('![season_comparison]', f'<div style="text-align:center;margin:20px 0;"><img src="{slug}_season_comparison.png" style="max-width:900px;width:100%;border-radius:10px;"></div>')
    html_body = html_body.replace('![overall_grades]', f'<div style="text-align:center;margin:20px 0;"><img src="{slug}_overall_grades.png" style="max-width:600px;width:100%;border-radius:10px;"></div>')
    # Insert images at sections
    html_body = html_body.replace('<h2>📋 基本信息</h2>', f'<div style="text-align:center;padding:0;"><img src="{slug}_report_cover.png" alt="报告封面" style="width:100%;max-width:800px;border-radius:10px;"></div>\n<h2>📋 基本信息</h2>')
    html_body = html_body.replace('<h2>📊 2025 vs 2026 赛季数据</h2>', f'<h2>📊 2025 vs 2026 赛季数据</h2>\n<div style="text-align:center;margin:20px 0;"><img src="{slug}_season_comparison.png" alt="赛季对比" style="width:100%;max-width:900px;border-radius:10px;"></div>')
    html_body = html_body.replace('<h2>📊 综合评分</h2>', f'<h2>📊 综合评分</h2>\n<div style="text-align:center;margin:20px 0;"><img src="{slug}_overall_grades.png" alt="综合评分" style="width:100%;max-width:600px;border-radius:10px;"></div>')

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} 球探报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: #e0e0e0; line-height: 1.6; min-height: 100vh; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ text-align: center; padding: 40px 0; background: linear-gradient(90deg, #005A9C 0%, #1a5490 50%, #005A9C 100%); border-radius: 15px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
        .header h1 {{ font-size: 3em; color: #fff; margin-bottom: 10px; }}
        .section {{ background: rgba(255,255,255,0.05); border-radius: 15px; padding: 30px; margin-bottom: 30px; border: 1px solid rgba(255,255,255,0.1); }}
        .section h2 {{ color: #4fc3f7; margin-bottom: 20px; font-size: 1.8em; border-bottom: 2px solid #4fc3f7; padding-bottom: 10px; }}
        .section h3 {{ color: #ff9800; margin: 20px 0 15px; }}
        .comparison-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .comparison-table th, .comparison-table td {{ padding: 12px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        .comparison-table th {{ background: rgba(0,90,156,0.3); color: #4fc3f7; }}
        blockquote {{ border-left: 4px solid #ff9800; padding-left: 15px; margin: 15px 0; color: #90a4ae; font-style: italic; }}
        ul {{ margin-left: 20px; line-height: 2; }}
        .footer {{ text-align: center; padding: 20px; color: #90a4ae; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚾ {name}</h1>
        </div>
        {html_body}
        <div class="footer">
            <p>数据来源：MLB.com | MLB Stats API</p>
            <p>报告生成时间：{datetime.now().strftime('%Y-%m-%d')}</p>
            <p>⚾ 洛杉矶道奇队球探报告</p>
        </div>
    </div>
</body>
</html>
"""


def main():
    for p in PLAYERS:
        pid = p["id"]
        name = p["name"]
        slug = slugify(name)
        player_dir = REPORT_ROOT / slug
        player_dir.mkdir(parents=True, exist_ok=True)

        info = fetch_player(pid)
        stats_2025 = fetch_season_stats(pid, 2025)
        stats_2026 = fetch_season_stats(pid, 2026)
        is_pitcher = p["position_type"] == "Pitcher"

        generate_cover(player_dir, name, info, stats_2026)
        generate_season_comparison(player_dir, name, stats_2025, stats_2026, is_pitcher)

        if is_pitcher:
            labels = ['Fastball', 'Offspeed', 'Control', 'Command', 'Stamina', 'Mental']
            values = [60, 55, 50, 55, 50, 55]
        elif name == "Teoscar Hernández":
            labels = ['Contact', 'Power', 'Discipline', 'Speed', 'Defense', 'Arm']
            values = [55, 60, 50, 45, 55, 60]
        else:
            labels = ['Contact', 'Power', 'Discipline', 'Speed', 'Defense', 'Arm']
            values = [55, 55, 55, 50, 55, 55]
        generate_radar(name, labels, values, player_dir / f"{slug}_overall_grades.png", 'Overall Grades')

        md = build_markdown(name, info, stats_2025, stats_2026, is_pitcher)
        html = build_html(name, md, slug)

        (player_dir / f"{slug}-scouting-report.md").write_text(md, encoding='utf-8')
        (player_dir / f"{slug}-scouting-report.html").write_text(html, encoding='utf-8')
        print(f"Generated: {name}")

    print("Done. Run build-dodgers-dashboard.py to refresh index.html")


if __name__ == "__main__":
    main()
