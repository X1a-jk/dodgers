# -*- coding: utf-8 -*-
# 一次性：为 charlie-barnes 补旧版风格封面（其 HTML 无 <img> 引用，仅为文件一致性）
import io
import json
import os
import re
import importlib.util

spec = importlib.util.spec_from_file_location('rc', r'D:\baseball\scripts\regen-covers-old-style.py')
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

stats = json.load(io.open(r'D:\baseball\data\final-stats.json', encoding='utf-8'))
roster = {p['name']: p for p in json.load(io.open(r'D:\baseball\data\season-roster.json', encoding='utf-8'))['players']}
rp = roster['Charlie Barnes']
p26 = stats['pitching_2026'][str(rp['id'])]
grid = [
    ('ERA', p26.get('era', '—')), ('WHIP', p26.get('whip', '—')),
    ('K', str(p26.get('strikeOuts', '—'))), ('IP', p26.get('inningsPitched', '—')),
    ('W-L', f"{p26.get('wins', 0)}-{p26.get('losses', 0)}"),
    ('K/9', rc.fmt1(p26.get('strikeoutsPer9Inn'))), ('BB/9', rc.fmt1(p26.get('walksPer9Inn'))),
    ('Age', str(p26.get('age', '—'))),
]
era = float(p26.get('era') or 99)
tag = ('王牌' if era <= 2.5 else '主力' if era <= 3.5 else '轮值' if era <= 4.5 else '起伏' if era <= 6 else '待调整') + '中继'
if p26.get('gamesPitched', 99) < 15:
    tag += '（小样本）'
pdir = r'D:\baseball\report\charlie-barnes'
html = io.open(os.path.join(pdir, 'charlie-barnes-scouting-report.html'), encoding='utf-8').read()
targets = set(re.findall(r'([\w-]+_report_cover\.png)', html)) | {'charlie-barnes_report_cover.png', 'barnes_report_cover.png'}
for f in targets:
    rc.render_cover('Charlie Barnes', '57', 'P', '投手', grid, tag, os.path.join(pdir, f))
    print('wrote', f, '|', tag)
# 同步封存批次
for batch in ('players-regular',):
    dst = os.path.join(r'D:\baseball\seasons\2026', batch, 'charlie-barnes')
    if os.path.isdir(dst):
        import shutil
        for f in targets:
            shutil.copy2(os.path.join(pdir, f), os.path.join(dst, f))
        print('synced to', batch)
