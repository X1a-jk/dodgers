# -*- coding: utf-8 -*-
import io, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
hits = []
for p in sorted(Path(r'D:\baseball\scripts').glob('*.py')):
    try:
        t = io.open(p, encoding='utf-8').read()
    except Exception:
        continue
    for m in re.finditer(r'[^\n]*2026[^\n]*', t):
        line = m.group(0).strip()
        if line and not line.startswith('#'):
            hits.append((p.name, line[:130]))
for name, line in hits:
    print(f'{name}: {line}')
