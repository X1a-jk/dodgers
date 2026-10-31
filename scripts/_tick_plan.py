# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
p = r'D:\baseball\PLAYER-REPORTS-PLAN.md'
src = open(p, encoding='utf-8').read()
players = sys.argv[1:]
for name in players:
    lines = src.split('\n')
    hit = 0
    for i, ln in enumerate(lines):
        if ln.startswith('| [ ]') and f'| {name} |' in ln:
            lines[i] = ln.replace('| [ ] |', '| [x] |').replace('旧版待更新', '✅ 10-26 旧版重写')
            hit += 1
    src = '\n'.join(lines)
    print(name, 'ticked:', hit)
open(p, 'w', encoding='utf-8', newline='\n').write(src)
