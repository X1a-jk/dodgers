# -*- coding: utf-8 -*-
"""项目审计：index.html fetch 引用存在性 + 日报管线引用 + 关键路径"""
import io, re, os, json

BASE = r'D:\baseball'
out = io.open(os.path.join(BASE, 'scripts', '_audit.txt'), 'w', encoding='utf-8')

# 1. index.html 中所有静态 fetch/引用路径
t = io.open(os.path.join(BASE, 'index.html'), encoding='utf-8').read()
paths = set()
for m in re.finditer(r"fetch\('([^']+)'", t):
    p = m.group(1)
    if p.startswith(('http', 'data:', 'blob:')) or '${' in p:
        continue
    paths.add(p)
for m in re.finditer(r"fetchJsonWithBak\('([^']+)'", t):
    paths.add(m.group(1))
out.write('== index.html 静态引用 ==\n')
missing = []
for p in sorted(paths):
    # 带 ?v= 的去掉参数
    clean = p.split('?')[0]
    exists = os.path.exists(os.path.join(BASE, clean.replace('/', os.sep)))
    out.write('  %s %s\n' % ('OK ' if exists else 'MISSING', p))
    if not exists:
        missing.append(p)

# 2. 日报管线引用
out.write('\n== run-daily-update.ps1 引用的脚本 ==\n')
ps1 = io.open(os.path.join(BASE, 'scripts', 'run-daily-update.ps1'), encoding='utf-8').read()
for m in sorted(set(re.findall(r'scripts[\\/]([\w.-]+\.(?:py|ps1))', ps1))):
    exists = os.path.exists(os.path.join(BASE, 'scripts', m))
    out.write('  %s %s\n' % ('OK ' if exists else 'MISSING', m))

# 3. FILE_INDEX folder 路径存在性
fi = json.load(open(os.path.join(BASE, 'portal', 'file-index.json'), encoding='utf-8'))
out.write('\n== FILE_INDEX folder 路径 ==\n')
folders = set()
for key in ['weekly', 'daily', 'postseason']:
    for e in fi.get(key, []):
        folders.add(e.get('folder', ''))
for f in sorted(folders):
    exists = os.path.exists(os.path.join(BASE, f.replace('/', os.sep)))
    out.write('  %s %s\n' % ('OK ' if exists else 'MISSING', f))

# 4. reportEditions 路径
out.write('\n== reportEditions 路径 ==\n')
for e in fi.get('reportEditions', []):
    folder = e.get('folder', '')
    exists = os.path.exists(os.path.join(BASE, folder.replace('/', os.sep)))
    out.write('  %s %s -> %s\n' % ('OK ' if exists else 'MISSING', e.get('label'), folder))

# 5. 顶层结构
out.write('\n== 顶层结构 ==\n')
for d in ['weekly', 'roster', 'data', 'report', 'seasons/2026/players', 'seasons/2026/players-regular',
          'seasons/2026/players-postseason', 'seasons/2026/snapshots', 'portal']:
    p = os.path.join(BASE, *d.split('/'))
    if os.path.isdir(p):
        n = sum(len(files) for _, _, files in os.walk(p))
        out.write('  OK  %-32s %d files\n' % (d, n))
    else:
        out.write('  --  %s (不存在)\n' % d)
out.write('  report\\ 不存在 = 已封存，预期\n')

out.close()
print('audit done')
