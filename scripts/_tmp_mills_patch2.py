import io, re
path = r'D:\baseball\report\wyatt-mills\wyatt-mills-scouting-report.html'
t = io.open(path, encoding='utf-8').read()

def card(label, old, new):
    global t
    anchor = 'stat-label">' + label + '</div>'
    i = t.find(anchor)
    if i < 0:
        print('anchor MISS', label)
        return
    seg_start = t.rfind('<div class="stat-card">', 0, i)
    seg = t[seg_start:i]
    seg2, k = re.subn(r'(stat-value"[^>]*>)' + re.escape(old) + r'(</span>)',
                      lambda m: m.group(1) + new + m.group(2), seg, count=1)
    if k != 1:
        print('WARN card', label, old, '->', new)
    t = t[:seg_start] + seg2 + t[i:]

card('出赛', '5', '6')
card('ERA', '6.23', '5.68')
card('IP', '4.1', '6.1')
card('K', '4', '5')
card('BB', '7', '9')
card('WHIP', '2.31', '2.21')
card('K/9', '8.31', '7.38')
card('BB/9', '14.54', '13.28')

anchor = 'stat-label">状态</div>'
i = t.find(anchor)
seg_start = t.rfind('<td>', 0, i)
seg = t[seg_start:i]
seg2, k = re.subn(r'(<td>\s*)Minors(\s*</td>)',
                  lambda m: m.group(1) + '已离队（8/6 被国民捡走、9/17 被释出）' + m.group(2), seg, count=1)
print('status:', k)
t = t[:seg_start] + seg2 + t[i:]

old_row = '<td>2026</td>\n <td>5</td>\n <td>0</td>\n <td>0-0</td>\n <td>6.23</td>\n <td>4.1</td>\n <td>4</td>\n <td>7</td>\n <td>2.31</td>\n <td>8.31</td>'
new_row = '<td>2026</td>\n <td>6</td>\n <td>0</td>\n <td>0-0</td>\n <td>5.68</td>\n <td>6.1</td>\n <td>5</td>\n <td>9</td>\n <td>2.21</td>\n <td>7.38</td>'
if old_row in t:
    t = t.replace(old_row, new_row, 1)
    print('row ok')
else:
    print('row MISS')

pairs = [
 ('<p><strong>2026 下半季：</strong>若控球改善，可能偶尔被征召上大联盟；否则继续在 AAA 担任 veteran depth。</p>',
  '<p><strong>2026 实际轨迹：</strong>6 场 5.68 ERA、BB/9 13.28 后于 8/3 DFA；8/6 被国民捡走但长住 3A Rochester；9/17 被释出，赛季以失业收场。</p>'),
 ('<p><strong>2027：</strong>若无法稳定贡献，可能转战独立联盟或海外联赛。</p>',
  '<p><strong>2027：</strong>需以小联盟合约重新出发，若开季找不到球队，可能转战独立联盟或海外联赛。</p>'),
]
for o, n in pairs:
    if o in t:
        t = t.replace(o, n, 1)
        print('ok:', o[:20])
    else:
        print('MISS:', o[:30])

io.open(path, 'w', encoding='utf-8').write(t)
print('done')
