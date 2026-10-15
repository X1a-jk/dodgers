# -*- coding: utf-8 -*-
"""补丁3：FILE_INDEX 改 let（运行时刷新真正生效）+ selectFile 按条目 folder 取文件"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
P = r'D:\baseball\index.html'
t = io.open(P, encoding='utf-8').read()

def rep(old, new, count=1):
    global t
    n = t.count(old)
    assert n == count, f'anchor {n}x: {old[:70]!r}'
    t = t.replace(old, new, count)
    print('ok:', old.strip()[:60].replace('\n', ' '))

# 1. 内嵌索引改 let
i = t.find('const FILE_INDEX = {')
assert i > 0
t = t[:i] + 'let FILE_INDEX = {' + t[i + len('const FILE_INDEX = {'):]
print('ok: FILE_INDEX -> let')

# 2. selectFile 用条目的 folder
rep('''        async function selectFile(type, filename) {
            const folder = (MODULE_META[type] || {}).folder || (type === 'weekly' ? 'weekly' : 'roster');''',
'''        async function selectFile(type, filename) {
            const entry = ((typeof FILE_INDEX !== 'undefined' ? FILE_INDEX : {})[type] || [])
                .find(x => x.name === filename);
            const folder = (entry && entry.folder)
                || (MODULE_META[type] || {}).folder
                || (type === 'weekly' ? 'weekly' : 'roster');''')

io.open(P, 'w', encoding='utf-8').write(t)
print('done, len', len(t))
