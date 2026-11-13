# -*- coding: utf-8 -*-
"""Batch9 报告验证：文件齐全 + 后世视角 + 回退键 + 图片引用 + 标题 + 数据锚"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
base = r'D:\baseball\seasons\2025\players'
players = {
 'michael-kopech': ('kopech', 'Michael Kopech'),
 'alexis-diaz': ('diaz', 'Alexis Díaz'),
 'noah-davis': ('davis', 'Noah Davis'),
 'bobby-miller': ('miller', 'Bobby Miller'),
 'evan-phillips': ('phillips', 'Evan Phillips'),
}
ip_expected = {'michael-kopech': '11.0', 'alexis-diaz': '9.0', 'noah-davis': '6.0',
               'bobby-miller': '5.0', 'evan-phillips': '5.2'}
problems = []
for slug, (pfx, name) in players.items():
    d = os.path.join(base, slug)
    files = os.listdir(d)
    need = [f'{slug}-scouting-report.html', f'{slug}-scouting-report.md',
            f'{pfx}_report_cover.png', f'{pfx}_overall_grades.png', f'{pfx}_season_comparison.png',
            'headshot.jpg', 'charts_config.json']
    for n in need:
        if n not in files:
            problems.append(f'{slug}: missing {n}')
    html = open(os.path.join(d, f'{slug}-scouting-report.html'), encoding='utf-8').read()
    md = open(os.path.join(d, f'{slug}-scouting-report.md'), encoding='utf-8').read()
    for tag, txt in (('html', html), ('md', md)):
        for m in re.finditer('2026', txt):
            ctx = txt[max(0, m.start()-12):m.start()+14]
            if not re.search(r'(2026\s*(年|春|赛季目标|目标|开局|选项|年春训|年春天|年的|年没有|走向|解题钥匙|主题|前)|2026 年|的 2026|在 2026|等 2026)', ctx):
                problems.append(f'{slug} {tag}: 可疑 2026 上下文 ...{ctx}...')
    if '返回报告列表' not in html:
        problems.append(f'{slug}: no back button')
    for m in re.finditer(r'src="([^"]+\.png)"', html):
        if m.group(1) not in files:
            problems.append(f'{slug}: broken img ref {m.group(1)}')
    if f'{name} 球探报告（2025 赛季）' not in html:
        problems.append(f'{slug}: title mismatch')
    if ip_expected[slug] not in html:
        problems.append(f'{slug}: missing expected IP {ip_expected[slug]}')
print('PROBLEMS:' if problems else 'ALL PASS (5 players)')
for p in problems:
    print(' -', p)
