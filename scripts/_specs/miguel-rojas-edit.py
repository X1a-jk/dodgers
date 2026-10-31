#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Editorial updates + PS section for Miguel Rojas."""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8")

path = r"D:\baseball\report\miguel-rojas\miguel-rojas-scouting-report.html"
t = io.open(path, encoding="utf-8").read()

reps = [
    ("37岁老将的打击率从 .262 提升至 .290，OPS 从 .715 提升至 .755。这显示他依然能保持良好的接触能力和选球。虽然长打有限，但他的打击足以让他在阵容中占据位置。",
     "37岁老将全季缴出.267打击率、.703 OPS，较2025年（.262/.715）基本持平，107场出赛显示他仍保持良好的接触能力和健康的身体状态。虽然长打有限，但他的打击足以让他在阵容中占据位置。此外他本赛季还有4次登板救火（13.50 ERA、0三振），是球队锁定胜局时的欢乐担当。"),
    ("37岁仍保持 .290 打击率", "37岁仍保持 .267 打击率"),
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
 <tr><th>G</th><th>PA</th><th>AVG</th><th>OBP</th><th>SLG</th><th>OPS</th><th>BB</th><th>SO</th></tr>
 </thead>
 <tbody>
 <tr>
 <td>4</td><td>7</td><td>.333</td><td>.429</td><td>.500</td><td class="highlight">1.262</td><td>1</td><td>2</td>
 </tr>
 </tbody>
 </table>
 <ul style="margin-left: 20px; line-height: 2; margin-top: 15px;">
 <li>季后赛以替补身份出赛4场，7打席2安打，.333/.429/.500 的效率极高，是轮换阵容中的稳定替补</li>
 <li>样本极小，但其选球和守备价值在季后赛继续体现</li>
 </ul>
 </div>
'''
anchor = ' <div class="section">\n <h2>🔮 未来展望</h2>'
assert anchor in t, "anchor missing"
t = t.replace(anchor, PS + anchor, 1)

io.open(path, "w", encoding="utf-8").write(t)
print("editorial done: miguel-rojas")
