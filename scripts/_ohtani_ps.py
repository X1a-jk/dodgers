# -*- coding: utf-8 -*-
"""给大谷 HTML 插入 2026 季后赛表现章节"""
import io

path = r'D:\baseball\report\shohei-ohtani\shohei-ohtani-scouting-report.html'
t = io.open(path, encoding='utf-8').read()

anchor = '<div class="section">\n <h2>🔮 未来展望</h2>'
assert t.count(anchor) == 1, 'anchor count %d' % t.count(anchor)

ps_section = '''<div class="section">
 <h2>🏆 2026 季后赛表现</h2>
 <p style="margin-bottom: 15px;">道奇 2026 季后赛战绩：NLDS 3-1 晋级、NLCS 0-4 止步。大谷 8 场全勤担任指定打击，未登板投球（球队彻底保护其手臂）。</p>
 <table class="comparison-table">
 <thead>
 <tr><th>G</th><th>PA</th><th>AVG</th><th>OBP</th><th>SLG</th><th>OPS</th><th>HR</th><th>RBI</th><th>SB</th><th>BB</th><th>SO</th></tr>
 </thead>
 <tbody>
 <tr>
 <td>8</td><td>32</td><td>.192</td><td>.323</td><td>.308</td><td class="highlight">.631</td><td>1</td><td>3</td><td>1</td><td>4</td><td>10</td>
 </tr>
 </tbody>
 </table>
 <ul style="margin-left: 20px; line-height: 2; margin-top: 15px;">
 <li>季后赛缴出.192/.323/.308、OPS .631，选球手感仍在（4保送、.323上垒率）但长打完全熄火：26打数仅5安打、10三振，长打率从常规赛的.512暴跌至.308</li>
 <li>8场仅1轰3打点，与常规赛30轰81打点的联盟顶级火力形成巨大反差，是道奇打线在 NLCS 被横扫的关键因素之一</li>
 <li>对比2025年季后赛11轰、NLCS MVP 的史诗表现，今年季后赛是他道奇生涯首次真正意义上的季后赛低迷</li>
 </ul>
 </div>

'''

t = t.replace(anchor, ps_section + anchor)
io.open(path, 'w', encoding='utf-8', newline='').write(t)
print('inserted, new LEN', len(t))
