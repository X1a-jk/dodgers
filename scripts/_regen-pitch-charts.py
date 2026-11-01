# -*- coding: utf-8 -*-
"""按 API 数据重生成 pitch_velocities.png（均速+占比条形图），替换旧的纯手工区间图。
只处理 HTML 里实际引用了该图的球员；图注文案同步更新。"""
import io, json, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 中文字体：Windows 自带微软雅黑
CN_FONT = None
for cand in ['Microsoft YaHei', 'SimHei', 'DengXian']:
    try:
        font_manager.findfont(cand, fallback_to_default=False)
        CN_FONT = cand
        break
    except Exception:
        continue
if CN_FONT:
    plt.rcParams['font.family'] = CN_FONT
plt.rcParams['axes.unicode_minus'] = False
print('中文字体:', CN_FONT or '无（英文标注）')

AUDIT = json.load(io.open(r'D:\baseball\data\_arsenal_audit.json', encoding='utf-8'))
EDITIONS = [
    r'D:\baseball\seasons\2026\players',
    r'D:\baseball\seasons\2026\players-regular',
    r'D:\baseball\seasons\2026\players-postseason',
]
OLD_CAPTION = '上图为各球种球速区间（蓝=最低球速，橙=最高球速，红线=平均值）。球速差与位移差越大，打者越难锁定单一球路。'
NEW_CAPTION = '上图为各球种均速与配球占比（数据来源：MLB Stats API pitchArsenal，2026 赛季）。'


def make_chart(truth, season, out_path):
    sig = [t for t in truth if t['pct'] >= 2.0][:6]
    sig = sorted(sig, key=lambda x: x['avgSpeed'])
    names = [('%s' % t['cn']) if CN_FONT else t['desc'] for t in sig]
    speeds = [t['avgSpeed'] for t in sig]
    pcts = [t['pct'] for t in sig]
    colors = plt.cm.Blues([0.45 + 0.5 * i / max(1, len(sig) - 1) for i in range(len(sig))])

    fig, ax = plt.subplots(figsize=(9, 0.9 * len(sig) + 1.6), dpi=110)
    fig.patch.set_facecolor('#0d2137')
    ax.set_facecolor('#0d2137')
    bars = ax.barh(names, speeds, color=colors, edgecolor='#4fc3f7', height=0.62)
    for b, sp, pc in zip(bars, speeds, pcts):
        ax.text(b.get_width() + 0.3, b.get_y() + b.get_height() / 2,
                '%.1f mph · 占比 %.1f%%' % (sp, pc), va='center', color='#e2e8f0', fontsize=11)
    ax.set_xlim(0, max(speeds) * 1.28)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors='#90a4ae', labelsize=12)
    ax.set_xlabel('平均球速 (mph)', color='#90a4ae', fontsize=11)
    title = 'Pitch Arsenal — Avg Velocity & Usage (%d)' % season
    ax.set_title(title, color='white', fontsize=14, fontweight='bold', pad=14)
    plt.tight_layout()
    fig.savefig(out_path, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    done = []
    for slug, a in AUDIT.items():
        if not a['truth']:
            continue
        for root in EDITIONS:
            d = os.path.join(root, slug)
            if not os.path.isdir(d):
                continue
            f = [x for x in os.listdir(d) if x.endswith('-scouting-report.html')]
            if not f:
                continue
            p = os.path.join(d, f[0])
            html = io.open(p, encoding='utf-8').read()
            m = re.search(r'src="([^"]*pitch_velocities\.png)"', html)
            if not m:
                continue
            chart = os.path.join(d, m.group(1))
            make_chart(a['truth'], a['season'], chart)
            if OLD_CAPTION in html:
                html = html.replace(OLD_CAPTION, NEW_CAPTION)
                io.open(p, 'w', encoding='utf-8', newline='').write(html)
            done.append('%s [%s]' % (slug, os.path.basename(root)))
    print('重生成 %d 张图:' % len(done))
    for x in done:
        print(' ', x)


if __name__ == '__main__':
    main()
