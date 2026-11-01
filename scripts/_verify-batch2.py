# -*- coding: utf-8 -*-
"""批次2报告验证：文件齐全 + 无2026泄漏 + OPS 恒等式"""
import io, re, os, sys

slugs = ['andy-pages', 'teoscar-hernandez', 'michael-conforto', 'will-smith', 'max-muncy']
base = r'D:\baseball\seasons\2025\players'
errors = []

for s in slugs:
    d = os.path.join(base, s)
    files = os.listdir(d)
    for n in [s + '-scouting-report.html', s + '-scouting-report.md', 'headshot.jpg', 'charts_config.json']:
        if n not in files:
            errors.append('%s: missing %s' % (s, n))
    pngs = [f for f in files if f.endswith('.png')]
    if len(pngs) < 3:
        errors.append('%s: only %d pngs' % (s, len(pngs)))
    html = io.open(os.path.join(d, s + '-scouting-report.html'), encoding='utf-8').read()
    md = io.open(os.path.join(d, s + '-scouting-report.md'), encoding='utf-8').read()
    for tag, txt in (('html', html), ('md', md)):
        for m in re.finditer(r'.{60}2026.{60}', txt):
            errors.append('%s %s LEAK: ...%s...' % (s, tag, m.group(0)))
    # 常规赛对比表：AVG OBP SLG OPS 连续四格
    for m in re.finditer(r'<td>(\.\d{3})</td>\s*<td>(\.\d{3})</td>\s*<td>(\.\d{3})</td>\s*<td>(\.\d{3})</td>', html):
        avg, obp, slg, ops = map(float, m.groups())
        if abs(obp + slg - ops) > 0.002:
            errors.append('%s: OPS fail avg=%.3f obp=%.3f slg=%.3f ops=%.3f' % (s, avg, obp, slg, ops))
    # 季后赛表：PA AVG OBP SLG OPS(highlight)
    for m in re.finditer(r'<td>(\d+)</td><td>(\d+)</td><td>(\.\d{3})</td><td>(\.\d{3})</td><td>(\.\d{3})</td><td class="highlight">(\.\d{3})</td>', html):
        obp, slg, ops = float(m.group(4)), float(m.group(5)), float(m.group(6))
        if abs(obp + slg - ops) > 0.002:
            errors.append('%s: PS OPS fail %s' % (s, m.groups()))
    # headshot 非 0 字节
    hs = os.path.join(d, 'headshot.jpg')
    if os.path.getsize(hs) < 2000:
        errors.append('%s: headshot too small (%d bytes)' % (s, os.path.getsize(hs)))

sys.stdout.reconfigure(encoding='utf-8')
if errors:
    print('ERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)
print('BATCH2 VERIFY: ALL PASS (5 players x files / no-2026-leak / OPS identity / headshot size)')
