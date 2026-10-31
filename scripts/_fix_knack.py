# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
p = r'D:\baseball\report\landon-knack\landon-knack-scouting-report.html'
src = open(p, encoding='utf-8').read()

old = '<h4>🏥 2025-2026年 - 伤病与角色转型</h4>\n <p>2025 年出赛 10 场（7 场先发）后再次受伤；2026 年上半年基本缺阵，8 月 12 日伤愈回归后以纯牛棚身份出赛，4 场全部后援。</p>'
new = ('<h4>💪 2025年9月28日 - 见证历史的一夜</h4>\n <p>常规赛收官战，在 Clayton Kershaw 生涯最后一次常规赛登板后接替出场，'
       '后援 3.2 局送出 7 次三振（面对 13 名打者），拿下救援成功，为传奇的常规赛生涯画上句点。</p>\n </div>\n'
       ' <div class="career-highlight">\n <h4>🏥 2025-2026年 - 伤病与角色转型</h4>\n'
       ' <p>2025 年开季在大联盟名单、先发 7 场后受伤病困扰；2026 年上半年基本缺阵，8 月 12 日伤愈回归后以纯牛棚身份出赛，4 场全部后援。</p>')
assert src.count(old) == 1, src.count(old)
src = src.replace(old, new)

old2 = 'Landon Knack 1997 年 7 月 15 日出生于田纳西州 Johnson City。他就读于田纳西理工大学（Tennessee Tech），大学时期便展露出精英级的控球天赋：2019 年他在 NCAA 送出惊人的 12.0+ K/BB 比，成为选秀市场的热门名字。'
new2 = ('Landon Dakota Knack 1997 年 7 月 15 日出生于田纳西州 Johnson City。他先在 Walters State 社区学院打了两年，'
        '随后转入东田纳西州立大学（ETSU）。在 ETSU 他成为校史生涯 ERA 纪录保持者（2.60），并在 2020 年 3 月 7 日对 Wagner 的比赛中'
        '单场 16 次三振创下校史纪录——那个因疫情缩短的赛季，他投出 4 胜 0 败。')
assert src.count(old2) == 1, src.count(old2)
src = src.replace(old2, new2)

old3 = '2020 年 MLB 选秀（因疫情缩短为五轮），道奇用第二轮签选中了这位田纳西右投。'
new3 = '2020 年 MLB 选秀（因疫情缩短为五轮），道奇在第 2 轮（总第 60 顺位）选中了他。'
assert src.count(old3) == 1, src.count(old3)
src = src.replace(old3, new3)

open(p, 'w', encoding='utf-8', newline='\n').write(src)
print('OK')
