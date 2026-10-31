#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量转换通用模板 HTML 报告为 alex-vesia / tanner-scott 风格。
只修改 HTML 结构和 CSS 排版，**完全保留原有文字内容**。
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re
import sys

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
import generate_remaining_reports as gr

BASE_DIR = Path(r'D:\baseball\report')

TARGETS = {
    'alex-call', 'alex-freeland', 'ben-casparius', 'blake-treinen', 'bobby-miller',
    'brock-stewart', 'brusdar-graterol', 'charlie-barnes', 'dalton-rushing',
    'edwin-diaz', 'eliezer-alfonzo', 'evan-phillips', 'gavin-stone', 'hyeseong-kim',
    'jack-dreyer', 'jake-cousins', 'kyle-hurt', 'landon-knack', 'nick-frasso',
    'paul-gervase', 'river-ryan', 'roki-sasaki', 'ryan-ward', 'will-klein'
}

# alex-vesia / tanner-scott 风格的 CSS
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
        table { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 0.95em; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
        th { background: rgba(0, 90, 156, 0.3); color: #4fc3f7; font-weight: bold; }
        tr:hover { background: rgba(255, 255, 255, 0.05); }
        blockquote { border-left: 4px solid #4fc3f7; padding-left: 15px; margin: 15px 0; color: #b0bec5; font-style: italic; }
        strong { color: #4fc3f7; }
        hr { border: none; border-top: 1px solid rgba(255, 255, 255, 0.1); margin: 20px 0; }
        @media (max-width: 768px) { .header h1 { font-size: 2em; } .stats-grid { grid-template-columns: repeat(2, 1fr); } }
"""

# 标题映射：旧标题 -> 新标题
TITLE_MAP = {
    '📋 基本信息': '基本信息',
    '📊 2026 赛季统计数据': '📊 2026赛季数据',
    '📊 生涯统计数据': '📊 生涯数据',
    '📊 生涯与小联盟背景': '📖 背景故事',
    '📊 赛季数据对比': '📊 2025 vs 2026 赛季对比',
    '🎯 投球武器库': '⚾ 投球武器库',
    '📖 背景故事与历史成就': '📖 背景故事',
    # 以下板块会被移除
    '📅 2026 赛季近期比赛日志': '__REMOVE__',
    '📅 2026 赛季近期比赛日志（部分）': '__REMOVE__',
    '📅 2026赛季比赛日志（部分）': '__REMOVE__',
    '📅 2026赛季比赛日志': '__REMOVE__',
    '📚 数据来源': '__REMOVE__',
    '📈 数据图表': '__REMOVE__',
    '🛡️ 守备与位置弹性': '__REMOVE__',
}


def detect_type(soup):
    """根据报告内容判断是投手还是打者"""
    text = soup.get_text()
    if '投球武器库' in text or '先发投手' in text or '后援' in text or 'ERA' in text:
        return 'pitcher'
    return 'batter'


def extract_meta_info(soup, name_slug):
    """从 blockquote 或基本信息表格中提取球员元信息（背号 + 状态）"""
    # 1. 尝试从 blockquote 提取
    for bq in soup.find_all('blockquote'):
        text = bq.get_text(strip=True)
        m = re.search(r'Los Angeles Dodgers\s*#?(\d+|—)\s*\|\s*([^|]+)\s*\|\s*(.+?)\s*\*?', text)
        if m:
            return {'number': m.group(1).strip().strip('*'), 'position': m.group(3).strip().strip('*')}

    # 2. 从基本信息表格提取
    info_section = None
    for sec in soup.find_all('div', class_='section'):
        h2 = sec.find('h2')
        if h2 and '基本信息' in h2.get_text():
            info_section = sec
            break
    number = ''
    status = ''
    if info_section:
        for tr in info_section.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) >= 2:
                label = tds[0].get_text(strip=True)
                value = tds[1].get_text(strip=True)
                if '背号' in label:
                    number = value.replace('#', '').strip()
                if '状态' in label:
                    status = value

    # 4. 如果 still 没有 number，从 PLAYER_CONFIGS 查找
    if (number or '—') == '—':
        for cfg in gr.PLAYER_CONFIGS:
            # 简单按 slug 匹配
            cfg_slug = cfg['name'].lower().replace(' ', '-').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n').replace('ü', 'u')
            if cfg_slug == name_slug:
                number = cfg.get('number', '')
                break

    return {'number': number or '—', 'position': status or '—'}


def build_new_subtitle(name, meta, player_type, name_slug):
    pos = '投手' if player_type == 'pitcher' else '打者'
    status = meta.get('position', '')
    # 如果 status 已经包含 pos，避免重复
    if status and status != '—' and not status.startswith(pos):
        return f"Los Angeles Dodgers #{meta['number']} | {pos} | {status}"
    elif status and status != '—':
        return f"Los Angeles Dodgers #{meta['number']} | {status}"
    return f"Los Angeles Dodgers #{meta['number']} | {pos}"


def normalize_title(text):
    """去除标题中的空格，用于模糊匹配"""
    return text.replace(' ', '').replace('\u3000', '')


def remove_redundant_sections(soup):
    """删除不需要的 section"""
    for sec in list(soup.find_all('div', class_='section')):
        h2 = sec.find('h2')
        if h2:
            norm = normalize_title(h2.get_text(strip=True))
            for k, v in TITLE_MAP.items():
                if normalize_title(k) == norm and v == '__REMOVE__':
                    sec.decompose()
                    break


def unify_section_titles(soup, player_type):
    """统一 section 标题"""
    for h2 in soup.find_all('h2'):
        text = h2.get_text(strip=True)
        norm = normalize_title(text)
        for k, v in TITLE_MAP.items():
            if normalize_title(k) == norm and v != '__REMOVE__':
                h2.string = v
                break
        # 投手/打者数据标题细分
        if norm == normalize_title('📊 2026 赛季统计数据') or norm == normalize_title('📊 2026赛季数据'):
            h2.string = '📊 2026赛季投球数据' if player_type == 'pitcher' else '📊 2026赛季打击数据'


def clean_header(soup, name, meta, player_type, name_slug):
    """清理 header 区域，移除顶部 blockquote，更新 subtitle"""
    # 移除 header 后面的 blockquote 和 hr
    container = soup.find('div', class_='container')
    if not container:
        return
    # 移除 container 中 header 后面的 blockquote 和空 p
    removed = False
    for tag in list(container.children):
        if tag.name == 'div' and 'header' in tag.get('class', []):
            removed = True
            # 更新 subtitle
            sub = tag.find('p', class_='subtitle')
            if sub:
                sub.string = build_new_subtitle(name, meta, player_type, name_slug)
            continue
        if removed and tag.name in ('blockquote', 'p', 'hr'):
            tag.decompose()


def wrap_basic_info_as_card(soup):
    """把基本信息 section 包装成 player-card 样式（保留原有内容）"""
    for sec in soup.find_all('div', class_='section'):
        h2 = sec.find('h2')
        if h2 and h2.get_text(strip=True) == '基本信息':
            # 保留 section 内的内容，但添加 player-card class
            sec['class'] = sec.get('class', []) + ['player-card']
            # 移除 h2（alex-vesia 风格中 player-card 内部用 h2  player-info）
            # 这里我们不强制改太多，只把 h2 保留，保持内容
            break


def build_footer(soup):
    """统一 footer"""
    container = soup.find('div', class_='container')
    if not container:
        return
    # 移除现有 footer
    for f in list(container.find_all('div', class_='footer')):
        f.decompose()
    # 移除最后的 stray <p> 如 *⚾ 洛杉矶道奇队球探报告*</p>
    for p in list(container.find_all('p')):
        text = p.get_text(strip=True)
        if '⚾ 洛杉矶道奇队球探报告' in text or '数据来源' in text:
            p.decompose()
    # 添加新 footer
    footer = soup.new_tag('div', **{'class': 'footer'})
    footer.append(soup.new_tag('p'))
    footer.find('p').string = '数据来源：MLB.com | Baseball Savant (Statcast) | Fangraphs | MLB Stats API'
    p2 = soup.new_tag('p')
    from datetime import datetime
    p2.string = f'报告生成时间：{datetime.now().strftime("%Y-%m-%d")} | 数据截止日期：{datetime.now().strftime("%Y-%m-%d")}'
    footer.append(p2)
    p3 = soup.new_tag('p')
    p3.string = '⚾ 洛杉矶道奇队球探报告'
    footer.append(p3)
    container.append(footer)


def process_html(html_path, name, name_slug):
    html = html_path.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    # 替换 CSS
    style = soup.find('style')
    if style:
        style.string = ALEX_VESIA_CSS

    # 判断类型
    player_type = detect_type(soup)

    # 提取元信息
    meta = extract_meta_info(soup, name_slug)

    # 清理 header
    clean_header(soup, name, meta, player_type, name_slug)

    # 删除冗余 section
    remove_redundant_sections(soup)

    # 统一标题
    unify_section_titles(soup, player_type)

    # 把基本信息 section 改为 player-card 外观
    wrap_basic_info_as_card(soup)

    # 统一 footer
    build_footer(soup)

    # 格式化输出
    return soup.prettify()


def main():
    from datetime import datetime
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting HTML style unification...")
    print(f"Targets: {len(TARGETS)}")

    for slug in sorted(TARGETS):
        player_dir = BASE_DIR / slug
        html_path = player_dir / f"{slug}-scouting-report.html"
        if not html_path.exists():
            print(f"  [SKIP] {slug}: HTML not found")
            continue
        try:
            new_html = process_html(html_path, slug.replace('-', ' ').title(), slug)
            html_path.write_text(new_html, encoding='utf-8')
            print(f"  [OK] {slug}")
        except Exception as e:
            print(f"  [FAIL] {slug}: {e}")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Done")


if __name__ == '__main__':
    main()
