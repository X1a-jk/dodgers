# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('D:/baseball/index.html', encoding='utf-8').read()
for kw in ('showGameModal', 'gameModal', 'calendar', '周战报', '日报', '快照'):
    idxs = [m.start() for m in re.finditer(kw, t)]
    print(kw, len(idxs), idxs[:12])
