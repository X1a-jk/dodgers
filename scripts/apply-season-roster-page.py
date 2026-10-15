# -*- coding: utf-8 -*-
"""补丁5：门户「📜 历年阵容」页 + 球员报告版本切换"""
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

# 0. CSS：补 tag-yellow / tag-blue
rep('''        /* ===== 年份选择器（战报/日报阅读器） ===== */''',
'''        .tag-yellow {
            background: rgba(234, 179, 8, 0.18);
            color: #fde047;
        }
        .tag-blue {
            background: rgba(79, 195, 247, 0.15);
            color: #7dd3fc;
        }

        /* ===== 年份选择器（战报/日报阅读器） ===== */''')

# 1. 导航：阵容组加「历年阵容」
rep('''                    <a class="nav-item" data-page="transactions">
                        <span class="nav-icon">🔄</span> 人员变动
                    </a>''',
'''                    <a class="nav-item" data-page="transactions">
                        <span class="nav-icon">🔄</span> 人员变动
                    </a>
                    <a class="nav-item" data-page="seasonroster">
                        <span class="nav-icon">📜</span> 历年阵容
                    </a>''')

# 2. 标题映射
rep("                postseason: '季后赛战报',",
    "                postseason: '季后赛战报',\n                seasonroster: '历年阵容',")

# 3. 路由
rep('''            } else if (page === 'recap') {
                renderRecapPage();
            } else if (page === 'depth') {''',
'''            } else if (page === 'recap') {
                renderRecapPage();
            } else if (page === 'seasonroster') {
                renderSeasonRosterPage();
            } else if (page === 'depth') {''')

# 4. 命令面板
rep("            { id: 'recap',        label: '常规赛总结',     icon: '🏁' },",
    "            { id: 'recap',        label: '常规赛总结',     icon: '🏁' },\n            { id: 'seasonroster', label: '历年阵容',       icon: '📜' },")

# 5. 新页面渲染函数（插在 applyOctoberTheme 前）
rep('''        /* ---------- 十月主题：赛程公布或进入 10 月自动启用 ---------- */''',
'''        /* ---------- 历年阵容（按年分档，含中途签来/DFA） ---------- */
        const SR_STATUS = {
            a:      { cn: '活跃',   cls: 'tag-green' },
            active: { cn: '活跃',   cls: 'tag-green' },
            il:     { cn: '伤病',   cls: 'tag-yellow' },
            d10:    { cn: '伤病',   cls: 'tag-yellow' },
            d15:    { cn: '伤病',   cls: 'tag-yellow' },
            d60:    { cn: '伤病',   cls: 'tag-yellow' },
            rm:     { cn: '小联盟', cls: 'tag-blue' },
            minors: { cn: '小联盟', cls: 'tag-blue' },
            departed: { cn: '已离队', cls: 'tag-red' },
        };

        async function renderSeasonRosterPage() {
            const content = $('#content');
            const years = fileIndexYears();
            const cur = ((typeof FILE_INDEX !== 'undefined' ? FILE_INDEX : {}).currentSeason)
                || String(new Date().getFullYear());
            content.innerHTML = `
                <div class="dashboard-section">
                    <div class="dashboard-section-title">📜 历年阵容 <span class="gh-tag">该赛季所有为道奇出场过的球员 · 含中途签来 / DFA / 交易离队</span></div>
                    <div class="module-year-bar" style="border:1px solid var(--border);border-radius:12px;background:var(--panel);margin-bottom:14px;">
                        <select id="sr-year" class="module-year-select" onchange="renderSeasonRosterTable()">
                            ${years.map(y => `<option value="${y}" ${y === cur ? 'selected' : ''}>${y} 赛季</option>`).join('')}
                        </select>
                        <span class="module-year-hint" id="sr-hint"></span>
                    </div>
                    <div id="sr-body"><div class="schedule-loading"><div>⏳ 正在加载阵容...</div></div></div>
                </div>`;
            await renderSeasonRosterTable();
        }

        async function renderSeasonRosterTable() {
            const year = $('#sr-year').value;
            const cur = ((typeof FILE_INDEX !== 'undefined' ? FILE_INDEX : {}).currentSeason)
                || String(new Date().getFullYear());
            const body = $('#sr-body');
            const hint = $('#sr-hint');
            body.innerHTML = '<div class="schedule-loading"><div>⏳ 正在加载阵容...</div></div>';

            let data = null, source = '';
            const paths = [];
            if (year === cur) paths.push(['data/season-roster.json', 'current']);
            paths.push([`seasons/${year}/snapshots/season-roster.json`, 'snapshot']);
            if (year === cur) paths.push(['data/season-roster.json.bak', 'bak']);
            for (const [p, s] of paths) {
                try {
                    const r = await fetch(p + '?v=' + Date.now());
                    if (r.ok) { data = await r.json(); source = s; break; }
                } catch (e) { /* try next */ }
            }
            if (!data || !Array.isArray(data.players)) {
                body.innerHTML = `<div class="schedule-error"><strong>${year} 赛季阵容数据不存在</strong><br>
                    该年份封存时未快照 season-roster.json，或赛季尚未开始。</div>`;
                hint.textContent = '';
                return;
            }

            const sm = data.summary || {};
            const chip = (label, val, color) =>
                `<div class="dashboard-card" style="text-align:center;padding:12px 8px;"><div style="font-size:1.4rem;font-weight:900;color:${color};">${val}</div><div class="dc-stats">${label}</div></div>`;

            const rows = data.players.map(p => {
                const st = SR_STATUS[p.status] || { cn: p.statusCn || p.status, cls: 'tag-blue' };
                const batLine = p.bat ? `打击 ${p.bat.avg} · ${p.bat.hr} HR · ${p.bat.rbi} RBI` : '';
                const pitLine = p.pit ? `投球 ${p.pit.w}-${p.pit.l} · ${p.pit.era} ERA · ${p.pit.so} K${p.pit.sv ? ' · ' + p.pit.sv + ' SV' : ''}` : '';
                const statLine = [batLine, pitLine].filter(Boolean).join('<br>') || '-';
                const trail = [];
                if (p.joined) trail.push(`<span class="tag tag-green">＋ ${p.joined}</span>`);
                if (!p.joined && p.status !== 'departed') trail.push('<span class="dc-stats">季初在队</span>');
                if (p.departed) trail.push(`<span class="tag tag-red">－ ${p.departed}</span>`);
                const lad = p.status === 'departed' ? '' : (p.status === 'a' || p.status === 'active' ? 'background:rgba(0,90,156,0.18);' : '');
                return `<tr style="${lad}">
                    <td><span class="st-team">${p.name}</span></td>
                    <td>${p.pos || '-'}</td>
                    <td>${p.g}</td>
                    <td class="dc-stats">${statLine}</td>
                    <td><span class="tag ${st.cls}">${st.cn}</span></td>
                    <td>${trail.join(' ') || '-'}</td>
                </tr>`;
            }).join('');

            hint.textContent = `${data.season} 赛季 · ${data.players.length} 人 · 按出场数排序`;
            body.innerHTML = `
                <div class="dashboard-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin-bottom:14px;">
                    ${chip('总出场人数', sm.total ?? '-', '#4fc3f7')}
                    ${chip('活跃', sm.current ?? '-', '#22c55e')}
                    ${chip('伤病名单', sm.il ?? '-', '#eab308')}
                    ${chip('小联盟', sm.minors ?? '-', '#4fc3f7')}
                    ${chip('已离队', sm.departed ?? '-', '#ef4444')}
                    ${chip('中途加入', sm.joinedMidseason ?? '-', '#f5b942')}
                </div>
                <div class="dashboard-card" style="overflow-x:auto;">
                    <table class="st-table compact">
                        <thead><tr><th>球员</th><th>位置</th><th>出场</th><th>赛季数据</th><th>现状</th><th>赛季轨迹</th></tr></thead>
                        <tbody>${rows}</tbody>
                    </table>
                </div>
                <div class="data-age">数据时间：${data.generatedAt ? new Date(data.generatedAt).toLocaleString('zh-CN') : '未知'} · 来源：MLB Stats API + transactions 全量解析（${source === 'snapshot' ? '年份封存快照' : '实时数据'}）</div>
            `;
        }

        /* ---------- 球员报告版本切换 ---------- */
        function reportEditions() {
            const idx = (typeof FILE_INDEX !== 'undefined') ? FILE_INDEX : (window.FILE_INDEX || {});
            if (Array.isArray(idx.reportEditions) && idx.reportEditions.length) return idx.reportEditions;
            return [{ label: '当前报告', path: 'report/index.html', current: true }];
        }

        function switchReportEdition() {
            const sel = $('#rep-edition');
            const iframe = $('#report-iframe');
            if (sel && iframe) iframe.src = sel.value + '?v=' + Date.now();
        }

        /* ---------- 十月主题：赛程公布或进入 10 月自动启用 ---------- */''')

# 6. 球员报告页：加版本选择条
rep('''            } else if (page === 'reports') {
                const cacheBuster = new Date().getTime();
                content.innerHTML = `
                    <div style="background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; height: calc(100vh - 170px); min-height: 600px;">
                        <iframe src="report/index.html?v=${cacheBuster}" style="width: 100%; height: 100%; border: none;"></iframe>
                    </div>
                `;
            }''',
'''            } else if (page === 'reports') {
                const cacheBuster = new Date().getTime();
                const editions = reportEditions();
                content.innerHTML = `
                    <div class="module-year-bar" style="border:1px solid var(--border);border-radius:12px 12px 0 0;background:var(--panel);">
                        <span style="font-size:0.85rem;color:var(--text-muted);white-space:nowrap;">报告版本：</span>
                        <select id="rep-edition" class="module-year-select" style="max-width:280px;" onchange="switchReportEdition()">
                            ${editions.map(e => `<option value="${e.path}">${e.label}</option>`).join('')}
                        </select>
                        <button class="btn btn-ghost" onclick="window.open(document.getElementById('rep-edition').value + '?v=' + Date.now(), '_blank')">在新标签打开</button>
                        <span class="module-year-hint">赛季中可存多批次：全明星版 / 常规赛版 / 季后赛版</span>
                    </div>
                    <div style="background: var(--panel); border: 1px solid var(--border); border-top: none; border-radius: 0 0 var(--radius) var(--radius); overflow: hidden; height: calc(100vh - 225px); min-height: 560px;">
                        <iframe id="report-iframe" src="${editions[0].path}?v=${cacheBuster}" style="width: 100%; height: 100%; border: none;"></iframe>
                    </div>
                `;
            }''')

io.open(P, 'w', encoding='utf-8').write(t)
print('done, len', len(t))
