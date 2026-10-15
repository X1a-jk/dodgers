# -*- coding: utf-8 -*-
"""补丁6：赛程中心日历弹窗——日报链接（按北京时间索引）+ 快照路径走 FILE_INDEX.folder"""
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

# 1. 当日快照路径按 FILE_INDEX.folder 解析（迁移后日报在 seasons\2026\regular\daily\）
rep('''            let html = `<div class="gm-section-title">📰 当日内容（北京时间 ${bjDate}）</div>`;
            // 1) 当日阵容快照：按北京时间索引（美国比赛日 +1）
            try {
                const r = await fetch(`roster/${bjDate}.md?v=` + Date.now());''',
'''            let html = `<div class="gm-section-title">📰 当日内容（北京时间 ${bjDate}）</div>`;
            // 按北京时间索引（美国比赛日 +1）：日报条目在 FILE_INDEX.daily 里，带归档 folder
            const dayEntry = ((FILE_INDEX.daily || []).find(x => x.date === bjDate)) || null;
            const dayFolder = (dayEntry && dayEntry.folder) || 'roster';
            // 1) 当日阵容快照
            try {
                const r = await fetch(`${dayFolder}/${bjDate}.md?v=` + Date.now());''')

# 2. 链接区：日报按钮（主）+ 周报按钮（次）
rep('''            // 2) 所属周报（覆盖该美国日期的周）
            try {
                const d = new Date(usDate + 'T00:00:00Z');
                const monday = new Date(d);
                monday.setUTCDate(d.getUTCDate() - ((d.getUTCDay() + 6) % 7));
                const mondayStr = monday.toISOString().slice(0, 10);
                const weeks = (FILE_INDEX.weekly || []);
                const hit = weeks.find(w => w.date === mondayStr);
                if (hit && links) {
                    const b = document.createElement('button');
                    b.className = 'btn btn-ghost';
                    b.textContent = `📊 查看 ${hit.label}`;
                    b.onclick = () => { closeGameModal(); setPage('weekly'); setTimeout(() => selectFile('weekly', hit.name), 80); };
                    links.appendChild(b);
                }
            } catch (e) { /* 周报索引不可用时忽略 */ }''',
'''            // 2) 当日日报链接（按北京时间索引：美国比赛日 +1）
            try {
                if (dayEntry && links) {
                    const b = document.createElement('button');
                    b.className = 'btn btn-primary';
                    b.textContent = `⚾ 查看当日日报（${bjDate}）`;
                    b.onclick = () => { closeGameModal(); setPage('daily'); setTimeout(() => selectFile('daily', dayEntry.name), 80); };
                    links.appendChild(b);
                }
            } catch (e) { /* 日报索引不可用时忽略 */ }
            // 3) 所属周报（覆盖该美国日期的周）作为次级入口
            try {
                const d = new Date(usDate + 'T00:00:00Z');
                const monday = new Date(d);
                monday.setUTCDate(d.getUTCDate() - ((d.getUTCDay() + 6) % 7));
                const mondayStr = monday.toISOString().slice(0, 10);
                const weeks = (FILE_INDEX.weekly || []);
                const hit = weeks.find(w => w.date === mondayStr);
                if (hit && links) {
                    const b = document.createElement('button');
                    b.className = 'btn btn-ghost';
                    b.textContent = `📊 所属周报 · ${hit.label}`;
                    b.onclick = () => { closeGameModal(); setPage('weekly'); setTimeout(() => selectFile('weekly', hit.name), 80); };
                    links.appendChild(b);
                }
            } catch (e) { /* 周报索引不可用时忽略 */ }''')

io.open(P, 'w', encoding='utf-8').write(t)
print('done, len', len(t))
