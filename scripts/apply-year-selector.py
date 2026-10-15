# -*- coding: utf-8 -*-
"""补丁4：战报/日报阅读器加年份选择器（接口预留：FILE_INDEX.years 驱动）"""
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

# 1. CSS：年份选择器样式
rep('        /* ===== 季后赛对阵图 ===== */',
'''        /* ===== 年份选择器（战报/日报阅读器） ===== */
        .module-year-bar {
            display: flex; align-items: center; gap: 8px;
            padding: 8px 12px; border-bottom: 1px solid var(--border);
        }
        .module-year-select {
            background: var(--panel-solid); color: var(--text);
            border: 1px solid var(--border); border-radius: 8px;
            padding: 6px 10px; font-size: 0.85rem; cursor: pointer; flex: 1;
        }
        .module-year-select:focus { outline: 1px solid var(--dodgers-light); }
        body.october .module-year-select:focus { outline-color: #f5b942; }
        .module-year-hint { font-size: 0.75rem; color: var(--text-muted); white-space: nowrap; }

        /* ===== 季后赛对阵图 ===== */''')

# 2. helper：可用年份清单
rep('''        const MODULE_META = {''',
'''        function fileIndexYears() {
            const idx = (typeof FILE_INDEX !== 'undefined') ? FILE_INDEX : (window.FILE_INDEX || {});
            if (Array.isArray(idx.years) && idx.years.length) return idx.years;
            const set = new Set();
            ['weekly', 'daily', 'postseason'].forEach(k => (idx[k] || []).forEach(f => { if (f.season) set.add(f.season); }));
            return Array.from(set).sort().reverse();
        }

        const MODULE_META = {''')

# 3. renderModule：年份选择条 + 条目带 data-season
rep('''                        <div class="module-search">
                            <input type="text" id="${type}-search" placeholder="搜索日期或 Week..." oninput="filterFiles('${type}', this.value)">
                        </div>
                        <div class="module-file-list" id="${type}-list">
                            ${files.map(f => `
                                <div class="module-file-item" data-file="${f.name}" data-label="${f.label}" onclick="selectFile('${type}','${f.name}')">${f.label}</div>
                            `).join('')}
                        </div>''',
'''                        <div class="module-year-bar">
                            <select id="${type}-year" class="module-year-select" onchange="filterFiles('${type}', document.getElementById('${type}-search').value)">
                                <option value="">全部年份</option>
                                ${fileIndexYears().map(y => `<option value="${y}">${y} 赛季</option>`).join('')}
                            </select>
                            <span class="module-year-hint">共 ${files.length} 份 · 按年分档</span>
                        </div>
                        <div class="module-search">
                            <input type="text" id="${type}-search" placeholder="搜索日期或 Week..." oninput="filterFiles('${type}', this.value)">
                        </div>
                        <div class="module-file-list" id="${type}-list">
                            ${files.map(f => `
                                <div class="module-file-item" data-file="${f.name}" data-label="${f.label}" data-season="${f.season || ''}" onclick="selectFile('${type}','${f.name}')">${f.label}</div>
                            `).join('')}
                        </div>''')

# 4. filterFiles：年份 + 关键词组合过滤
rep('''        function filterFiles(type, query) {
            const q = query.trim().toLowerCase();
            $$(`#${type}-list .module-file-item`).forEach(el => {
                const label = el.dataset.label.toLowerCase();
                el.style.display = label.includes(q) ? '' : 'none';
            });
        }''',
'''        function filterFiles(type, query) {
            const q = (query || '').trim().toLowerCase();
            const yearSel = $(`#${type}-year`);
            const year = yearSel ? yearSel.value : '';
            $$(`#${type}-list .module-file-item`).forEach(el => {
                const label = el.dataset.label.toLowerCase();
                const matchQ = !q || label.includes(q);
                const matchY = !year || el.dataset.season === year;
                el.style.display = (matchQ && matchY) ? '' : 'none';
            });
        }''')

io.open(P, 'w', encoding='utf-8').write(t)
print('done, len', len(t))
