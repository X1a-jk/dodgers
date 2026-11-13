# -*- coding: utf-8 -*-
"""Batch-12 报告验证（打者）：文件齐全 / 零宽字符 / AVG 锚点抽查。"""
import os, re, sys

ROOT = r'D:\baseball\seasons\2025\players'
BATCH = {
 'chris-taylor': {'avg': '.200', 'charts': ['taylor_report_cover.png', 'taylor_overall_grades.png', 'taylor_season_comparison.png']},
 'esteury-ruiz': {'avg': '.190', 'charts': ['ruiz_report_cover.png', 'ruiz_overall_grades.png', 'ruiz_season_comparison.png']},
 'buddy-kennedy': {'avg': '.059', 'charts': ['kennedy_report_cover.png', 'kennedy_overall_grades.png', 'kennedy_season_comparison.png']},
 'eddie-rosario': {'avg': '.250', 'charts': ['rosario_report_cover.png', 'rosario_overall_grades.png', 'rosario_season_comparison.png']},
}
ZW = re.compile(r'[\u200B-\u200F\uFEFF]')
problems = []
for slug, meta in BATCH.items():
    d = os.path.join(ROOT, slug)
    html = os.path.join(d, f'{slug}-scouting-report.html')
    md = os.path.join(d, f'{slug}-scouting-report.md')
    cfg = os.path.join(d, 'charts_config.json')
    for f, label in [(html, 'html'), (md, 'md'), (cfg, 'config')]:
        if not os.path.exists(f):
            problems.append(f'{slug}: 缺 {label}')
            continue
        if os.path.getsize(f) < 200:
            problems.append(f'{slug}: {label} 过小 {os.path.getsize(f)}B')
    for c in meta['charts']:
        p = os.path.join(d, c)
        if not os.path.exists(p):
            problems.append(f'{slug}: 缺图 {c}')
        elif os.path.getsize(p) < 3000:
            problems.append(f'{slug}: 图过小 {c} {os.path.getsize(p)}B')
    hs = os.path.join(d, 'headshot.jpg')
    if not os.path.exists(hs):
        problems.append(f'{slug}: 缺 headshot.jpg')
    for f, label in [(html, 'html'), (md, 'md')]:
        if not os.path.exists(f):
            continue
        txt = open(f, encoding='utf-8').read()
        if ZW.search(txt):
            problems.append(f'{slug} {label}: 含零宽字符')
        if meta['avg'] not in txt:
            problems.append(f'{slug} {label}: 缺 AVG 锚点 {meta["avg"]}')
    if os.path.exists(html) and os.path.exists(md):
        h = open(html, encoding='utf-8').read()
        m = open(md, encoding='utf-8').read()
        if '# ' not in m.splitlines()[0]:
            problems.append(f'{slug} md: 首行不是标题')
        if '返回报告列表' not in h:
            problems.append(f'{slug} html: 缺返回按钮')
        img_refs = len(re.findall(r'<img ', h))
        if img_refs < 3:
            problems.append(f'{slug} html: 图片引用过少 {img_refs}')
print('PROBLEMS:' if problems else 'ALL PASS (4 players)')
for p in problems:
    print(' -', p)
sys.exit(1 if problems else 0)
