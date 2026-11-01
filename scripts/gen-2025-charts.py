# -*- coding: utf-8 -*-
"""2025 报告图表渲染（单人手动模式）：读 charts_config.json → 出封面/评分雷达/两年对比图。
用法: python gen-2025-charts.py <slug>   （在 seasons\\2025\\players\\<slug>\\ 下读写）"""
import io, json, os, sys

sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

ROOT = r'D:\baseball\seasons\2025\players'

C_DARK = '#1a1a2e'
C_BLUE = '#4fc3f7'
C_ORANGE = '#ff9800'
C_GRAY = '#78909c'
C_GREEN = '#4caf50'


def render_cover(cfg, out):
    fig, ax = plt.subplots(figsize=(8, 10), dpi=100)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    fig.patch.set_facecolor(C_DARK)
    ax.set_facecolor(C_DARK)
    info = cfg['info']
    ax.text(0.5, 0.88, cfg['player_name'], fontsize=30, fontweight='bold', ha='center', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.80, "Los Angeles Dodgers #%s | %s (%s)" % (info['number'], info['position_cn'], info['position']),
            fontsize=16, ha='center', color=C_BLUE, transform=ax.transAxes)
    ax.text(0.5, 0.70, 'SCOUTING REPORT 2025', fontsize=22, fontweight='bold', ha='center', color=C_ORANGE, transform=ax.transAxes)
    y_pos = 0.48
    for i, (label, value) in enumerate(cfg['cover']['stats'][:8]):
        x_pos = 0.15 + (i % 4) * 0.23
        if i >= 4:
            y_pos = 0.28
        ax.text(x_pos, y_pos, str(value), fontsize=25, fontweight='bold', ha='center', color=C_BLUE, transform=ax.transAxes)
        ax.text(x_pos, y_pos - 0.075, str(label), fontsize=12, ha='center', color='#90a4ae', transform=ax.transAxes)
    ax.text(0.5, 0.10, cfg['cover']['tagline'], fontsize=14, ha='center', color='#90a4ae', style='italic', transform=ax.transAxes)
    ax.text(0.5, 0.03, 'Generated: 2026-11-01 | Data: MLB.com, MLB Stats API', fontsize=10, ha='center', color='#666', transform=ax.transAxes)
    plt.savefig(out, dpi=300, bbox_inches='tight', facecolor=C_DARK)
    plt.close()


def render_grades(cfg, out):
    g = cfg['grades']
    labels = list(g.keys())
    vals = [g[k] for k in labels]
    N = len(labels)
    ang = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    vv = vals + vals[:1]; aa = ang + ang[:1]
    fig = plt.figure(figsize=(7, 7), dpi=110)
    fig.patch.set_facecolor(C_DARK)
    ax = plt.subplot(111, polar=True)
    ax.set_facecolor(C_DARK)
    ax.plot(aa, vv, color=C_BLUE, linewidth=2)
    ax.fill(aa, vv, color=C_BLUE, alpha=0.25)
    ax.set_xticks(ang)
    ax.set_xticklabels(labels, color='#e0e0e0', fontsize=12)
    ax.set_ylim(0, 80)
    ax.set_yticks([20, 40, 60, 80])
    ax.set_yticklabels(['20', '40', '60', '80'], color='#666', fontsize=9)
    ax.grid(color='#37474f')
    ax.spines['polar'].set_color('#37474f')
    ax.set_title('%s — 2025 综合评分（20-80 标尺）' % cfg['player_name'], color='white', fontsize=14, fontweight='bold', pad=22)
    plt.tight_layout()
    plt.savefig(out, bbox_inches='tight', facecolor=C_DARK)
    plt.close()


def render_comparison(cfg, out):
    if 'comparison_p' in cfg:  # 投手版：每轴独立 low/high 归一化
        return render_comparison_pitcher(cfg, out)
    c = cfg['comparison']
    cats = c['categories']
    y24 = c['y2024']
    y25 = c['y2025']
    N = len(cats)
    ang = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    a24 = y24 + y24[:1]; a25 = y25 + y25[:1]; aa = ang + ang[:1]
    fig = plt.figure(figsize=(7.5, 7), dpi=110)
    fig.patch.set_facecolor(C_DARK)
    ax = plt.subplot(111, polar=True)
    ax.set_facecolor(C_DARK)
    ax.plot(aa, a24, color=C_GRAY, linewidth=2, label='2024')
    ax.fill(aa, a24, color=C_GRAY, alpha=0.12)
    ax.plot(aa, a25, color=C_BLUE, linewidth=2.4, label='2025')
    ax.fill(aa, a25, color=C_BLUE, alpha=0.25)
    ax.set_xticks(ang)
    ax.set_xticklabels(cats, color='#e0e0e0', fontsize=12)
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['.200', '.400', '.600', '.800', '1.000'], color='#666', fontsize=9)
    ax.grid(color='#37474f')
    ax.spines['polar'].set_color('#37474f')
    ax.legend(loc='upper right', bbox_to_anchor=(1.22, 1.1), facecolor=C_DARK, labelcolor='white')
    ax.set_title('%s — 2024 vs 2025 打击率值对比' % cfg['player_name'], color='white', fontsize=14, fontweight='bold', pad=22)
    plt.tight_layout()
    plt.savefig(out, bbox_inches='tight', facecolor=C_DARK)
    plt.close()


def render_comparison_pitcher(cfg, out):
    c = cfg['comparison_p']
    cats = c['categories']
    lo = c['low']; hi = c['high']
    y24 = c['y2024']; y25 = c['y2025']
    def norm(v, l, h): return max(0.0, min(1.0, (v - l) / (h - l)))
    n24 = [norm(v, l, h) for v, l, h in zip(y24, lo, hi)]
    n25 = [norm(v, l, h) for v, l, h in zip(y25, lo, hi)]
    N = len(cats)
    ang = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    a24 = n24 + n24[:1]; a25 = n25 + n25[:1]; aa = ang + ang[:1]
    fig = plt.figure(figsize=(7.5, 7), dpi=110)
    fig.patch.set_facecolor(C_DARK)
    ax = plt.subplot(111, polar=True)
    ax.set_facecolor(C_DARK)
    ax.plot(aa, a24, color=C_GRAY, linewidth=2, label='2024')
    ax.fill(aa, a24, color=C_GRAY, alpha=0.12)
    ax.plot(aa, a25, color=C_BLUE, linewidth=2.4, label='2025')
    ax.fill(aa, a25, color=C_BLUE, alpha=0.25)
    ax.set_xticks(ang)
    ax.set_xticklabels(cats, color='#e0e0e0', fontsize=12)
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels([], color='#666')
    ax.grid(color='#37474f')
    ax.spines['polar'].set_color('#37474f')
    ax.legend(loc='upper right', bbox_to_anchor=(1.22, 1.1), facecolor=C_DARK, labelcolor='white')
    ax.set_title('%s — 2024 vs 2025 投球对比（中心=联盟均值档）' % cfg['player_name'], color='white', fontsize=13, fontweight='bold', pad=22)
    # 每轴末端标注真实值
    for a_, v24, v25, cat in zip(ang, y24, y25, cats):
        ax.text(a_, 1.13, '%s\n24:%s 25:%s' % (cat, v24, v25), color='#90a4ae', fontsize=8.5, ha='center', va='center')
    plt.tight_layout()
    plt.savefig(out, bbox_inches='tight', facecolor=C_DARK)
    plt.close()


def main():
    slug = sys.argv[1]
    d = os.path.join(ROOT, slug)
    cfg = json.load(io.open(os.path.join(d, 'charts_config.json'), encoding='utf-8'))
    pfx = cfg['prefix']
    render_cover(cfg, os.path.join(d, '%s_report_cover.png' % pfx))
    render_grades(cfg, os.path.join(d, '%s_overall_grades.png' % pfx))
    render_comparison(cfg, os.path.join(d, '%s_season_comparison.png' % pfx))
    print('OK', slug, '->', pfx + '_report_cover.png /', pfx + '_overall_grades.png /', pfx + '_season_comparison.png')


if __name__ == '__main__':
    main()
