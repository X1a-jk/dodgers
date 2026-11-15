# -*- coding: utf-8 -*-
"""重新生成 ORGAN_TUNES 并整体替换 index.html 中的旧块（锚点：注释头 ~ '};'）"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

tunes = io.open(r'D:\baseball\data\_organ_tunes.js.txt', encoding='utf-8').read().rstrip()
idx_path = r'D:\baseball\index.html'
html = io.open(idx_path, encoding='utf-8-sig').read()

START = '        /* 8-bit 曲库'
i = html.find(START)
assert i > 0, 'tunes block start not found'
if html.find('\n        };\n        };\n', i) > 0:
    endmark = '\n        };\n        };\n'
else:
    endmark = '\n        };\n'
j = html.find(endmark, i)
assert j > i, 'tunes block end not found'
old_block = html[i:j + len(endmark)]
assert old_block.count('banner:') == 1 and old_block.count('saints:') == 1
tunes = tunes.rstrip()
assert tunes.endswith('        };')
html = html[:i] + tunes + '\n' + html[j + len(endmark):]
io.open(idx_path, 'w', encoding='utf-8', newline='\n').write(html)
print('SWAP_OK, size', len(html))
