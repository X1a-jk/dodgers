#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将球探报告 Markdown 重新生成为 alex-vesia / tanner-scott 风格的 HTML。
保留原有文字内容，统一结构与排版，补齐缺失板块（如职业生涯亮点）。
"""
import re
import os
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r'D:\baseball\report')
LOG_PATH = BASE_DIR / 'regenerate_target_reports.log'

TARGETS = [
    'ben-casparius', 'blake-treinen', 'bobby-miller', 'brock-stewart',
    'brusdar-graterol', 'gavin-stone', 'jack-dreyer', 'jake-cousins',
    'kyle-hurt', 'landon-knack', 'nick-frasso', 'paul-gervase',
    'river-ryan', 'will-klein'
]

ALEX_VESIA_CSS = """
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
        .section table { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 0.95em; }
        .section th, .section td { padding: 12px; text-align: left; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
        .section th { background: rgba(0, 90, 156, 0.3); color: #4fc3f7; font-weight: bold; }
        .section tr:hover { background: rgba(255, 255, 255, 0.05); }
        .section h3 { color: #4fc3f7; margin: 20px 0 12px 0; font-size: 1.2em; }
        .section p { margin-bottom: 12px; }
        .section blockquote { border-left: 4px solid #4fc3f7; padding-left: 15px; margin: 15px 0; color: #b0bec5; font-style: italic; }
        .section strong { color: #4fc3f7; }
        .section ul { margin-left: 25px; margin-bottom: 15px; }
        .section li { margin-bottom: 8px; }
        @media (max-width: 768px) { .header h1 { font-size: 2em; } .stats-grid { grid-template-columns: repeat(2, 1fr); } }
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__TITLE__</title>
    <style>__CSS__</style>
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

        <div class="section">
            <h2>📊 2026赛季投球数据</h2>
            <div class="stats-grid">
__2026_STATS__
            </div>
        </div>

        <div class="section">
            <h2>📊 2025 vs 2026 赛季对比</h2>
            <div style="text-align: center; margin: 20px 0;">
                <img src="__SEASON_COMPARISON_IMG__" alt="赛季对比" style="width: 100%; max-width: 900px; border-radius: 10px;">
            </div>
__SEASON_COMPARISON_TABLE__
        </div>

        <div class="section">
            <h2>⚾ 投球武器库</h2>
            <div class="pitch-arsenal">
__PITCH_ARSENAL__
            </div>
        </div>

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
                <img src="__OVERALL_GRADES_IMG__" alt="综合评分雷达图" style="width: 100%; max-width: 600px; border-radius: 10px;">
            </div>
__GRADES_TABLE__
            <div style="margin-top: 30px; text-align: center;">
                <h3 style="color: #4fc3f7; margin-bottom: 15px;">总体潜力评分</h3>
                <div style="font-size: 4em; color: #4caf50; font-weight: bold;">__OVERALL_GRADE__</div>
                <p style="color: #90a4ae; margin-top: 10px;">__OVERALL_DESC__</p>
                <p style="margin-top: 15px;"><span class="grade grade-__OVERALL_GRADE_CLASS__" style="font-size: 1.2em;">__OVERALL_LABEL__</span></p>
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


def format_inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text


def parse_markdown_sections(md_text):
    """按一级/二级标题切分 Markdown，返回 {标题: 内容}。
    内容中保留 ### 子标题，方便后续进一步切分。"""
    sections = {}
    current_title = None
    current_lines = []

    for line in md_text.splitlines():
        m = re.match(r'^(#{1,2})\s+(.*)$', line)
        if m:
            if current_title is not None:
                sections[current_title] = '\n'.join(current_lines).strip()
            current_title = m.group(2).strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_title is not None:
        sections[current_title] = '\n'.join(current_lines).strip()
    return sections


def split_subsections(text):
    """把一段内容按 ### 子标题切分为 [(子标题, 内容), ...]。"""
    parts = re.split(r'\n###\s+', text)
    result = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        first_line = part.split('\n', 1)[0].strip()
        rest = part[len(first_line):].strip()
        result.append((first_line, rest))
    return result


def first_table_only(text):
    """只取第一个 Markdown 表格（遇到空行或子标题停止）。"""
    lines = []
    for line in text.splitlines():
        if line.startswith('###'):
            break
        if line.strip() == '' and lines:
            # 如果遇到空行且已经收集到表格行，则停止
            break
        lines.append(line)
    return parse_table(lines)


def parse_table(lines):
    """从 Markdown 表格行解析为列表。"""
    rows = []
    for line in lines:
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.split('|')]
        cells = [c for c in cells if c]
        if all(set(c) <= set('-:| ') for c in cells):
            continue
        rows.append(cells)
    return rows


def table_to_info_grid(table_rows):
    """把基本信息表转换为 info-grid 的 div。"""
    items = []
    label_map = {
        '全名': '全名', '姓名': '全名',
        '出生日期': '出生日期', '年龄': '年龄',
        '出生地': '出生地', '身高/体重': '身高/体重',
        '投球/击球': '投球/击球', '击球/投球': '击球/投球',
        '位置': '位置', 'MLB首秀': 'MLB首秀', '选秀': '选秀',
        '大学': '大学', '绰号': '绰号', '背号': '背号', '状态': '状态'
    }
    for row in table_rows[1:]:
        if len(row) < 2:
            continue
        raw_label = row[0].replace('**', '').strip()
        label = label_map.get(raw_label, raw_label)
        value = format_inline(row[1])
        items.append(f'                    <div class="info-item"><div class="label">{label}</div><div class="value">{value}</div></div>')
    return '\n'.join(items)


def table_to_stat_cards(table_rows, player_type='pitcher'):
    """把 2026 赛季统计数据表转换为 stat-card。"""
    cards = []
    label_color_map = {
        'ERA': '#4caf50', 'WHIP': '#4caf50',
        'AVG': '#4caf50', 'OPS': '#4caf50', 'SLG': '#4caf50', 'OBP': '#4caf50'
    }
    for row in table_rows[1:]:
        if len(row) < 2:
            continue
        label = row[0].replace('**', '').strip()
        # 去掉括号内英文缩写
        label_short = re.sub(r'\s*[\(（].*?[\)）]', '', label).strip()
        value = format_inline(row[1])
        color = label_color_map.get(label_short, '#4fc3f7')
        cards.append(f'                <div class="stat-card">\n                    <span class="stat-value" style="color: {color};">{value}</span>\n                    <div class="stat-label">{label_short}</div>\n                </div>')
    return '\n'.join(cards)


def table_to_html_table(table_rows, table_class='comparison-table'):
    """把 Markdown 表格转为 HTML 表格。"""
    if not table_rows:
        return ''
    html = f'<table class="{table_class}">\n<thead>\n<tr>'
    for cell in table_rows[0]:
        html += f'<th>{format_inline(cell)}</th>'
    html += '</tr>\n</thead>\n<tbody>\n'
    for row in table_rows[1:]:
        html += '<tr>'
        for cell in row:
            html += f'<td>{format_inline(cell)}</td>'
        html += '</tr>\n'
    html += '</tbody>\n</table>'
    return html


def markdown_to_html_paragraphs(text):
    """把 Markdown 段落和列表转为简单 HTML，保留标题。"""
    lines = text.splitlines()
    out = []
    in_list = False
    list_items = []
    in_table = False
    table_lines = []

    def flush_list():
        nonlocal in_list, list_items
        if in_list and list_items:
            out.append('<ul>')
            for item in list_items:
                out.append(f'<li>{format_inline(item)}</li>')
            out.append('</ul>')
            list_items = []
            in_list = False

    def flush_table():
        nonlocal in_table, table_lines
        if in_table and table_lines:
            rows = parse_table(table_lines)
            if rows:
                out.append(table_to_html_table(rows, 'comparison-table'))
            table_lines = []
            in_table = False

    for line in lines:
        s = line.strip()
        if s.startswith('### '):
            flush_list(); flush_table()
            out.append(f'<h3>{format_inline(s[4:])}</h3>')
        elif s.startswith('|'):
            flush_list()
            table_lines.append(line)
            in_table = True
        elif s.startswith('- ') or s.startswith('- ✅') or s.startswith('- ❌'):
            flush_table()
            item = s[2:].strip()
            list_items.append(item)
            in_list = True
        elif s == '' or s == '---':
            flush_list(); flush_table()
        elif s.startswith('> '):
            flush_list(); flush_table()
            out.append(f'<blockquote>{format_inline(s[2:])}</blockquote>')
        else:
            flush_list(); flush_table()
            out.append(f'<p>{format_inline(s)}</p>')
    flush_list(); flush_table()
    return '\n'.join(out)


def parse_pitch_arsenal(section_text):
    """解析投球武器库，返回 pitch-card HTML 列表。"""
    cards = []
    subsections = split_subsections(section_text)
    for title, content in subsections:
        # 清理标题中的 ### 和 emoji
        title_clean = re.sub(r'^#+\s*', '', title).strip()
        title_clean = re.sub(r'^[🔥🌪️💫⚡🎯⚾]+\s*', '', title_clean).strip()
        # 提取球速：支持 **球速**：96-100 mph（标签单独加粗）
        velo_match = re.search(r'\*\*\s*球速\s*\*\*\s*[：:]\s*\*?\*?\s*([\d\-–]+\s*mph)', content)
        velocity = velo_match.group(1).strip() if velo_match else '—'
        # 提取评分：支持 **评分**：**A-** 或 **评分：** **B**
        grade_match = re.search(r'(?:\*\*\s*评分\s*\*\*\s*[：:]\s*\*?\*?\s*\*?\*?|\*\*\s*评分\s*[：:]\s*\*\*)\s*\*?\*?\s*([A-D][+-]?)', content)
        grade = grade_match.group(1) if grade_match else ''
        # 描述：去掉球速、评分、空行
        desc_lines = []
        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith('-'):
                line = line[1:].strip()
            # 去掉整行的球速/评分行
            if re.match(r'^(\*\*\s*球速\s*\*\*\s*[：:]\s*\*?[\d\-–]+\s*mph)', line):
                continue
            if re.match(r'^(\*\*\s*评分\s*\*\*\s*[：:]\s*\*?\*?\s*\*?\*?\s*[A-D][+-]?)', line):
                continue
            if re.match(r'^(\*\*\s*评分\s*[：:]\s*\*\*\s*\*?\*?\s*[A-D][+-]?)', line):
                continue
            # 清理行首尾 **
            line = re.sub(r'^\*+', '', line)
            line = re.sub(r'\*+$', '', line)
            if line:
                desc_lines.append(format_inline(line))
        desc = ' '.join(desc_lines).strip()
        desc = re.sub(r'\s+--$', '', desc)
        desc = re.sub(r'^--\s*$', '', desc)
        if not desc or desc == '--':
            desc = '该球种是该球员投球组合中的重要武器，详见上方评分与球速。'
        grade_class = f'grade-{grade[0].lower()}' if grade else 'grade-b'
        grade_badge = f'<span class="grade {grade_class}">{grade}</span>' if grade else ''
        cards.append(f'''                <div class="pitch-card">
                    <h3>{format_inline(title_clean)} {grade_badge}</h3>
                    <div class="velocity">{velocity}</div>
                    <p style="margin-top: 10px; color: #b0bec5;">{desc}</p>
                </div>''')
    return '\n'.join(cards) if cards else '<p>暂无投球武器库数据。</p>'


def parse_pros_cons(section_text):
    """解析优势/劣势，返回 (pros_html, cons_html)。"""
    pros = []
    cons = []
    current = None
    for line in section_text.splitlines():
        s = line.strip()
        if '优势' in s and ('Strengths' in s or s.startswith('###')):
            current = 'pros'
            continue
        if '劣势' in s and ('Weaknesses' in s or s.startswith('###')):
            current = 'cons'
            continue
        if s.startswith('- ') or s.startswith('- ✅') or s.startswith('- ❌'):
            item = s[2:].strip()
            item = re.sub(r'^[✅❌]\s*', '', item)
            item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
            if current == 'pros':
                pros.append(f'                        <li>{item}</li>')
            elif current == 'cons':
                cons.append(f'                        <li>{item}</li>')
    return '\n'.join(pros), '\n'.join(cons)


def extract_pros_cons_from_analysis(analysis_text):
    """从球探分析中的 ### 优势 / ### 劣势子板块提取，返回 (pros_html, cons_html)。"""
    if not analysis_text:
        return '', ''
    pros = []
    cons = []
    current = None
    for line in analysis_text.splitlines():
        s = line.strip()
        if s.startswith('### ') and ('优势' in s or 'Strengths' in s or '优点' in s):
            current = 'pros'
            continue
        if s.startswith('### ') and ('劣势' in s or 'Weaknesses' in s or '弱点' in s or '缺点' in s):
            current = 'cons'
            continue
        if s.startswith('- ') or s.startswith('- ✅') or s.startswith('- ❌'):
            item = s[2:].strip()
            item = re.sub(r'^[✅❌]\s*', '', item)
            item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
            if current == 'pros':
                pros.append(f'                        <li>{item}</li>')
            elif current == 'cons':
                cons.append(f'                        <li>{item}</li>')
    return '\n'.join(pros), '\n'.join(cons)


def extract_overall_grade(grades_text):
    """从综合评分段提取总体评分。"""
    m = re.search(r'总体评分[:：]\s*\*\*(\d+)\*\*', grades_text)
    if m:
        return int(m.group(1))
    m = re.search(r'总体评分[:：]\s*(\d+)', grades_text)
    if m:
        return int(m.group(1))
    return 50


def extract_overall_label(grades_text):
    """提取总体评级标签，如 'B 级 / 优质年轻后援'。"""
    m = re.search(r'（(.+?)）', grades_text)
    if m:
        return m.group(1)
    m = re.search(r'总体评分.*?(B\+?级|A\-?级|C\+?级|D\+?级)', grades_text)
    if m:
        return m.group(1)
    return ''


def build_career_highlights(slug, sections, player_name, status, debut):
    """根据背景故事和基本信息构建职业生涯亮点。"""
    highlights = []
    bg = sections.get('📖 背景故事与历史成就', '') + sections.get('📖 背景故事', '')

    # 大学（优先匹配 University/College/State/Institute，避开中学）
    for college_match in re.finditer(r'(?:毕业于|就读于|进入|来自)\s*([A-Z][A-Za-z\s&.]+(?:University|College|State|Institute|School))', bg):
        college = college_match.group(1).strip()
        if 'High School' not in college:
            highlights.append(f'<div class="career-highlight"><h4>🎓 大学时期 - {college}</h4><p>{player_name} 在大学时期展现出成为大联盟投手的潜力，积累了扎实的基础与比赛经验。</p></div>')
            break

    # 选秀
    draft_match = re.search(r'(\d{4})\s*年\s*MLB\s*选秀.*?第\s*(\d+)\s*轮', bg)
    if draft_match:
        year, round_ = draft_match.group(1), draft_match.group(2)
        highlights.append(f'<div class="career-highlight"><h4>⭐ {year}年 - 第{round_}轮选中</h4><p>{player_name} 在 {year} 年 MLB 选秀第 {round_} 轮被选中，开启职业棒球生涯。</p></div>')

    # MLB 首秀（仅当 debut 是日期格式时）
    if debut and debut != '—' and not re.search(r'尚未|未|None|N/A', debut, re.IGNORECASE) and re.search(r'\d{4}', debut):
        highlights.append(f'<div class="career-highlight"><h4>🌟 {debut[:4]}年 - 大联盟首秀</h4><p>{player_name} 于 {debut} 登上大联盟，开始在高水平舞台展现自己的实力。</p></div>')

    # 状态
    if 'IL' in status:
        highlights.append(f'<div class="career-highlight"><h4>🏥 当前状态 - {status} 伤病名单</h4><p>{player_name} 目前因伤位于 {status} 名单。恢复后，他将重新回到道奇的投手阵容中。</p></div>')
    elif status == 'Minors':
        highlights.append(f'<div class="career-highlight"><h4>🔮 当前状态 - 小联盟发展中</h4><p>{player_name} 目前位于道奇小联盟体系，是球队长期深度规划的一部分。</p></div>')
    else:
        highlights.append(f'<div class="career-highlight"><h4>🔵 道奇时期 - 活跃名单贡献者</h4><p>{player_name} 目前是洛杉矶道奇活跃名单的一员，作为投手为球队提供稳定贡献。</p></div>')

    return '\n'.join(highlights) if highlights else f'<div class="career-highlight"><h4>🌟 职业生涯</h4><p>{player_name} 在职业棒球生涯中持续成长，为道奇队提供投手深度。</p></div>'


def extract_basic_info(sections):
    """从基本信息段解析关键字段。"""
    info = {}
    basic = sections.get('📋 基本信息', '')
    rows = parse_table(basic.splitlines())
    for row in rows[1:]:
        if len(row) < 2:
            continue
        key = row[0].replace('**', '').strip()
        val = row[1].strip()
        info[key] = val
    return info


def build_html(slug, md_text):
    sections = parse_markdown_sections(md_text)
    name_match = re.search(r'^#\s+(.+?)\s+球探报告', md_text, re.MULTILINE)
    player_name = name_match.group(1).strip() if name_match else slug.replace('-', ' ').title()

    info = extract_basic_info(sections)
    status = info.get('状态', '活跃')
    debut = info.get('MLB首秀', '—')
    number = info.get('背号', '#—').replace('#', '')
    position = '投手'
    # 状态清洗（用于 subtitle）
    def clean_status(s):
        s = s.strip()
        if 'IL' in s:
            m = re.search(r'IL-\d+', s)
            return m.group(0) if m else 'IL'
        if '小联盟' in s or 'Minors' in s or 'AAA' in s or 'AA' in s:
            return 'Minors'
        return s

    status_clean = clean_status(status)
    subtitle = f"Los Angeles Dodgers #{number} | {position} | {status_clean}"

    # 基本信息表格 -> info-grid
    basic_rows = parse_table(sections.get('📋 基本信息', '').splitlines())
    info_grid = table_to_info_grid(basic_rows)

    # 球探总评（紧跟在基本信息后的 ### 球探总评）
    summary = ''
    basic_text = sections.get('📋 基本信息', '')
    summary_match = re.search(r'###\s+球探总评\s*\n(.+?)(?=\n---|\n##|$)', basic_text, re.DOTALL)
    if summary_match:
        summary = markdown_to_html_paragraphs(summary_match.group(1).strip())
    if not summary:
        # 尝试从 2026 数据段上方找
        summary = '<p>详细球探总评见下文分析。</p>'

    # 职业生涯亮点
    career_highlights = build_career_highlights(slug, sections, player_name, status_clean, debut)

    # 2026 数据 -> stat-cards（只取该section内第一个表格）
    stats_2026_section = sections.get('📊 2026 赛季统计数据', sections.get('📊 2026赛季数据', ''))
    fallback_to_minor = False
    if not stats_2026_section:
        # 如果只有小联盟/生涯背景，作为说明表格
        stats_2026_section = sections.get('📊 生涯与小联盟背景', '')
        fallback_to_minor = True
    stats_rows = first_table_only(stats_2026_section)
    stat_cards = table_to_stat_cards(stats_rows) if stats_rows else f'<p style="color: #90a4ae;">2026 年大联盟样本有限，数据主要参考小联盟与过往表现。</p>'

    # 2025 vs 2026 对比表（可能在 📊 2026 赛季统计数据 的subsection里）
    comp_section = sections.get('📊 2025 vs 2026 赛季对比', '')
    if not comp_section:
        for sub_title, sub_text in split_subsections(stats_2026_section):
            if '2025 vs 2026' in sub_title or '赛季对比' in sub_title:
                comp_section = sub_text
                break
    comp_rows = first_table_only(comp_section)
    comp_table = table_to_html_table(comp_rows, 'comparison-table')
    comp_notes = markdown_to_html_paragraphs(re.sub(r'\|[^\n]*\|', '', comp_section))

    # 生涯数据表（如果有的话）单独保留，但避免把小联盟背景表标成大联盟生涯数据
    career_rows = []
    for sub_title, sub_text in split_subsections(stats_2026_section):
        if '大联盟生涯' in sub_title or 'MLB生涯' in sub_title:
            career_rows = first_table_only(sub_text)
            break
    career_table = table_to_html_table(career_rows, 'comparison-table')
    if career_table and not fallback_to_minor:
        career_table = f'<h3 style="margin-top: 30px; color: #4fc3f7;">大联盟生涯数据</h3>\n{career_table}'
    elif career_table and fallback_to_minor:
        career_table = f'<h3 style="margin-top: 30px; color: #4fc3f7;">小联盟与背景信息</h3>\n{career_table}'

    # 投球武器库
    pitch_section = sections.get('🎯 投球武器库', sections.get('⚾ 投球武器库', ''))
    pitch_cards = parse_pitch_arsenal(pitch_section)

    # 检测 2026 数据是否全是占位符 "—"
    all_dash = bool(stats_rows) and all(len(r) >= 2 and str(r[1]).strip() in ('—', '-', '') for r in stats_rows[1:])
    has_placeholder_note = any('小联盟数据未纳入' in str(r[1]) or '未纳入' in str(r[1]) for r in stats_rows[1:] if len(r) >= 2)
    if all_dash or has_placeholder_note:
        stat_cards = f'<p style="color: #90a4ae;">2026 年大联盟样本有限或尚未登上大联盟，数据主要参考小联盟与过往表现。</p>'

    # 球探分析
    analysis = markdown_to_html_paragraphs(sections.get('🔍 球探分析', ''))

    # 优势劣势：优先找独立板块，否则从球探分析中提取
    analysis_section = sections.get('🔍 球探分析', '')
    pros_cons_section = sections.get('✅ 优势 vs ❌ 劣势', sections.get('优势 vs 劣势', ''))
    pros, cons = parse_pros_cons(pros_cons_section)
    if not pros and not cons:
        # 从分析板块的子列表里提取
        pros, cons = extract_pros_cons_from_analysis(analysis_section)

    # 综合评分
    grades_section = sections.get('📊 综合评分', '')
    grades_rows = parse_table(grades_section.splitlines())
    grades_table = table_to_html_table(grades_rows, 'comparison-table')
    overall_grade = extract_overall_grade(grades_section)
    overall_label = extract_overall_label(grades_section)
    overall_desc_match = re.search(r'>\s*(.+)', grades_section)
    overall_desc = overall_desc_match.group(1).strip() if overall_desc_match else overall_label

    # 未来展望
    future = markdown_to_html_paragraphs(sections.get('🔮 未来展望', ''))

    # 背景故事
    background = markdown_to_html_paragraphs(sections.get('📖 背景故事与历史成就', sections.get('📖 背景故事', '')))
    if not background:
        background = f'<p>{player_name} 的背景故事与生涯轨迹详见职业生涯亮点与球探分析。</p>'

    # 图片路径（优先使用 slug 前缀的版本）
    cover_img = f'{slug}_report_cover.png'
    season_img = f'{slug}_season_comparison.png'
    grades_img = f'{slug}_overall_grades.png'

    # 确定总体等级 class
    grade_letter = overall_label[0].lower() if overall_label else 'b'
    if grade_letter not in 'abcd':
        grade_letter = 'b'

    today = datetime.now().strftime('%Y-%m-%d')

    html = HTML_TEMPLATE
    html = html.replace('__TITLE__', f'{player_name} 球探报告')
    html = html.replace('__PLAYER_NAME__', player_name)
    html = html.replace('__SUBTITLE__', subtitle)
    html = html.replace('__CSS__', ALEX_VESIA_CSS)
    html = html.replace('__COVER_IMG__', cover_img)
    html = html.replace('__INFO_GRID__', info_grid)
    html = html.replace('__SCOUTING_SUMMARY__', summary)
    html = html.replace('__CAREER_HIGHLIGHTS__', career_highlights)
    html = html.replace('__2026_STATS__', stat_cards)
    html = html.replace('__SEASON_COMPARISON_IMG__', season_img)
    html = html.replace('__SEASON_COMPARISON_TABLE__', comp_table + '\n' + career_table + '\n' + comp_notes)
    html = html.replace('__PITCH_ARSENAL__', pitch_cards)
    html = html.replace('__ANALYSIS__', analysis)
    html = html.replace('__PROS__', pros if pros else '<li>优势分析见上文。</li>')
    html = html.replace('__CONS__', cons if cons else '<li>劣势分析见上文。</li>')
    html = html.replace('__OVERALL_GRADES_IMG__', grades_img)
    html = html.replace('__GRADES_TABLE__', grades_table)
    html = html.replace('__OVERALL_GRADE__', str(overall_grade))
    html = html.replace('__OVERALL_DESC__', overall_desc)
    html = html.replace('__OVERALL_LABEL__', overall_label)
    html = html.replace('__OVERALL_GRADE_CLASS__', grade_letter)
    html = html.replace('__FUTURE_OUTLOOK__', future)
    html = html.replace('__BACKGROUND__', background)
    html = html.replace('__FOOTER_DATE__', today)
    html = html.replace('__DATA_DATE__', today)

    return html


def main():
    logs = []
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logs.append(f'[{today}] 开始重新生成 {len(TARGETS)} 名球员报告')

    for slug in TARGETS:
        player_dir = BASE_DIR / slug
        md_path = player_dir / f'{slug}-scouting-report.md'
        html_path = player_dir / f'{slug}-scouting-report.html'
        if not md_path.exists():
            logs.append(f'[SKIP] {slug}: Markdown 不存在')
            continue
        try:
            md_text = md_path.read_text(encoding='utf-8')
            html = build_html(slug, md_text)
            html_path.write_text(html, encoding='utf-8')
            logs.append(f'[OK] {slug}: 已生成 {html_path.name}')
        except Exception as e:
            import traceback
            logs.append(f'[FAIL] {slug}: {e}')
            logs.append(traceback.format_exc())

    LOG_PATH.write_text('\n'.join(logs), encoding='utf-8')
    print('\n'.join(logs))


if __name__ == '__main__':
    main()
