# -*- coding: utf-8 -*-
"""
regen-covers-old-style.py — 全部球员报告头图返工为旧版风格（report.bak-20261017 风格）

背景：2026-10-17 最终版报告生成时 generate-final-reports.py 用了新版封面（笑脸印章式），
用户要求恢复旧版风格（参考 report.bak-20261017\\kyle-tucker\\tucker_report_cover.png）：
深蓝 #1a1a2e 底、居中排版、SCOUTING REPORT 2026 橙色标题、8 格数据、标语、页脚。

做法：
1. 数据全部来自本地 data\\final-stats.json（2025/2026 完整打击+投球，按 MLB id）+
   data\\season-roster.json（名单/位置）+ data\\depth-chart.json（背号），不访问网络。
2. 封面写到各球员 HTML 实际引用的文件名下（不动 HTML）。
3. 目录里若残留 <slug>_report_cover.png（未被引用的旧新版文件）也一并覆盖为旧版风格，避免混淆。
4. 打者 8 格：AVG OPS HR RBI / SB OBP Age 2025OPS（无2025数据则改 G）
   投手 8 格：ERA WHIP K IP / W-L K/9 BB/9 Age；二刀流用打击格 + 二刀流标语。
"""
import io
import json
import os
import re
import unicodedata
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

BASE = r'D:\baseball'
REPORT = os.path.join(BASE, 'report')
DATA = os.path.join(BASE, 'data')
TODAY = datetime.now().strftime('%Y-%m-%d')

POS_CN = {
    'RF': ('右外野手', '外野'), 'LF': ('左外野手', '外野'), 'CF': ('中外野手', '外野'),
    'SS': ('游击手', '内野'), '2B': ('二垒手', '内野'), '3B': ('三垒手', '内野'),
    '1B': ('一垒手', '内野'), 'C': ('捕手', '捕手'), 'DH': ('指定打击', '重炮'),
    'P': ('投手', '投手'), 'OF': ('外野手', '外野'), 'IF': ('内野手', '内野'),
    'TWP': ('二刀流', '二刀流'),
}


def slugify(name):
    s = unicodedata.normalize('NFKD', name)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.lower().replace(' ', '-')


def fmt1(x):
    return f"{float(x):.1f}" if x not in (None, '', '-') else '—'


def load_json(p):
    return json.load(io.open(p, encoding='utf-8'))


def main():
    roster = load_json(os.path.join(DATA, 'season-roster.json'))['players']
    stats = load_json(os.path.join(DATA, 'final-stats.json'))
    dc = load_json(os.path.join(DATA, 'depth-chart.json'))
    jersey = {}

    def _take(group):
        for p in group:
            jersey[p['name']] = str(p.get('jersey', ''))

    _take(dc.get('starters') or [])
    _take(dc.get('relievers') or [])
    for col in dc.get('columns') or []:
        _take(col.get('players') or [])

    ok, skipped = [], []
    for rp in roster:
        name, pid, pos = rp['name'], str(rp['id']), rp['pos']
        slug = slugify(name)
        pdir = os.path.join(REPORT, slug)
        if not os.path.isdir(pdir):
            skipped.append((name, 'no dir'))
            continue
        htmls = [f for f in os.listdir(pdir) if f.endswith('.html')]
        if not htmls:
            skipped.append((name, 'no html'))
            continue
        html = io.open(os.path.join(pdir, htmls[0]), encoding='utf-8').read()
        m = re.search(r'([\w-]+_report_cover\.png)', html)
        if not m:
            skipped.append((name, 'no cover ref'))
            continue
        cover_name = m.group(1)

        h26 = stats['hitting_2026'].get(pid)
        p26 = stats['pitching_2026'].get(pid)
        h25 = stats['hitting_2025'].get(pid, {})
        age = (h26 or p26 or {}).get('age', '—')
        pa26 = (h26 or {}).get('plateAppearances', 0) or 0
        # 二刀流：有实质打击量（PA>=50）且投球 >=5 场；国联投手客串打席不算
        two_way = bool(h26 and p26 and p26.get('gamesPitched', 0) >= 5 and pa26 >= 50)
        # 以投手为主：有投球数据且打击量小（或纯投手）
        is_pitcher = p26 is not None and (h26 is None or pa26 < 50) and not two_way

        if h26 and not is_pitcher:
            ops = float(h26.get('ops') or 0)
            grid = [
                ('AVG', h26.get('avg', '—')), ('OPS', h26.get('ops', '—')),
                ('HR', str(h26.get('homeRuns', '—'))), ('RBI', str(h26.get('rbi', '—'))),
                ('SB', str(h26.get('stolenBases', '—'))), ('OBP', h26.get('obp', '—')),
                ('Age', str(age)),
                ('2025 OPS', h25.get('ops') or '—') if h25 else ('G', str(h26.get('gamesPlayed', '—'))),
            ]
            if ops >= .900: tag = '顶级火力'
            elif ops >= .800: tag = '强力'
            elif ops >= .700: tag = '稳定'
            elif ops >= .600: tag = '实用'
            else: tag = '待调整'
            tag += POS_CN.get(pos, ('', '打者'))[1]
            if two_way:
                tag = '二刀流 · ' + tag
            if h26.get('gamesPlayed', 99) < 30:
                tag += '（小样本）'
        else:
            sp = p26 or {}
            era = float(sp.get('era') or 99)
            gs = sp.get('gamesStarted', 0)
            sv = sp.get('saves', 0)
            grid = [
                ('ERA', sp.get('era', '—')), ('WHIP', sp.get('whip', '—')),
                ('K', str(sp.get('strikeOuts', '—'))), ('IP', sp.get('inningsPitched', '—')),
                ('W-L', f"{sp.get('wins', 0)}-{sp.get('losses', 0)}"),
                ('K/9', fmt1(sp.get('strikeoutsPer9Inn'))), ('BB/9', fmt1(sp.get('walksPer9Inn'))),
                ('Age', str(age)),
            ]
            if era <= 2.50: tag = '王牌'
            elif era <= 3.50: tag = '主力'
            elif era <= 4.50: tag = '轮值'
            elif era <= 6.00: tag = '起伏'
            else: tag = '待调整'
            if sv and sv >= 15:
                tag += '终结者'
            elif gs >= (sp.get('gamesPitched', 0) or 0) / 2:
                tag += '先发'
            else:
                tag += '中继'
            if sp.get('gamesPitched', 99) < 15 and not two_way:
                tag += '（小样本）'

        pos_cn, _ = POS_CN.get(pos, (pos, pos))
        number = jersey.get(name) or ''
        if not number:
            mds = [f for f in os.listdir(pdir) if f.endswith('.md')]
            if mds:
                mm = re.search(r'Dodgers\s*#([\w-]+)', io.open(os.path.join(pdir, mds[0]), encoding='utf-8').read(800))
                number = mm.group(1) if mm else '—'
        else:
            number = str(number)

        cover_names = {cover_name} | {f for f in os.listdir(pdir) if f.endswith('_report_cover.png')}
        for cn in sorted(cover_names):
            render_cover(
                name=name, number=number, pos=pos, pos_cn=pos_cn,
                grid=grid, tagline=tag, out_path=os.path.join(pdir, cn))
        ok.append((name, cover_name, tag))

    print(f'OK: {len(ok)}  SKIP: {len(skipped)}')
    for n, c, t in ok:
        print(f'  [ok] {n} -> {c} | {t}')
    for n, why in skipped:
        print(f'  [skip] {n}: {why}')


def render_cover(name, number, pos, pos_cn, grid, tagline, out_path):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')

    ax.text(0.5, 0.85, name, fontsize=32, fontweight='bold', ha='center',
            color='white', transform=ax.transAxes)
    ax.text(0.5, 0.75, f"Los Angeles Dodgers #{number} | {pos_cn} ({pos})",
            fontsize=18, ha='center', color='#4fc3f7', transform=ax.transAxes)
    ax.text(0.5, 0.65, 'SCOUTING REPORT 2026', fontsize=22, fontweight='bold',
            ha='center', color='#ff9800', transform=ax.transAxes)

    y_pos = 0.45
    for i, (label, value) in enumerate(grid[:8]):
        x_pos = 0.15 + (i % 4) * 0.23
        if i >= 4:
            y_pos = 0.25
        ax.text(x_pos, y_pos, value, fontsize=26, fontweight='bold', ha='center',
                color='#4fc3f7', transform=ax.transAxes)
        ax.text(x_pos, y_pos - 0.08, label, fontsize=12, ha='center',
                color='#90a4ae', transform=ax.transAxes)

    ax.text(0.5, 0.08, tagline, fontsize=14, ha='center', color='#90a4ae',
            transform=ax.transAxes, style='italic')
    ax.text(0.5, 0.02, f'Generated: {TODAY} | Data: MLB.com, MLB Stats API',
            fontsize=10, ha='center', color='#666', transform=ax.transAxes)

    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='#1a1a2e')
    plt.close()


if __name__ == '__main__':
    main()
