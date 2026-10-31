# custom_report_lib.py - 定制化球探报告模板库
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
TODAY = datetime.now().strftime('%Y-%m-%d')

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
        .pitch-card .velocity { font-size: 1.5em; color: #fff; font-weight: bold; }
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
        .career-highlight { background: rgba(255, 215, 0, 0.1); border: 1px solid rgba(255, 215, 0, 0.3); border-radius: 10px; padding: 15px; margin: 15px 0; }
        .career-highlight h4 { color: #FFD700; margin-bottom: 10px; }
        .decline-note { background: rgba(255, 152, 0, 0.1); border: 1px solid rgba(255, 152, 0, 0.3); border-radius: 10px; padding: 15px; margin: 15px 0; }
        .decline-note h4 { color: #ff9800; margin-bottom: 10px; }
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
            <h2>🏆 职业生涯亮点</h2>
__CAREER_HIGHLIGHTS__
        </div>

__2026_STATS_SECTION__

__SEASON_COMPARISON_SECTION__

__PITCH_ARSENAL_SECTION__

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


def slugify(name):
    s = name.lower().replace(' ', '-')
    for a, b in [('á', 'a'), ('é', 'e'), ('í', 'i'), ('ó', 'o'), ('ú', 'u'),
                 ('ñ', 'n'), ('ü', 'u'), ('ã', 'a'), ('õ', 'o'), ('ç', 'c'),
                 ('à', 'a'), ('è', 'e'), ('ì', 'i'), ('ò', 'o'), ('ù', 'u')]:
        s = s.replace(a, b)
    return s


def generate_cover(p, output_path):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')

    ax.text(0.5, 0.85, p['name'], fontsize=32, fontweight='bold', ha='center',
            color='white', transform=ax.transAxes)
    ax.text(0.5, 0.75, f"Los Angeles Dodgers #{p['number']} | {p['position']}", fontsize=18,
            ha='center', color='#4fc3f7', transform=ax.transAxes)
    ax.text(0.5, 0.65, 'SCOUTING REPORT 2026', fontsize=22, fontweight='bold', ha='center',
            color='#ff9800', transform=ax.transAxes)

    y_pos = 0.45
    for i, (label, value) in enumerate(p['cover_stats']):
        x_pos = 0.15 + (i % 4) * 0.23
        if i >= 4:
            y_pos = 0.25
        ax.text(x_pos, y_pos, value, fontsize=26, fontweight='bold', ha='center',
                color='#4fc3f7', transform=ax.transAxes)
        ax.text(x_pos, y_pos - 0.08, label, fontsize=12, ha='center',
                color='#90a4ae', transform=ax.transAxes)

    subtitle = p.get('cover_subtitle', '')
    if not subtitle:
        subtitle = f"{p['status']} | {p.get('college', '')} | MLB Debut {p['debut']}"
    ax.text(0.5, 0.08, subtitle, fontsize=14, ha='center',
            color='#90a4ae', transform=ax.transAxes, style='italic')
    ax.text(0.5, 0.02, f'Generated: {TODAY} | Data: MLB.com, MLB Stats API',
            fontsize=10, ha='center', color='#666', transform=ax.transAxes)

    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close()


def generate_season_chart(p, output_path):
    stats = p['season_chart_stats']
    vals_2025 = p['season_chart_2025']
    vals_2026 = p['season_chart_2026']

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    colors = ['#4fc3f7', '#ff9800']

    for idx, stat in enumerate(stats):
        ax = axes[idx]
        vals = [vals_2025[idx], vals_2026[idx]]
        bars = ax.bar(['2025', '2026'], vals, color=colors, edgecolor='white', alpha=0.9, width=0.5)
        ax.set_title(stat, fontsize=14, fontweight='bold', color='#1a1a2e')
        max_val = max(vals) * 1.25 if max(vals) != 0 else 1
        ax.set_ylim(0, max_val)
        ax.grid(axis='y', alpha=0.3)
        for bar, val in zip(bars, vals):
            height = bar.get_height()
            if p['type'] == 'pitcher':
                text = f'{val:.2f}' if stat in ['ERA', 'WHIP'] else f'{val:.1f}'
            else:
                text = f'{val:.3f}'
            ax.text(bar.get_x() + bar.get_width()/2., height + max_val*0.02,
                    text, ha='center', va='bottom', fontweight='bold', fontsize=11)

    fig.suptitle(f"{p['name']} - 2025 vs 2026 Season Comparison", fontsize=16, fontweight='bold', color='#1a1a2e', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def generate_pitch_velocities(p, output_path):
    if not p.get('pitch_arsenal'):
        return
    arsenal = p['pitch_arsenal']
    fig, ax = plt.subplots(figsize=(12, 6))

    pitches = [a['name'] for a in arsenal]
    min_velo = []
    max_velo = []
    for a in arsenal:
        try:
            rng = a['velocity'].split('（')[0].strip()
            parts = rng.replace('mph', '').split('-')
            min_velo.append(float(parts[0].strip()))
            max_velo.append(float(parts[1].strip()))
        except Exception:
            min_velo.append(0)
            max_velo.append(0)
    avg_velo = [(min_v + max_v) / 2 for min_v, max_v in zip(min_velo, max_velo)]

    x = np.arange(len(pitches))
    width = 0.35
    bars1 = ax.bar(x - width/2, min_velo, width, label='Min', color='#4fc3f7', alpha=0.8)
    bars2 = ax.bar(x + width/2, max_velo, width, label='Max', color='#ff9800', alpha=0.8)

    for i, avg in enumerate(avg_velo):
        ax.plot([i - width/2, i + width/2], [avg, avg], 'r--', linewidth=2, alpha=0.7)
        ax.text(i, avg + 0.5, f'Avg {avg:.1f}', ha='center', va='bottom', fontweight='bold', color='red')

    ax.set_xlabel('Pitch Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Velocity (mph)', fontsize=12, fontweight='bold')
    ax.set_title(f"{p['name']} Pitch Arsenal Velocity Distribution", fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(pitches)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(70, 105)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()


def generate_grades_chart(p, output_path):
    categories = [g['label'] for g in p['grades']]
    values = [g['value'] for g in p['grades']]
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


def grade_class(value):
    if value >= 60: return 'grade-a'
    if value >= 50: return 'grade-b'
    if value >= 40: return 'grade-c'
    return 'grade-d'


def build_info_grid(p):
    items = [
        ("全名", p['name']),
        ("出生日期", p['birth_date']),
        ("年龄", p['age'] + "岁"),
        ("出生地", p['birthplace']),
        ("身高/体重", p['height_weight']),
        ("击球/投球", p['bats_throws']),
        ("位置", p['position']),
        ("MLB首秀", p['debut']),
    ]
    if p.get('college'):
        items.append(("大学", p['college']))
    if p.get('nickname'):
        items.append(("绰号", p['nickname']))
    items.append(("背号", "#" + p['number']))
    items.append(("状态", p['status']))
    return "\n".join(
        f'                    <div class="info-item"><div class="label">{label}</div><div class="value">{value}</div></div>'
        for label, value in items
    )


def build_pitching_grid(stats):
    order = [('G', '出赛'), ('GS', '先发'), ('W', '胜'), ('L', '败'), ('ERA', 'ERA'),
             ('IP', 'IP'), ('K', 'K'), ('BB', 'BB'), ('WHIP', 'WHIP'), ('K/9', 'K/9'), ('BB/9', 'BB/9'), ('HR', '被全垒打')]
    html = ""
    for k, label in order:
        val = stats.get(k, '—')
        color = "#4fc3f7"
        if k == 'ERA' and val != '—':
            try:
                if float(val) > 4.5: color = "#ff9800"
                if float(val) > 5.5: color = "#f44336"
                if float(val) < 3.5: color = "#4caf50"
            except Exception:
                pass
        html += f'''
                <div class="stat-card">
                    <span class="stat-value" style="color: {color};">{val}</span>
                    <div class="stat-label">{label}</div>
                </div>'''
    return html


def build_batting_grid(stats):
    order = [('G', '出赛'), ('AVG', '打击率'), ('OBP', '上垒率'), ('SLG', '长打率'), ('OPS', 'OPS'),
             ('HR', '本垒打'), ('RBI', '打点'), ('SB', '盗垒')]
    html = ""
    for k, label in order:
        val = stats.get(k, '—')
        html += f'''
                <div class="stat-card">
                    <span class="stat-value">{val}</span>
                    <div class="stat-label">{label}</div>
                </div>'''
    return html


def build_pitching_table(s25, s26):
    rows = ""
    for year, s in [("2025", s25), ("2026", s26)]:
        rows += f'''                    <tr>
                        <td class="{'warning' if year == '2026' else 'highlight'}">{year}</td>
                        <td>{s.get('G', '—')}</td>
                        <td>{s.get('GS', '—')}</td>
                        <td>{s.get('W', '—')}-{s.get('L', '—')}</td>
                        <td>{s.get('ERA', '—')}</td>
                        <td>{s.get('IP', '—')}</td>
                        <td>{s.get('K', '—')}</td>
                        <td>{s.get('BB', '—')}</td>
                        <td>{s.get('WHIP', '—')}</td>
                        <td>{s.get('K/9', '—')}</td>
                    </tr>'''
    return rows


def build_batting_table(s25, s26):
    rows = ""
    for year, s in [("2025", s25), ("2026", s26)]:
        rows += f'''                    <tr>
                        <td class="{'warning' if year == '2026' else 'highlight'}">{year}</td>
                        <td>{s.get('G', '—')}</td>
                        <td>{s.get('AVG', '—')}</td>
                        <td>{s.get('OBP', '—')}</td>
                        <td>{s.get('SLG', '—')}</td>
                        <td>{s.get('OPS', '—')}</td>
                        <td>{s.get('HR', '—')}</td>
                        <td>{s.get('RBI', '—')}</td>
                        <td>{s.get('BB', '—')}</td>
                        <td>{s.get('SO', '—')}</td>
                    </tr>'''
    return rows


def build_pitch_arsenal_html(p):
    if not p.get('pitch_arsenal'):
        return ""
    cards = "\n".join(
        f'''                <div class="pitch-card">
                    <h3>{a['name']}</h3>
                    <p><span class="velocity">{a['velocity']}</span></p>
                    <p>{a['desc']}</p>
                </div>'''
        for a in p['pitch_arsenal']
    )
    return f'''
        <div class="section">
            <h2>⚾ 投球武器库</h2>
            <div style="text-align: center; margin: 20px 0;">
                <img src="{p['slug']}_pitch_velocities.png" alt="投球武器库速度" style="width: 100%; max-width: 900px; border-radius: 10px;">
            </div>
            <div class="pitch-arsenal">
{cards}
            </div>
        </div>
'''


def build_grades_grid(grades):
    return "\n".join(
        f'''                <div class="stat-card">
                    <span class="stat-value" style="color: {'#4caf50' if g['value'] >= 60 else '#4fc3f7' if g['value'] >= 50 else '#ff9800'};">{g['value']}</span>
                    <div class="stat-label">{g['label']}</div>
                    <span class="grade {grade_class(g['value'])}">{g['grade']}</span>
                </div>'''
        for g in grades
    )


def build_pros_cons(items):
    return "\n".join(f'                        <li>{item}</li>' for item in items)


def build_html(p):
    html = HTML_TEMPLATE
    html = html.replace('__TITLE__', f"{p['name']} 球探报告")
    html = html.replace('__PLAYER_NAME__', p['name'])
    html = html.replace('__SUBTITLE__', f"Los Angeles Dodgers #{p['number']} | {p['position']} | {p['status']}")
    html = html.replace('__COVER_IMG__', f"{p['slug']}_report_cover.png")
    html = html.replace('__INFO_GRID__', build_info_grid(p))
    html = html.replace('__SCOUTING_SUMMARY__', p['summary'])
    html = html.replace('__CAREER_HIGHLIGHTS__', p['career_highlights'])

    if p['type'] == 'pitcher':
        stats_section = f'''
        <div class="section">
            <h2>📊 2026赛季投球数据</h2>
            <div class="stats-grid">
{build_pitching_grid(p['stats_2026'])}
            </div>
        </div>
'''
        season_section = f'''
        <div class="section">
            <h2>📊 2025 vs 2026 赛季对比</h2>
            <div style="text-align: center; margin: 20px 0;">
                <img src="{p['slug']}_season_comparison.png" alt="赛季对比" style="width: 100%; max-width: 900px; border-radius: 10px;">
            </div>
            <h3 style="margin-top: 30px; color: #4fc3f7;">投球数据对比</h3>
            <table class="comparison-table">
                <thead>
                    <tr><th>赛季</th><th>G</th><th>GS</th><th>W-L</th><th>ERA</th><th>IP</th><th>K</th><th>BB</th><th>WHIP</th><th>K/9</th></tr>
                </thead>
                <tbody>
{build_pitching_table(p['stats_2025'], p['stats_2026'])}
                </tbody>
            </table>
        </div>
'''
    else:
        stats_section = f'''
        <div class="section">
            <h2>📊 2026赛季打击数据</h2>
            <div class="stats-grid">
{build_batting_grid(p['stats_2026'])}
            </div>
        </div>
'''
        season_section = f'''
        <div class="section">
            <h2>📊 2025 vs 2026 赛季对比</h2>
            <div style="text-align: center; margin: 20px 0;">
                <img src="{p['slug']}_season_comparison.png" alt="赛季对比" style="width: 100%; max-width: 900px; border-radius: 10px;">
            </div>
            <h3 style="margin-top: 30px; color: #4fc3f7;">打击数据对比</h3>
            <table class="comparison-table">
                <thead>
                    <tr><th>赛季</th><th>G</th><th>AVG</th><th>OBP</th><th>SLG</th><th>OPS</th><th>HR</th><th>RBI</th><th>BB</th><th>SO</th></tr>
                </thead>
                <tbody>
{build_batting_table(p['stats_2025'], p['stats_2026'])}
                </tbody>
            </table>
        </div>
'''

    html = html.replace('__2026_STATS_SECTION__', stats_section)
    html = html.replace('__SEASON_COMPARISON_SECTION__', season_section)
    html = html.replace('__PITCH_ARSENAL_SECTION__', build_pitch_arsenal_html(p))
    html = html.replace('__ANALYSIS__', p['analysis'])
    html = html.replace('__PROS__', build_pros_cons(p['pros']))
    html = html.replace('__CONS__', build_pros_cons(p['cons']))
    html = html.replace('__GRADES_RADAR__', f"{p['slug']}_overall_grades.png")
    html = html.replace('__GRADES_GRID__', build_grades_grid(p['grades']))
    html = html.replace('__OVERALL_GRADE__', str(p['overall_grade']))
    html = html.replace('__OVERALL_DESC__', p['overall_desc'])
    html = html.replace('__OVERALL_LABEL__', p['overall_label'])
    html = html.replace('__FUTURE_OUTLOOK__', p['future_outlook'])
    html = html.replace('__BACKGROUND__', p['background'])
    html = html.replace('__FOOTER_DATE__', TODAY)
    html = html.replace('__DATA_DATE__', TODAY)
    return html


def build_md(p):
    s26 = p['stats_2026']
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
        f"- **击球/投球**：{p['bats_throws']}",
        f"- **出生日期**：{p['birth_date']}（{p['age']}岁）",
        f"- **MLB首秀**：{p['debut']}",
        "",
        "---",
        "",
        "## 📊 2026赛季数据",
        "",
    ]
    if p['type'] == 'pitcher':
        lines.append(f"| G | GS | W | L | ERA | IP | K | BB | WHIP | K/9 |")
        lines.append(f"|---|---|---|---|---|---|---|---|---|---|")
        lines.append(f"| {s26.get('G','—')} | {s26.get('GS','—')} | {s26.get('W','—')} | {s26.get('L','—')} | {s26.get('ERA','—')} | {s26.get('IP','—')} | {s26.get('K','—')} | {s26.get('BB','—')} | {s26.get('WHIP','—')} | {s26.get('K/9','—')} |")
    else:
        lines.append(f"| G | AVG | OBP | SLG | OPS | HR | RBI | SB | BB | SO |")
        lines.append(f"|---|---|---|---|---|---|---|---|---|---|")
        lines.append(f"| {s26.get('G','—')} | {s26.get('AVG','—')} | {s26.get('OBP','—')} | {s26.get('SLG','—')} | {s26.get('OPS','—')} | {s26.get('HR','—')} | {s26.get('RBI','—')} | {s26.get('SB','—')} | {s26.get('BB','—')} | {s26.get('SO','—')} |")
    lines.extend(["", "---", "", "## 📝 备注", "", "此报告为大谷/佐佐木级别的定制化详细球探报告。", "", f"*数据来源：MLB.com / MLB Stats API | 生成时间：{TODAY}*"])
    return "\n".join(lines)


def generate_report(p):
    output_dir = os.path.join(r'D:\baseball\report', p['slug'])
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating custom report for {p['name']} -> {output_dir}")

    generate_cover(p, os.path.join(output_dir, f"{p['slug']}_report_cover.png"))
    generate_season_chart(p, os.path.join(output_dir, f"{p['slug']}_season_comparison.png"))
    if p['type'] == 'pitcher' and p.get('pitch_arsenal'):
        generate_pitch_velocities(p, os.path.join(output_dir, f"{p['slug']}_pitch_velocities.png"))
    generate_grades_chart(p, os.path.join(output_dir, f"{p['slug']}_overall_grades.png"))

    html = build_html(p)
    html_path = os.path.join(output_dir, f"{p['slug']}-scouting-report.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[OK] HTML: {html_path}")

    md = build_md(p)
    md_path = os.path.join(output_dir, f"{p['slug']}-scouting-report.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"[OK] MD: {md_path}")
    print(f"\n{p['name']} custom detailed report completed!")
