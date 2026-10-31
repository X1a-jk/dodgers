# -*- coding: utf-8 -*-
"""renderRecapPage 年份参数化 + 赛季总结文档入口
- 年份选择器（对齐历年阵容页模式），非当前年份读 seasons/YYYY/snapshots/
- 周战报/季后赛战报列表按 FILE_INDEX season 过滤
- 赛季总结叙事文档（seasons/YYYY/YYYY-赛季总结.md）阅读入口
"""
import io

p = r'D:\baseball\index.html'
t = io.open(p, encoding='utf-8').read()

start = t.find('async function renderRecapPage() {')
assert start > 0, 'recap function start not found'
end = t.find('/* ---------- 历年阵容', start)
assert end > start, 'recap function end not found'

NEW = '''async function renderRecapPage() {
            const content = $('#content');
            const years = fileIndexYears();
            const cur = ((typeof FILE_INDEX !== 'undefined' ? FILE_INDEX : {}).currentSeason)
                || String(new Date().getFullYear());
            content.innerHTML = `
                <div class="dashboard-section">
                    <div class="dashboard-section-title">📋 常规赛总结 <span class="gh-tag">战绩 · 排名 · 领袖 · 战报存档</span></div>
                    <div class="module-year-bar" style="border:1px solid var(--border);border-radius:12px;background:var(--panel);margin-bottom:14px;">
                        <select id="rc-year" class="module-year-select" onchange="renderRecapContent()">
                            ${years.map(y => `<option value="${y}" ${y === cur ? 'selected' : ''}>${y} 赛季</option>`).join('')}
                        </select>
                        <span class="module-year-hint" id="rc-hint"></span>
                    </div>
                    <div id="rc-body"><div class="schedule-loading"><div>⏳ 正在加载常规赛总结...</div></div></div>
                </div>`;
            await renderRecapContent();
        }

        async function renderRecapContent() {
            const year = $('#rc-year').value;
            const cur = ((typeof FILE_INDEX !== 'undefined' ? FILE_INDEX : {}).currentSeason)
                || String(new Date().getFullYear());
            const body = $('#rc-body');
            const hint = $('#rc-hint');
            body.innerHTML = '<div class="schedule-loading"><div>⏳ 正在加载...</div></div>';

            const tryJson = async paths => {
                for (const p of paths) {
                    try {
                        const r = await fetch(p + '?v=' + Date.now());
                        if (r.ok) return await r.json();
                    } catch (e) { /* try next */ }
                }
                return null;
            };

            const dashPaths = [];
            if (year === cur) dashPaths.push('portal/dashboard-data.json');
            dashPaths.push(`seasons/${year}/snapshots/dashboard-data.json`);
            if (year === cur) dashPaths.push('portal/dashboard-data.json.bak');
            const dash = await tryJson(dashPaths);

            const postPaths = [];
            if (year === cur) postPaths.push('data/postseason.json');
            postPaths.push(`seasons/${year}/snapshots/postseason.json`);
            if (year === cur) postPaths.push('data/postseason.json.bak');
            const post = await tryJson(postPaths);

            if (!dash && !post) {
                body.innerHTML = `<div class="schedule-error"><strong>${year} 赛季总结数据不存在</strong><br>
                    该年份封存时未快照 dashboard/postseason 数据，或赛季尚未开始。</div>`;
                hint.textContent = '';
                return;
            }

            const st = (dash && dash.standings) || {};
            const nlWest = (dash && dash.nlStandings && dash.nlStandings.nlWest) || [];
            const leaders = (post && post.leaders) || {};
            const bracket = (post && post.bracket) || {};
            const weeklyFiles = (((window.FILE_INDEX || {}).weekly) || []).filter(f => String(f.season || '') === String(year));
            const psFiles = (((window.FILE_INDEX || {}).postseason) || []).filter(f => String(f.season || '') === String(year));

            // 赛季总结叙事文档（可选，位于 seasons/YYYY/ 根下）
            const summaryPath = `seasons/${year}/${year}-赛季总结.md`;
            let hasSummary = false;
            try {
                const r = await fetch(summaryPath + '?v=' + Date.now());
                hasSummary = r.ok;
            } catch (e) { /* ignore */ }

            const srcTag = (label, ok) => ok ? label : null;
            hint.textContent = [
                srcTag('战绩数据', !!dash),
                srcTag('季后赛数据', !!post),
            ].filter(Boolean).join(' + ') || '无数据';

            const westRows = nlWest.map(t => `
                <tr style="${t.isDodgers ? 'background:rgba(245,185,66,0.1);' : ''}">
                    <td>${t.divRank}</td>
                    <td><span class="st-team">${t.name}</span>${t.isDodgers ? '<span class="tag tag-green">道奇</span>' : ''}${t.clinch ? '<span class="tag tag-green">' + t.clinch + '</span>' : ''}</td>
                    <td>${t.w}-${t.l}</td>
                    <td>${t.pct}</td>
                    <td>${t.gb}</td>
                    <td class="dc-stats">${t.streak || '-'}</td>
                </tr>`).join('');

            const seedChip = (lg, seed) => {
                const tm = psTeam(bracket, lg, seed);
                if (!tm) return '';
                return `<div class="rc-chip"><span class="ps-seed">#${seed}</span><span>${tm.name}</span><i>${tm.w}-${tm.l}</i></div>`;
            };
            const seedBlock = lg => [1, 2, 3, 4, 5, 6].map(s => seedChip(lg, s)).join('');

            const leaderChip = (r, key, fmt) => r ? `<div class="rc-chip"><span>${r.name}</span><b>${fmt ? fmt(r[key]) : r[key]}</b></div>` : '';
            const leaderBlock = (title, rows) => `
                <div class="dashboard-card">
                    <h3 style="margin-bottom:8px;">${title}</h3>
                    ${rows.join('')}
                </div>`;
            const H = leaders.hitting || {}, P = leaders.pitching || {};
            const hitBlock = leaderBlock('🔥 打击领袖', [
                H.hr && H.hr.length ? `<div class="rc-chip"><span>本垒打</span></div>` : '',
                ...(H.hr || []).map(r => leaderChip(r, 'homeRuns')),
                ...(H.avg || []).map(r => leaderChip(r, 'avg')),
                ...(H.ops || []).map(r => leaderChip(r, 'ops')),
            ].filter(Boolean));
            const pitBlock = leaderBlock('⚾ 投球领袖', [
                ...(P.w || []).map(r => leaderChip(r, 'wins')),
                ...(P.era || []).map(r => leaderChip(r, 'era')),
                ...(P.so || []).map(r => leaderChip(r, 'strikeOuts')),
                ...(P.sv || []).map(r => leaderChip(r, 'saves')),
            ].filter(Boolean));

            const weekItems = weeklyFiles.map(f => `
                <div class="module-file-item" onclick="viewWeeklyArchive('${f.name}')">${f.label}</div>`).join('');
            const psItems = psFiles.map(f => `
                <div class="module-file-item" onclick="viewPsArchive('${f.name}')">${f.label}</div>`).join('');

            const summarySection = hasSummary ? `
                <div class="dashboard-section">
                    <div class="dashboard-section-title">🏆 ${year} 赛季总结 <span class="gh-tag">长篇叙事版 · 轨迹/季后赛/人员流动/展望</span></div>
                    <div class="dashboard-card">
                        <p class="dc-stats" style="margin-bottom:10px;">赛季全程叙事报告：分周轨迹、球队领袖、季后赛逐场、人员流动、数据资产清单与 2027 展望。</p>
                        <button class="btn btn-primary" onclick="viewSeasonSummary('${year}')">📖 阅读 ${year} 赛季总结</button>
                        <button class="btn" onclick="window.open('${summaryPath}', '_blank')">原始 Markdown ↗</button>
                    </div>
                </div>` : '';

            body.innerHTML = `
                ${summarySection}
                <div class="dashboard-section">
                    <div class="dashboard-section-title">📊 ${year} 常规赛最终封存 <span class="gh-tag">162 场完整战绩</span></div>
                    <div class="rc-hero">
                        <div class="dashboard-card"><div class="rc-num">${st.wins != null ? st.wins + '-' + st.losses : '-'}</div><div class="rc-label">最终战绩</div></div>
                        <div class="dashboard-card"><div class="rc-num">${st.pct || '-'}</div><div class="rc-label">胜率</div></div>
                        <div class="dashboard-card"><div class="rc-num">${st.leagueRank ? '国联 #' + st.leagueRank : '-'}</div><div class="rc-label">国联排名</div></div>
                        <div class="dashboard-card"><div class="rc-num">${st.homeRecord || '-'}</div><div class="rc-label">主场</div></div>
                        <div class="dashboard-card"><div class="rc-num">${st.awayRecord || '-'}</div><div class="rc-label">客场</div></div>
                        <div class="dashboard-card"><div class="rc-num">${(st.streak && st.streak.streakCode) || '-'}</div><div class="rc-label">收官连胜</div></div>
                    </div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">🏅 国联西区最终排名</div>
                    <div class="dashboard-card" style="overflow-x:auto;">
                        <table class="st-table compact">
                            <thead><tr><th></th><th>球队</th><th>W-L</th><th>胜率</th><th>GB</th><th>近况</th></tr></thead>
                            <tbody>${westRows || '<tr><td colspan="6" class="dc-stats">无积分榜数据</td></tr>'}</tbody>
                        </table>
                    </div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">🎯 季后赛最终种子 <span class="gh-tag">分区冠军 1-3 · 外卡 4-6</span></div>
                    <div class="rc-leader-grid">
                        <div class="dashboard-card"><h3 style="margin-bottom:8px;">国联</h3>${seedBlock('NL') || '<p class="dc-stats">无种子数据</p>'}</div>
                        <div class="dashboard-card"><h3 style="margin-bottom:8px;">美联</h3>${seedBlock('AL') || '<p class="dc-stats">无种子数据</p>'}</div>
                    </div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">👑 球队领袖 <span class="gh-tag">${year} 常规赛数据</span></div>
                    <div class="rc-leader-grid">${hitBlock}${pitBlock}</div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">📰 周战报全存档 <span class="gh-tag">常规赛 · 点击跳转阅读器</span></div>
                    <div class="dashboard-card">
                        <div class="module-file-list" style="max-height:320px;overflow-y:auto;">${weekItems || '<p class="dc-stats">暂无存档</p>'}</div>
                    </div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">🍂 季后赛战报 <span class="gh-tag">点击跳转阅读器</span></div>
                    <div class="dashboard-card">
                        <div class="module-file-list" style="max-height:240px;overflow-y:auto;">${psItems || '<p class="dc-stats">暂无季后赛战报</p>'}</div>
                    </div>
                </div>
                <div class="data-age">来源：dashboard-data.json（${(dash && dash.generatedAt) || '归档快照'}）+ postseason.json（${(post && post.generatedAt) || '归档快照'}）</div>
            `;
        }

        async function viewSeasonSummary(year) {
            const content = $('#content');
            content.innerHTML = '<div class="schedule-loading"><div>⏳ 正在加载赛季总结...</div></div>';
            try {
                const res = await fetch(`seasons/${year}/${year}-赛季总结.md`);
                if (!res.ok) throw new Error(`无法读取文件 (HTTP ${res.status})`);
                const md = await res.text();
                content.innerHTML = `
                    <div class="dashboard-section">
                        <div class="module-file-item" onclick="renderRecapPage()" style="max-width:220px;">← 返回常规赛总结</div>
                        <div class="dashboard-card" style="margin-top:12px;">
                            <div class="markdown-body">${marked.parse(md)}</div>
                        </div>
                    </div>`;
                window.scrollTo(0, 0);
            } catch (err) {
                content.innerHTML = `
                    <div class="schedule-error">
                        <strong>赛季总结加载失败</strong><br>
                        ${err.message}<br><br>
                        建议通过本地服务器访问（<code>python -m http.server 8080</code>），而不是 file:// 直接打开。
                    </div>`;
            }
        }

        '''

t = t[:start] + NEW + t[end:]
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('recap page patched, index.html len', len(t))
