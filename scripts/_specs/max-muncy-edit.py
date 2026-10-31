#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Editorial prose updates + PS section for Max Muncy."""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8")

path = r"D:\baseball\report\max-muncy\max-muncy-scouting-report.html"
t = io.open(path, encoding="utf-8").read()

reps = [
    ("2026年他的打击率提升至.259，显示他正在做出更稳定的contact调整。",
     "2026年全年他的打击率停在.252，contact 稳定性较生涯早期已有明显改善。"),
    ("2026年保送率11.9%，上垒率.354",
     "2026年保送率11.6%（65次保送），上垒率.348"),
    ("2025年100场和2026年89场的出勤率显示他仍可靠",
     "2025年100场、2026年149场的出勤率显示他仍可靠"),
    ("精英级别的力量输出，17轰展现持续power",
     "精英级别的力量输出，29轰76打点展现持续power"),
    ("2026（下半季）：维持.250/.350/.480，全季约25-28轰",
     "2026：.252/.348/.490、29轰76打点，火力输出符合核心打者预期"),
    ("2027：可能转为1B/DH为主，OPS仍保持.800+",
     "2027：可能转为1B/DH为主，OPS仍保持.800+水准"),
]
for old, new in reps:
    if old not in t:
        print("  MISS:", old[:30])
    t = t.replace(old, new, 1)

PS = '''
 <div class="section">
 <h2>🏆 2026 季后赛表现</h2>
 <p style="margin-bottom: 15px;">道奇 2026 季后赛战绩：NLDS 3-1 晋级、NLCS 0-4 止步。</p>
 <table class="comparison-table">
 <thead>
 <tr><th>G</th><th>PA</th><th>AVG</th><th>OBP</th><th>SLG</th><th>OPS</th><th>HR</th><th>RBI</th><th>BB</th><th>SO</th></tr>
 </thead>
 <tbody>
 <tr>
 <td>8</td><td>24</td><td>.208</td><td>.208</td><td>.583</td><td class="highlight">.999</td><td>3</td><td>3</td><td>0</td><td>8</td>
 </tr>
 </tbody>
 </table>
 <ul style="margin-left: 20px; line-height: 2; margin-top: 15px;">
 <li>季后赛3支全垒打为全队最多，.583长打率展现elite power，是道奇季后赛最可靠的长打来源</li>
 <li>但24打席8次三振、0保送，「三真」属性在季后赛被放大，整体打击率仅.208</li>
 </ul>
 </div>
'''
anchor = ' <div class="section">\n <h2>🔮 未来展望</h2>'
assert anchor in t, "anchor missing"
t = t.replace(anchor, PS + anchor, 1)

io.open(path, "w", encoding="utf-8").write(t)
print("editorial done: max-muncy")
