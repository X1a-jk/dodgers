# -*- coding: utf-8 -*-
"""Batch-11 报告验证：文件齐全 / 零宽字符 / ERA 锚点抽查。"""
import os, re, sys

ROOT = r'D:\baseball\seasons\2025\players'
BATCH = {
 'brock-stewart': {'era': '4.91', 'charts': ['stewart_report_cover.png', 'stewart_overall_grades.png', 'stewart_season_comparison.png']},
 'andrew-heaney': {'era': '13.50', 'charts': ['heaney_report_cover.png', 'heaney_overall_grades.png', 'heaney_season_comparison.png']},
 'jp-feyereisen': {'era': '13.50', 'charts': ['feyereisen_report_cover.png', 'feyereisen_overall_grades.png', 'feyereisen_season_comparison.png']},
 'julian-fernandez': {'era': '9.00', 'charts': ['fernandez_report_cover.png', 'fernandez_overall_grades.png', 'fernandez_season_comparison.png']},
 'paul-gervase': {'era': '4.50', 'charts': ['gervase_report_cover.png', 'gervase_overall_grades.png', 'gervase_season_comparison.png']},
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
        if meta['era'] not in txt:
            problems.append(f'{slug} {label}: 缺 ERA 锚点 {meta["era"]}')
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
print('PROBLEMS:' if problems else 'ALL PASS (5 players)')
for p in problems:
    print(' -', p)
sys.exit(1 if problems else 0)
