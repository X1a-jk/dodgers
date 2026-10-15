# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
for d in ('2026-09-16', '2026-09-17', '2026-09-18'):
    text = open(rf'D:\baseball\roster\{d}.md', encoding='utf-8').read()
    for line in text.splitlines():
        if '日报 -' in line:
            print(d, '|', repr(line))
            break
    # 统计 emoji 数量
    import re
    emojis = re.findall(r'[\U0001F000-\U0001FAFF☀-➿✅-➿⚾⏰⚔️]', text)
    print('   emoji count:', len(emojis), '| ? count:', text.count('?'))
