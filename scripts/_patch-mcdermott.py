# -*- coding: utf-8 -*-
"""Chayce McDermott html 赛季收官补丁"""
import io

p = r'D:\baseball\report\chayce-mcdermott\chayce-mcdermott-scouting-report.html'
t = io.open(p, encoding='utf-8').read()
n0 = len(t)

def rep(old, new, cnt=1):
    global t
    c = t.count(old)
    assert c == cnt, f'anchor count {c} != {cnt}: {old[:60]}'
    t = t.replace(old, new)

rep('Chayce McDermott 是一名在大联盟已有初体验的右投，2024 年 7 月 24 日于巴尔的摩金莺完成首秀。2025 年在金莺短暂登板表现挣扎后，2026 年转战洛杉矶道奇体系，目前于小联盟持续调整。',
    'Chayce McDermott 是一名右投 swingman，2024 年 7 月 24 日于巴尔的摩金莺完成大联盟首秀。2025 年在金莺短暂登板表现挣扎（8.2 局 ERA 15.58），2026 年转战洛杉矶道奇体系，在大联盟出赛 2 场后长住 3A Oklahoma City，季后已不在 40 人名单。')

rep('<div class="career-highlight"><h4>🔵 2026年 - 加盟道奇</h4><p>McDermott 加入道奇组织，为球队提供轮值深度。在道奇教练团体系下，他有机会重塑自己的配球策略与球路组合。</p></div>',
    '<div class="career-highlight"><h4>🔵 2026年 - 加盟道奇</h4><p>McDermott 加入道奇组织，为球队提供轮值深度。在道奇教练团体系下，他有机会重塑自己的配球策略与球路组合。</p></div>\n<div class="career-highlight"><h4>📋 2026年 - 大联盟 2 场后长住 3A</h4><p>2026 年 4 月登上大联盟后援 2 场（2.1 局、7.71 ERA、1 支被轰），此后在 Oklahoma City 度过剩余赛季，季后不在 40 人名单。</p></div>')

rep('McDermott 的 2026 年目标是在 AAA 稳定出赛，把保送率压回生涯平均水平。若能找回大学时期的控球感觉，他有机会在道奇伤病潮或轮值深度不足时获得上大联盟的机会。',
    'McDermott 的 2026 年已收官：大联盟 2 场（2.1 局、7.71 ERA）+ 3A Oklahoma City 的剩余赛季。2027 年他需要在小联盟合约中重新证明控球，任何回大联盟的路径都始于把 BB/9 压回可接受区间。')

rep('\n <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">预期发展轨迹</h3>\n <p><strong>2026 下半季：</strong>在 AAA 稳定先发，争取 100+ 局，ERA 控制在 4.50 以下。</p>\n <p><strong>2027：</strong>有机会以 sixth starter / long relief 身份进入道奇大联盟名单。</p>\n <p><strong>2028+：</strong>若控球稳定，可成为道奇轮值深度与牛棚长局数的重要选项。</p>',
    '\n <h3 style="color: #4fc3f7; margin: 20px 0 15px 0;">2026赛季实际轨迹</h3>\n <p><strong>2026：</strong>4 月大联盟 2 场后援 → 长住 3A Oklahoma City → 季后不在 40 人名单</p>\n <p><strong>2027：</strong>小联盟合约争取春训邀请，目标 AAA 100+ 局、ERA 4.50 以下</p>\n <p><strong>2028+：</strong>若控球稳定，可成为 swingman 深度；否则逐渐淡出职业体系</p>')

rep('报告生成时间：2026-07-31 | 数据截止日期：2026-07-31',
    '报告生成时间：2026-10-28 | 数据截止日期：2026-10-28（常规赛最终数据）')

io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('patched ok, len', n0, '->', len(t))
