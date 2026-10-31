# -*- coding: utf-8 -*-
import re, datetime
from pathlib import Path

stale = []
for batch in ['players', 'players-regular', 'players-postseason']:
    for d in Path(batch).iterdir():
        if not d.is_dir():
            continue
        htmls = list(d.glob('*-scouting-report.html'))
        if not htmls:
            continue
        html = htmls[0].read_text(encoding='utf-8')
        refs = set(re.findall(r'src="([^"]*_season_comparison\.png)"', html))
        for f in d.glob('*_season_comparison.png'):
            if f.stat().st_mtime < datetime.datetime(2026, 10, 31).timestamp():
                stale.append((batch, d.name, f.name,
                              'REFERENCED' if f.name in refs else 'orphan'))

ref = [s for s in stale if s[3] == 'REFERENCED']
orp = [s for s in stale if s[3] == 'orphan']
print('stale but REFERENCED by HTML:', len(ref))
for s in ref:
    print('  ', s)
print('stale orphan (not displayed):', len(orp))
