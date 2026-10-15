# -*- coding: utf-8 -*-
"""补丁2：门户模块阅读器支持季后赛战报子目录"""
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

# 1. 路由：postseason 走 renderModule
rep("            } else if (page === 'weekly' || page === 'daily') {\n                renderModule(page);",
    "            } else if (page === 'weekly' || page === 'daily' || page === 'postseason') {\n                renderModule(page);")

# 2. 标题映射
rep("                recap: '常规赛总结',",
    "                recap: '常规赛总结',\n                postseason: '季后赛战报',")

# 3. renderModule 泛化
rep('''        function renderModule(type) {
            const content = $('#content');
            const files = FILE_INDEX[type];
            const title = type === 'weekly' ? '每周战报' : '每日阵容';
            const folder = type === 'weekly' ? 'weekly' : 'roster';''',
'''        const MODULE_META = {
            weekly: { title: '每周战报 · 常规赛存档', folder: 'weekly' },
            daily: { title: '每日阵容 · 常规赛存档', folder: 'roster' },
            postseason: { title: '季后赛战报 · 金色十月', folder: 'weekly/postseason' }
        };

        function renderModule(type) {
            const content = $('#content');
            const meta = MODULE_META[type] || { title: type, folder: type };
            const files = FILE_INDEX[type] || [];
            const title = meta.title;
            const folder = meta.folder;''')

# 4. selectFile 泛化
rep('''        async function selectFile(type, filename) {
            const folder = type === 'weekly' ? 'weekly' : 'roster';''',
'''        async function selectFile(type, filename) {
            const folder = (MODULE_META[type] || {}).folder || (type === 'weekly' ? 'weekly' : 'roster');''')

# 5. renderRecapPage 增加季后赛战报存档区
rep('''        function viewWeeklyArchive(name) {
            setPage('weekly');
            setTimeout(() => { try { selectFile('weekly', name); } catch (e) { } }, 400);
        }''',
'''        function viewWeeklyArchive(name) {
            setPage('weekly');
            setTimeout(() => { try { selectFile('weekly', name); } catch (e) { } }, 400);
        }

        function viewPsArchive(name) {
            setPage('postseason');
            setTimeout(() => { try { selectFile('postseason', name); } catch (e) { } }, 400);
        }''')

rep('''            const weeklyFiles = ((window.FILE_INDEX || {}).weekly) || [];''',
'''            const weeklyFiles = ((window.FILE_INDEX || {}).weekly) || [];
            const psFiles = ((window.FILE_INDEX || {}).postseason) || [];''')

rep('''            const weekItems = weeklyFiles.map(f => `
                <div class="module-file-item" onclick="viewWeeklyArchive('${f.name}')">${f.label}</div>`).join('');''',
'''            const weekItems = weeklyFiles.map(f => `
                <div class="module-file-item" onclick="viewWeeklyArchive('${f.name}')">${f.label}</div>`).join('');
            const psItems = psFiles.map(f => `
                <div class="module-file-item" onclick="viewPsArchive('${f.name}')">${f.label}</div>`).join('');''')

rep('''                <div class="dashboard-section">
                    <div class="dashboard-section-title">📚 周战报全存档 <span class="gh-tag">点击跳转到周报阅读器</span></div>
                    <div class="dashboard-card">
                        <div class="module-file-list" style="max-height:320px;overflow-y:auto;">${weekItems || '<p class="dc-stats">暂无存档</p>'}</div>
                    </div>
                </div>''',
'''                <div class="dashboard-section">
                    <div class="dashboard-section-title">📚 周战报全存档 <span class="gh-tag">常规赛 · 点击跳转阅读器</span></div>
                    <div class="dashboard-card">
                        <div class="module-file-list" style="max-height:320px;overflow-y:auto;">${weekItems || '<p class="dc-stats">暂无存档</p>'}</div>
                    </div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">🍂 季后赛战报 <span class="gh-tag">外卡轮结束后开始生成 · 点击跳转阅读器</span></div>
                    <div class="dashboard-card">
                        <div class="module-file-list" style="max-height:240px;overflow-y:auto;">${psItems || '<p class="dc-stats">暂无季后赛战报——外卡轮（10/01 前后）结束后，每周一生成系列赛总结。</p>'}</div>
                    </div>
                </div>''')

io.open(P, 'w', encoding='utf-8').write(t)
print('done, len', len(t))
