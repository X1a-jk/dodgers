import io

path = r'D:\baseball\report\wyatt-mills\wyatt-mills-scouting-report.html'
t = io.open(path, encoding='utf-8').read()

def oldc(*lines):
    return '\n'.join(lines)

subs = [
  ('Los Angeles Dodgers #58 | 右投后援 (RHP) | Minors',
   'Los Angeles Dodgers #58 | 右投后援 (RHP) | 已离队（8/6 被国民让渡捡走、9/17 被释出）'),
  (oldc('<td>', ' 状态', ' </td>', '<td>', ' Minors', ' </td>'),
   oldc('<td>', ' 状态', ' </td>', '<td>', ' 已离队（8/6 被国民捡走、9/17 被释出）', ' </td>')),
  ('2026 年在道奇的 4.1 局小样本中，ERA 6.23、WHIP 2.31，显示出控球问题仍需改善。',
   '2026 年在道奇的 6.1 局小样本中，ERA 5.68、WHIP 2.21，送出 9 次保送——控球问题不仅未改善，反而成了他离队的主因。'),
  ('31 岁的 Mills 已经进入生涯后期，他的价值在于经验、低肩角度与能吃局数。若能在道奇牛棚中找到定位，他可以作为 situational reliever 或 吃局数投手 提供深度。',
   '31 岁的 Mills 已经进入生涯后期，他的价值在于经验、低肩角度与能吃局数。8 月 3 日道奇将他 DFA，国民队 8 月 6 日捡走他但只让他待在小联盟，9 月 17 日直接释出——他的 2026 以失业收场。'),
  ('2026 年 Mills 加入道奇组织，为牛棚提供 veteran depth。虽然年龄与球速限制了他的 天花板，但他的经验与独特角度仍具价值。',
   '2026 年 Mills 以非名单邀请加盟道奇春训，5 月 10 日入选名单，6 场后援 5.68 ERA 但 BB/9 高达 13.28；8 月 3 日 DFA 后被国民捡走，9 月 17 日被释出。'),
  (oldc('<span class="stat-value">', ' 5', ' </span>', '<div class="stat-label">', ' 出赛', ' </div>'),
   oldc('<span class="stat-value">', ' 6', ' </span>', '<div class="stat-label">', ' 出赛', ' </div>')),
  (oldc('<span class="stat-value">', ' 6.23', ' </span>', '<div class="stat-label">', ' ERA', ' </div>'),
   oldc('<span class="stat-value">', ' 5.68', ' </span>', '<div class="stat-label">', ' ERA', ' </div>')),
  (oldc('<span class="stat-value">', ' 4.1', ' </span>', '<div class="stat-label">', ' IP', ' </div>'),
   oldc('<span class="stat-value">', ' 6.1', ' </span>', '<div class="stat-label">', ' IP', ' </div>')),
  (oldc('<span class="stat-value">', ' 4', ' </span>', '<div class="stat-label">', ' K', ' </div>'),
   oldc('<span class="stat-value">', ' 5', ' </span>', '<div class="stat-label">', ' K', ' </div>')),
  (oldc('<span class="stat-value">', ' 7', ' </span>', '<div class="stat-label">', ' BB', ' </div>'),
   oldc('<span class="stat-value">', ' 9', ' </span>', '<div class="stat-label">', ' BB', ' </div>')),
  (oldc('<span class="stat-value">', ' 2.31', ' </span>', '<div class="stat-label">', ' WHIP', ' </div>'),
   oldc('<span class="stat-value">', ' 2.21', ' </span>', '<div class="stat-label">', ' WHIP', ' </div>')),
  (oldc('<span class="stat-value">', ' 8.31', ' </span>', '<div class="stat-label">', ' K/9', ' </div>'),
   oldc('<span class="stat-value">', ' 7.38', ' </span>', '<div class="stat-label">', ' K/9', ' </div>')),
  (oldc('<span class="stat-value">', ' 14.54', ' </span>', '<div class="stat-label">', ' BB/9', ' </div>'),
   oldc('<span class="stat-value">', ' 13.28', ' </span>', '<div class="stat-label">', ' BB/9', ' </div>')),
  (oldc('<td>', ' 2026', ' </td>', '<td>', ' 5', ' </td>', '<td>', ' 0', ' </td>', '<td>', ' 0-0', ' </td>',
        '<td>', ' 6.23', ' </td>', '<td>', ' 4.1', ' </td>', '<td>', ' 4', ' </td>', '<td>', ' 7', ' </td>',
        '<td>', ' 2.31', ' </td>', '<td>', ' 8.31', ' </td>'),
   oldc('<td>', ' 2026', ' </td>', '<td>', ' 6', ' </td>', '<td>', ' 0', ' </td>', '<td>', ' 0-0', ' </td>',
        '<td>', ' 5.68', ' </td>', '<td>', ' 6.1', ' </td>', '<td>', ' 5', ' </td>', '<td>', ' 9', ' </td>',
        '<td>', ' 2.21', ' </td>', '<td>', ' 7.38', ' </td>')),
  ('4.1 局送出 7 次保送，BB/9 高达 14.54，这是不可接受的。无论角度多刁钻，无法把球投进好球带都会让自己和球队陷入被动。Mills 必须立即改善控球，否则很快会被取代。',
   '6.1 局送出 9 次保送，BB/9 高达 13.28，这是不可接受的。无论角度多刁钻，无法把球投进好球带都会让自己和球队陷入被动。Mills 没能改善控球——道奇 8 月 3 日将他 DFA，问题的答案已经写下。'),
  ('2026 下半季：\n 若控球改善，可能偶尔被征召上大联盟；否则继续在 AAA 担任 veteran depth。',
   '2026 实际轨迹：\n 6 场 5.68 ERA、BB/9 13.28 后于 8/3 DFA；8/6 被国民捡走但长住 3A Rochester；9/17 被释出，赛季以失业收场。'),
  ('2027：\n 若无法稳定贡献，可能转战独立联盟或海外联赛。',
   '2027：\n 需以小联盟合约重新出发，若开季找不到球队，可能转战独立联盟或海外联赛。'),
  ('2026 年加盟道奇后，Mills 希望在这座冠军球队中重新证明自己。他的经验和独特角度是资产，但年龄与控球问题也让他的未来充满不确定性。',
   '2026 年加盟道奇后，Mills 确实重新站上了大联盟——6 场登板、9 次保送、一场 DFA、一次让渡捡走、一次释出。他的经验和独特角度没能抵消失控的控球，31 岁的他在 9 月 17 日提前收到了冬天的通知。'),
  ('报告生成时间：2026-07-31 | 数据截止日期：2026-07-31',
   '报告生成时间：2026-10-27 | 数据截止日期：2026-10-27（常规赛最终数据）'),
]

ok = 0
for old, new in subs:
    if old in t:
        t = t.replace(old, new, 1)
        ok += 1
    else:
        print('MISS:', old[:60].replace('\n', ' '))
io.open(path, 'w', encoding='utf-8').write(t)
print(f'{ok}/{len(subs)} applied')
