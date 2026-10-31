# -*- coding: utf-8 -*-
"""验证 4 人报告：文件齐全、图表新鲜度、OPS 恒等式、关键数据 vs final-stats"""
import io, json, os, re

BASE = r'D:\baseball'
fs = json.load(open(os.path.join(BASE, 'data', 'final-stats.json'), encoding='utf-8'))

PLAYERS = {
    'seth-halvorsen':    {'id': '678020', 'kind': 'pitch', 'era': '8.10', 'ip': '10.0', 'whip': '1.30', 'g': 11},
    'santiago-espinal':  {'id': '669289', 'kind': 'hit',   'line': '.268/.276/.375', 'g': 36},
    'ben-rortvedt':      {'id': '666163', 'kind': 'hit',   'line': '.185/.185/.185', 'g': 16},
    'jonathan-hernandez':{'id': '642546', 'kind': 'pitch', 'era': '5.68', 'ip': '25.1', 'whip': '1.34', 'g': 16},
}

out = io.open(os.path.join(BASE, 'scripts', '_verify4.txt'), 'w', encoding='utf-8')
for slug, info in PLAYERS.items():
    d = os.path.join(BASE, 'report', slug)
    out.write(f'===== {slug} =====\n')
    # 1. files
    files = sorted(os.listdir(d))
    out.write('files: ' + ', '.join(files) + '\n')
    pngs = [f for f in files if f.endswith('.png')]
    charts = [f for f in pngs if 'cover' not in f]
    out.write(f'charts({len(charts)}): {charts}\n')
    for f in pngs:
        mt = os.path.getmtime(os.path.join(d, f))
        import datetime
        out.write(f'  {f}  mtime={datetime.datetime.fromtimestamp(mt):%m-%d %H:%M}\n')
    # 2. html checks
    t = io.open(os.path.join(d, f'{slug}-scouting-report.html'), encoding='utf-8').read()
    for k in ['era', 'ip', 'whip', 'g', 'line']:
        if k in info and info[k] is not None:
            needle = str(info[k])
            out.write(f'  html contains {k}={needle}: {needle in t}\n')
    # OPS identity check: find OPS mentions near OBP/SLG
    for m in re.finditer(r'OPS[^\d]{0,10}(\d?\.\d{3})', t):
        pass
    # explicit: look for pattern like .651 / .370 etc in md too
    # 3. FS cross-check
    grp = 'pitching_2026' if info['kind'] == 'pitch' else 'hitting_2026'
    fsd = fs.get(grp, {}).get(info['id'])
    if fsd:
        if info['kind'] == 'pitch':
            out.write(f"  FS: G={fsd.get('gamesPlayed')} ERA={fsd.get('era')} IP={fsd.get('inningsPitched')} WHIP={fsd.get('whip')} K={fsd.get('strikeOuts')} BB={fsd.get('baseOnBalls')} HR={fsd.get('homeRuns')} H={fsd.get('hits')}\n")
        else:
            out.write(f"  FS: G={fsd.get('gamesPlayed')} AVG={fsd.get('avg')} OBP={fsd.get('obp')} SLG={fsd.get('slg')} OPS={fsd.get('ops')} HR={fsd.get('homeRuns')} RBI={fsd.get('rbi')} BB={fsd.get('baseOnBalls')} SO={fsd.get('strikeOuts')}\n")
    else:
        out.write('  FS: NO ENTRY\n')
    # OPS constant check in FS itself
    if fsd and info['kind'] == 'hit':
        try:
            ops = float(fsd['ops']); obp = float(fsd['obp']); slg = float(fsd['slg'])
            out.write(f"  OPS identity: {ops:.3f} vs OBP+SLG={obp+slg:.3f} diff={abs(ops-obp-slg):.4f}\n")
        except Exception as e:
            out.write(f'  OPS check err {e}\n')
    out.write('\n')
out.close()
print('done')
