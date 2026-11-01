# -*- coding: utf-8 -*-
"""按 API 真实数据重写全部投球武器库（统一 NEW 格式），处理 players/ players-regular/ players-postseason 三个批次。
- 有 API 数据：整段按真实球种重写（均速+配球占比+数据驱动中文描述，评分按使用率映射）
- 无 API 数据（Stone/Graterol/Cousins，2025-26 无登板）：保留原内容转 NEW 格式 + 无数据注记
"""
import io, json, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
AUDIT = json.load(io.open(r'D:\baseball\data\_arsenal_audit.json', encoding='utf-8'))
EDITIONS = [
    (r'D:\baseball\seasons\2026\players', '总结版'),
    (r'D:\baseball\seasons\2026\players-regular', '常规赛版'),
    (r'D:\baseball\seasons\2026\players-postseason', '季后赛版'),
]
NOTE_NO_DATA = '⚠️ 该球员 2025-26 两个赛季均无 MLB 登板记录，以下为伤前配球参考，球速与使用率为历史资料。'

EN_NAME = {
    'FF': 'Four-Seam Fastball', 'SI': 'Sinker', 'FC': 'Cutter', 'SL': 'Slider',
    'ST': 'Sweeper', 'CU': 'Curveball', 'KC': 'Knuckle Curve', 'CH': 'Changeup',
    'FS': 'Splitter', 'FO': 'Forkball', 'SV': 'Screwball', 'KN': 'Knuckleball',
}
FAMILY_BLURB = {
    'FF': '直上直下的四缝线速球，负责抢好球数与建立球数领先，是所有配球的基准。',
    'SI': '伸卡球下沉明显，主要用于制造滚地球、压低长打率。',
    'FC': '卡特球介于速球与滑球之间，球尾小幅横移，用于破坏打者节奏与制造软弱击球。',
    'SL': '传统滑球横向位移锐利，是两好球后的主要挥空武器。',
    'ST': '横扫滑球比传统滑球横向位移更大，球路横扫进垒，对同侧打者威胁极大。',
    'CU': '曲球落差大，用于改变打者视线高度与击球节奏。',
    'KC': '指关节型曲球（Knuckle Curve），锐利下坠，常作为两好球后的追杀武器。',
    'CH': '变速球靠与速球的速差取命，主要用来对付反侧打者。',
    'FS': '快速指叉球下坠时机晚，与速球搭配形成致命速差。',
    'FO': '指叉球下坠幅度大，是主要的出局球之一。',
    'SV': '螺旋球反旋转内旋，极稀有球种，主要用来干扰同侧打者。',
    'KN': '蝴蝶球几乎不旋转，轨迹飘忽，连捕手都难以捉摸。',
}


def grade_of(pct):
    if pct >= 40: return 'A'
    if pct >= 25: return 'A-'
    if pct >= 15: return 'B+'
    if pct >= 8: return 'B'
    if pct >= 4: return 'B-'
    if pct >= 2: return 'C+'
    return 'C'


def gcls(g):
    return g.replace('+', 'plus').replace('-', 'minus').lower()


def lead_of(pct):
    if pct >= 35: return '主战球种'
    if pct >= 15: return '常用武器'
    if pct >= 5: return '辅助配球'
    return '偶尔使用'


def build_from_truth(slug, name, season, truth):
    sig = [t for t in truth if t['pct'] >= 2.0][:6]
    note = ''
    if season == 2025:
        note = '<p style="color:#ff9800;font-size:0.85rem;margin-bottom:12px;">📌 该球员 2026 赛季无 MLB 登板记录，以下基于 2025 赛季数据。</p>'
    cards = []
    for t in sig:
        code = t['code']
        desc = '%s，占全部配球的 %.1f%%，均速 %.1f mph。%s' % (
            lead_of(t['pct']), t['pct'], t['avgSpeed'], FAMILY_BLURB.get(code, ''))
        g = grade_of(t['pct'])
        cards.append('''<div class="pitch-card">
<h3>%s (%s) <span class="grade grade-%s">%s</span></h3>
<div class="velocity">均速 %.1f mph · 配球占比 %.1f%%</div>
<p style="margin-top: 10px; color: #b0bec5;">%s</p>
</div>''' % (t['cn'], EN_NAME.get(code, code), gcls(g), g, t['avgSpeed'], t['pct'], desc))
    return note + '\n'.join(cards)


def reformat_legacy(slug, current):
    """无 API 数据：旧内容转 NEW 格式。"""
    cards = []
    for c in current:
        h3 = c['name']
        g = c['grade'] if c['grade'] and c['grade'] != '?' else 'B-'
        gm = re.search(r'class="grade[^"]*"', g)
        vel = c['vel']
        cards.append('''<div class="pitch-card">
<h3>%s <span class="grade grade-%s">%s</span></h3>
<div class="velocity">%s</div>
<p style="margin-top: 10px; color: #b0bec5;">%s</p>
</div>''' % (h3, gcls(g), g, vel, '近年配球参考（详见上方说明）。'))
    return '<p style="color:#ff9800;font-size:0.85rem;margin-bottom:12px;">%s</p>' % NOTE_NO_DATA + '\n'.join(cards)


def replace_section(html, new_inner, slug, fname):
    # 变体A（标准/带图）：<h2>武器库</h2> [可含 pitch_velocities 图块] <div class="pitch-arsenal"> ... 下一个 section 前
    m = re.search(r'(?s)(<h2>\s*.{0,6}?投球武器库\s*</h2>.*?)<div class="pitch-arsenal">(.*?)(?=\s*<div class="section">)', html)
    if m:
        replacement = m.group(1) + '<div class="pitch-arsenal">\n' + new_inner + '\n</div>\n</div>\n'
        return html[:m.start()] + replacement + html[m.end():], True
    # 变体B（无 pitch-arsenal 容器，裸 h3+ul）：整段替换为规范结构
    m = re.search(r'(?s)(<h2>\s*.{0,6}?投球武器库\s*</h2>)(.*?)(?=\s*<div class="section">|\s*<footer|\s*<div class="back)', html)
    if m:
        replacement = m.group(1) + '\n<div class="pitch-arsenal">\n' + new_inner + '\n</div>\n</div>\n'
        return html[:m.start()] + replacement + html[m.end():], True
    return html, False


def main():
    summary = []
    for slug, a in sorted(AUDIT.items()):
        if a['truth']:
            inner = build_from_truth(slug, a['name'], a['season'], a['truth'])
            kind = 'API(%s)' % a['season']
        else:
            if not a['current']:
                summary.append((slug, 'SKIP 无API也无现有内容'))
                continue
            inner = reformat_legacy(slug, a['current'])
            kind = 'LEGACY格式修正'
        hits = []
        for root, label in EDITIONS:
            d = os.path.join(root, slug)
            if not os.path.isdir(d):
                continue
            f = [x for x in os.listdir(d) if x.endswith('-scouting-report.html')]
            if not f:
                continue
            p = os.path.join(d, f[0])
            html = io.open(p, encoding='utf-8').read()
            out, ok = replace_section(html, inner, slug, f[0])
            if not ok:
                hits.append(label + ':锚点缺失')
                continue
            n_cards = len(re.findall(r'class="pitch-card"', out))
            assert n_cards >= 1, '%s %s 卡片数为 0' % (slug, label)
            io.open(p, 'w', encoding='utf-8', newline='').write(out)
            hits.append('%s:OK(%d卡)' % (label, n_cards))
        summary.append((slug, kind + ' | ' + ' '.join(hits)))
    for s, k in summary:
        print('%-26s %s' % (s, k))


if __name__ == '__main__':
    main()
