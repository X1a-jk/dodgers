#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
path = r"D:\baseball\report\andy-pages\andy-pages-scouting-report.html"
t = io.open(path, encoding="utf-8").read()

repl = [
("2026年，他的OPS进一步提升至.807，上垒率从.313提升至.336，显示plate discipline持续进步。",
 "2026年，他的OPS进一步提升至.811，上垒率从.313提升至.343，显示plate discipline持续进步。"),
("<p>.270 AVG | .336 OBP | .471 SLG | .807 OPS | 17 HR | 66 RBI</p>",
 "<p>.274 AVG | .343 OBP | .468 SLG | .811 OPS | 23 HR | 85 RBI</p>"),
("保送率从4.6%提升至8.3%。",
 "保送率从4.6%提升至8.5%。"),
("2025年他仅有29次保送，但2026年已经34次，且出赛场次还更少。如果他继续改善击球区纪律，上垒率有望突破.350。",
 "2025年他仅有29次保送，但2026年已经49次，且出赛场次还更少（134场）。上垒率升至.343，如果他继续改善击球区纪律，有望突破.350。"),
("他的三振率仍偏高（19.5%）",
 "他的三振率仍偏高（19.7%）"),
("<li>2026年盗垒次数较2025年下降</li>",
 "<li>2026年盗垒13次仅比2025年少1次，且成功率降至.650</li>"),
("<p><strong>2026（下半季）：</strong>OPS有望维持在.800+，全季约25轰、12盗</p>",
 "<p><strong>2026（最终）：</strong>OPS .811达成.800+目标，全季23轰、13盗，出赛134场；但盗垒成功率仅.650，效率待提升</p>"),
]

for old, new in repl:
    n = t.count(old)
    if n != 1:
        print("WARN count=%d: %s" % (n, old[:50]))
    t = t.replace(old, new)

anchor = '<div class="section">\n <h2>🔮 未来展望</h2>'
assert t.count(anchor) == 1, "anchor not found: %d" % t.count(anchor)
ps = '''
 <div class="section">
 <h2>🏆 2026 季后赛表现</h2>
 <p style="margin-bottom: 15px;">道奇 2026 季后赛战绩：NLDS 3-1 晋级、NLCS 0-4 止步。</p>
 <table class="comparison-table">
 <thead>
 <tr><th>G</th><th>PA</th><th>AVG</th><th>OBP</th><th>SLG</th><th>OPS</th><th>HR</th><th>RBI</th><th>BB</th><th>SO</th></tr>
 </thead>
 <tbody>
 <tr>
 <td>8</td>
 <td>28</td>
 <td>.269</td>
 <td>.321</td>
 <td>.308</td>
 <td class="highlight">.629</td>
 <td>0</td>
 <td>4</td>
 <td>2</td>
 <td>9</td>
 </tr>
 </tbody>
 </table>
 <ul style="margin-left: 20px; line-height: 2; margin-top: 15px;">
 <li>8场出赛、28打席，敲出7支安打，贡献4分打点，但全垒挂零，长打率仅.308</li>
 <li>9次三振对2次保送，被三振率32.1%明显高于常规赛水准，NLCS 0-4期间适应不佳</li>
 <li>样本较小（28打席），.269打击率尚可，但整体攻击表现低于常规赛的.811 OPS</li>
 </ul>
 </div>

'''
t = t.replace(anchor, ps + anchor)
io.open(path, "w", encoding="utf-8").write(t)
print("prose updated")
