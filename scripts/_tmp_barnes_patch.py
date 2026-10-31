import io, re

path = r'D:\baseball\report\charlie-barnes\charlie-barnes-scouting-report.html'
t = io.open(path, encoding='utf-8').read()
n = [0]

def sub1(pat, rep, cnt=1, flags=0, literal=False):
    global t
    if literal:
        pat = re.escape(pat)
    t, k = re.subn(pat, rep, t, count=cnt, flags=flags)
    n[0] += k
    if k != cnt:
        print(f'WARN {k}/{cnt}: {pat[:70]}')

def seg_sub(seg_start, seg_end, pairs):
    global t
    i = t.find(seg_start)
    j = t.find(seg_end, i)
    if i < 0 or j < 0:
        print('SEG NOT FOUND:', seg_start)
        return
    seg = t[i:j]
    for label, old, new in pairs:
        pat = (r'(<td>\s*(?:<strong>\s*)?' + re.escape(label) +
               r'(?:\s*</strong>)?\s*</td>\s*<td>\s*)' + re.escape(old) + r'(\s*</td>)')
        seg, k = re.subn(pat, lambda m: m.group(1) + new + m.group(2), seg, count=1)
        if k != 1:
            print(f'  WARN seg [{label}] {old}->{new}: {k}')
    t = t[:i] + seg + t[j:]

# 1) 副标题 + 状态行
sub1('Minors（目前下放小联盟，2026 年曾短暂升上大联盟）',
     '已离队（8/18 后长住 3A，季后离开道奇组织）', cnt=2, literal=True)

# 2) 球探总评段落
sub1('2026 年他在 3 场后援出赛中投出 7.00 ERA，样本极小且表现挣扎，目前已被下放至小联盟继续调整。',
     '2026 年他整季 4 场后援出赛、10.0 局，缴出 6.30 ERA、1.70 WHIP、5 三振 4 保送，样本极小且仍挣扎；8 月 18 日后长住 3A Oklahoma City，季后已离开道奇组织。',
     literal=True)

# 3) 2026 赛季统计表
seg_sub('📊 2026赛季投球数据', '近年大联盟数据趋势', [
    ('出赛 (G)', '3', '4'),
    ('自责分率 (ERA)', '7.00', '6.30'),
    ('投球局数 (IP)', '9.0', '10.0'),
    ('三振 (K)', '3', '5'),
    ('保送 (BB)', '3', '4'),
    ('WHIP', '1.78', '1.70'),
    ('K/9', '3.00', '4.50'),
    ('BB/9', '3.00', '3.60'),
    ('K/BB', '1.00', '1.25'),
    ('HR/9', '3.00', '2.70'),
])

# 4) 生涯数据表
seg_sub('大联盟生涯数据', '⚾ 投球武器库', [
    ('出赛 (G)', '12', '13'),
    ('自责分率 (ERA)', '6.18', '6.00'),
    ('投球局数 (IP)', '47.0', '48.0'),
    ('三振 (K)', '23', '25'),
    ('保送 (BB)', '19', '20'),
    ('WHIP', '1.66', '1.65'),
    ('K/9', '4.40', '4.69'),
    ('BB/9', '3.64', '3.75'),
    ('K/BB', '1.21', '1.25'),
    ('HR/9', '1.34', '1.31'),
])

# 5) 趋势表 2026 行整行替换
new_row = '''<td>
 2026
 </td>
 <td>
 LAD
 </td>
 <td>
 4
 </td>
 <td>
 0
 </td>
 <td>
 0-1
 </td>
 <td>
 6.30
 </td>
 <td>
 10.0
 </td>
 <td>
 5
 </td>
 <td>
 4
 </td>
 <td>
 1.70
 </td>
 <td>
 4.50
 </td>
 <td>
 3.60
 </td>'''
sub1(r'<td>\s*2026\s*</td>\s*<td>\s*LAD\s*</td>\s*<td>\s*3\s*</td>\s*<td>\s*0\s*</td>\s*<td>\s*0-1\s*</td>\s*<td>\s*7\.00\s*</td>\s*<td>\s*9\.0\s*</td>\s*<td>\s*3\s*</td>\s*<td>\s*3\s*</td>\s*<td>\s*1\.78\s*</td>\s*<td>\s*3\.00\s*</td>\s*<td>\s*3\.00\s*</td>',
     new_row, flags=re.S)

# 6) 注释
sub1('注：2026 年仅 3 场、9 局的大联盟样本，数据波动极大，不宜过度解读。',
     '注：2026 年仅 4 场、10 局的大联盟样本，数据波动极大，不宜过度解读。', literal=True)

# 7) 未来展望 2026 段
sub1(r'<p>\s*2026 年剩余赛季\s*</p>\s*<ul>\s*<li>\s*首要目标\s*：在小联盟重建信心与状态，争取再次获得大联盟机会\s*</li>\s*<li>\s*角色预期\s*：AAA Oklahoma City 的 先发轮值 或 long relief 角色\s*</li>\s*<li>\s*ERA 目标\s*：若再次升上大联盟，目标 ERA 在 5\.00 以下即算合格 depth\s*</li>\s*<li>\s*风险点\s*：持续被击出长打可能让他在赛季末被释出\s*</li>\s*</ul>',
     '''<p>
 2026 实际轨迹
</p>
<ul>
<li>
 7 月两次、8 月一次进出大联盟（三度入选名单又三度 DFA），8 月 18 日后长住 3A
</li>
<li>
 大联盟合计 4 场、10.0 局、6.30 ERA、1.70 WHIP——长打问题未解（3 支本垒打）
</li>
<li>
 季后已离开道奇组织，成为自由球员
</li>
</ul>''', flags=re.S)

# 8) 背景故事 道奇时期
sub1('因伤病潮获得短暂大联盟机会，3 场后援出赛 7.00 ERA',
     '因伤病潮获得三次短暂大联盟机会，4 场后援出赛 6.30 ERA', literal=True)
sub1('目前下放至小联盟，继续寻找重返大联盟的机会', '8 月 18 日后长住 3A，季后离开道奇组织', literal=True)

# 9) 里程碑
sub1(r'生涯大联盟出赛\s*：12 场，上升空间有限', '生涯大联盟出赛：13 场，上升空间有限')
sub1(r'生涯三振\s*：23 次，突破 50 次需要更多 MLB 机会', '生涯三振：25 次，突破 50 次需要更多 MLB 机会')

# 10) 页脚日期
sub1('报告生成时间：2026-07-31 | 数据截止日期：2026-07-31',
     '报告生成时间：2026-10-27 | 数据截止日期：2026-10-27（常规赛最终数据）', literal=True)

io.open(path, 'w', encoding='utf-8').write(t)
print('total replacements:', n[0])
