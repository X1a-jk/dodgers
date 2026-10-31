# -*- coding: utf-8 -*-
"""Charlie Barnes: 评分区转 stat-card 格式 + 补封面/对比图引用，供雷达脚本解析"""
import io, re

p = r'D:\baseball\report\charlie-barnes\charlie-barnes-scouting-report.html'
t = io.open(p, encoding='utf-8').read()

# 1. 封面图：header 结束后插入
anchor = '<div class="section player-card player-card'
i = t.find(anchor)
assert i > 0
cover_sec = ('<div class="section" style="text-align: center; padding: 0; background: none; border: none; backdrop-filter: none; box-shadow: none;">\n'
             ' <img src="charlie-barnes_report_cover.png" alt="报告封面" style="width: 100%; max-width: 900px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">\n'
             ' </div>\n')
t = t[:i] + cover_sec + t[i:]

# 2. 评分区：找到 <h2>\n ?? 综合评分 开头的 section，整段替换到 </blockquote>\n <hr/> 前
m = re.search(r'<h2>\s*\n\s*📊 综合评分\s*\n\s*</h2>\s*\n\s*<table>.*?</table>\s*\n\s*<h3>\s*\n\s*总体评分.*?</h3>\s*\n\s*<blockquote>.*?</blockquote>', t, re.S)
assert m, 'grades block not found'
new_grades = '''<h2>📊 综合评分</h2>
 <div style="text-align: center; margin: 20px 0;">
 <img src="charlie-barnes_overall_grades.png" alt="综合评分雷达图" style="width: 100%; max-width: 600px; border-radius: 10px;">
 </div>
 <div class="stats-grid">
 <div class="stat-card"><span class="stat-value" style="color: #ff9800;">40</span><div class="stat-label">Fastball</div><span class="grade grade-c">C</span></div>
 <div class="stat-card"><span class="stat-value" style="color: #4fc3f7;">50</span><div class="stat-label">Changeup</div><span class="grade grade-b">B-</span></div>
 <div class="stat-card"><span class="stat-value" style="color: #ff9800;">45</span><div class="stat-label">Slider</div><span class="grade grade-c">C+</span></div>
 <div class="stat-card"><span class="stat-value" style="color: #ff9800;">45</span><div class="stat-label">Curveball</div><span class="grade grade-c">C+</span></div>
 <div class="stat-card"><span class="stat-value" style="color: #4fc3f7;">50</span><div class="stat-label">Control</div><span class="grade grade-b">B-</span></div>
 <div class="stat-card"><span class="stat-value" style="color: #ff9800;">45</span><div class="stat-label">Command</div><span class="grade grade-c">C+</span></div>
 <div class="stat-card"><span class="stat-value" style="color: #4fc3f7;">50</span><div class="stat-label">Mental</div><span class="grade grade-b">B-</span></div>
 <div class="stat-card"><span class="stat-value" style="color: #4fc3f7;">50</span><div class="stat-label">Durability</div><span class="grade grade-b">B-</span></div>
 <div class="stat-card"><span class="stat-value" style="color: #f44336;">35</span><div class="stat-label">Strikeout</div><span class="grade grade-d">D+</span></div>
 </div>
 <h3>总体评分：45（C+ 级 / 边缘大联盟 depth arm）</h3>
 <blockquote>
 Charlie Barnes 是典型的 organizational depth 左投，能在小联盟稳定吃局数，偶尔作为应急升上大联盟。但在道奇这样竞争激烈的球队中，他需要显著改善球质或快速球球速才能获得更稳定的 MLB 机会。
 </blockquote>'''
t = t[:m.start()] + new_grades + t[m.end():]

io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('barnes html patched, len', len(t))
