# -*- coding: utf-8 -*-
"""门户季后赛改造补丁：十月主题 + 季后赛对阵页 + 常规赛总结页"""
import io, sys

sys.stdout.reconfigure(encoding='utf-8')
P = r'D:\baseball\index.html'
t = io.open(P, encoding='utf-8').read()
orig_len = len(t)

NEW_CSS = r'''
        /* ===== 十月季后赛主题（postseason.json 公布或进入 10 月自动启用） ===== */
        body.october {
            background: radial-gradient(1200px 500px at 85% -10%, rgba(245, 185, 66, 0.07), transparent),
                        linear-gradient(180deg, #0b0e1a 0%, #0f172a 100%);
        }
        body.october .sidebar {
            background: linear-gradient(180deg, #171106 0%, #0a0a12 60%);
            border-right: 1px solid rgba(245, 185, 66, 0.22);
        }
        body.october .logo {
            background: linear-gradient(135deg, #f5b942 0%, #b8860b 100%);
            color: #1a1205;
        }
        body.october .nav-item.active {
            background: linear-gradient(90deg, rgba(245, 185, 66, 0.18) 0%, rgba(184, 134, 11, 0.08) 100%);
            border-left-color: #f5b942;
        }
        body.october .nav-item:hover { background: rgba(245, 185, 66, 0.07); }
        .october-banner {
            margin: 10px 14px 4px;
            padding: 9px 12px;
            border-radius: 12px;
            background: linear-gradient(90deg, rgba(245, 185, 66, 0.18), rgba(184, 134, 11, 0.1));
            border: 1px solid rgba(245, 185, 66, 0.35);
            font-size: 12px;
        }
        .october-banner b { color: #f5b942; display: block; font-size: 12.5px; letter-spacing: 1px; }
        .october-banner span { color: var(--text-muted); }

        /* ===== 季后赛对阵图 ===== */
        .ps-banner {
            border-radius: var(--radius);
            padding: 18px 20px;
            margin-bottom: 18px;
            background: linear-gradient(90deg, rgba(245,185,66,0.16), rgba(0,90,156,0.28));
            border: 1px solid rgba(245,185,66,0.4);
        }
        .ps-banner h2 { color: #f5b942; margin-bottom: 4px; font-size: 1.25rem; }
        .ps-banner p { color: var(--text); margin: 2px 0; }
        .ps-note {
            border-radius: 12px; padding: 10px 14px; margin-bottom: 16px;
            background: rgba(79,195,247,0.08); border: 1px solid rgba(79,195,247,0.3);
            color: var(--text-muted); font-size: 0.85rem;
        }
        .ps-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
        @media (max-width: 900px) { .ps-grid { grid-template-columns: 1fr; } }
        .ps-league {
            background: var(--panel); border: 1px solid var(--border);
            border-radius: var(--radius); padding: 14px;
        }
        .ps-league-head {
            font-weight: 800; font-size: 1.05rem; margin-bottom: 10px;
            color: #f5b942; letter-spacing: 1px;
        }
        .ps-round-label {
            font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;
            letter-spacing: 1.5px; margin: 12px 0 6px;
        }
        .ps-series {
            background: rgba(15, 23, 42, 0.6); border: 1px solid var(--border);
            border-radius: 12px; padding: 10px 12px; margin-bottom: 10px;
        }
        .ps-series-head {
            display: flex; justify-content: space-between; font-size: 0.8rem;
            color: var(--text-muted); margin-bottom: 8px;
        }
        .ps-bo { color: #f5b942; }
        .ps-team {
            display: flex; align-items: center; gap: 8px;
            padding: 6px 8px; border-radius: 8px; font-size: 0.92rem;
        }
        .ps-team + .ps-team { margin-top: 2px; }
        .ps-team.ps-lad { background: rgba(245,185,66,0.12); border: 1px solid rgba(245,185,66,0.35); }
        .ps-team.ps-tbd { color: var(--text-muted); font-style: italic; }
        .ps-seed { color: #f5b942; font-weight: 700; width: 26px; font-size: 0.82rem; }
        .ps-name { font-weight: 600; flex: 1; }
        .ps-rec { color: var(--text-muted); font-size: 0.78rem; }
        .ps-wins { font-weight: 800; font-size: 1.05rem; color: var(--text); width: 20px; text-align: right; }
        .ps-dots { display: flex; gap: 5px; margin: 8px 2px 2px; flex-wrap: wrap; }
        .ps-dot {
            min-width: 22px; height: 22px; border-radius: 50%;
            display: inline-flex; align-items: center; justify-content: center;
            font-size: 0.68rem; font-weight: 700;
        }
        .ps-dot-w { background: rgba(34,197,94,0.25); color: #86efac; border: 1px solid rgba(34,197,94,0.5); }
        .ps-dot-l { background: rgba(239,68,68,0.2); color: #fca5a5; border: 1px solid rgba(239,68,68,0.45); }
        .ps-dot-n { background: rgba(148,163,184,0.15); color: var(--text-muted); border: 1px solid var(--border); }
        .ps-dot-soon { background: rgba(79,195,247,0.1); color: var(--text-muted); border: 1px dashed rgba(79,195,247,0.4); }
        .ps-series-foot { font-size: 0.76rem; color: var(--text-muted); margin-top: 6px; }
        .ps-ws { margin-top: 16px; }
        .ps-ws .ps-series { border-color: rgba(245,185,66,0.45); background: linear-gradient(90deg, rgba(245,185,66,0.06), rgba(15,23,42,0.6)); }

        /* ===== 常规赛总结 ===== */
        .rc-hero { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-bottom: 16px; }
        .rc-hero .dashboard-card { text-align: center; padding: 16px 10px; }
        .rc-hero .rc-num { font-size: 1.7rem; font-weight: 900; color: #f5b942; }
        .rc-hero .rc-label { font-size: 0.78rem; color: var(--text-muted); margin-top: 2px; }
        .rc-leader-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
        @media (max-width: 900px) { .rc-leader-grid { grid-template-columns: 1fr; } }
        .rc-chip {
            display: flex; align-items: center; gap: 8px; padding: 7px 10px;
            border-radius: 9px; background: rgba(15,23,42,0.55);
            border: 1px solid var(--border); font-size: 0.86rem; margin-bottom: 6px;
        }
        .rc-chip b { color: #f5b942; min-width: 34px; text-align: right; }
        .rc-chip span { flex: 1; }
        .rc-chip i { color: var(--text-muted); font-style: normal; font-size: 0.78rem; }
'''

NEW_JS = r'''
        /* ---------- 季后赛对阵追踪（金色十月） ---------- */
        async function fetchJsonWithBak(url, bakUrl) {
            try {
                const res = await fetch(url + '?v=' + Date.now());
                if (res.ok) return { data: await res.json(), source: 'current' };
                throw new Error('http ' + res.status);
            } catch (e) {
                if (bakUrl) {
                    try {
                        const bak = await fetch(bakUrl);
                        if (bak.ok) return { data: await bak.json(), source: 'backup' };
                    } catch (e2) { /* ignore */ }
                }
                return { data: null, source: 'none' };
            }
        }

        function psTeam(bracket, league, seed) {
            const lg = bracket && bracket[league];
            return lg && lg.teams ? lg.teams[String(seed)] : null;
        }

        function psFindTeam(bracket, league, id) {
            const teams = ((bracket || {})[league] || {}).teams || {};
            for (const k of Object.keys(teams)) if (teams[k].id === id) return teams[k];
            return null;
        }

        function psWinnerId(series, bestOf) {
            if (!series || !series.wins) return null;
            const need = Math.floor(bestOf / 2) + 1;
            for (const tid of Object.keys(series.wins)) {
                if (series.wins[tid] >= need) return parseInt(tid);
            }
            return null;
        }

        function psRow(t, wins, placeholder) {
            if (!t) return `<div class="ps-team ps-tbd"><span class="ps-seed">·</span><span class="ps-name">${placeholder}</span><span class="ps-wins"></span></div>`;
            const isLad = t.id === 119;
            return `<div class="ps-team ${isLad ? 'ps-lad' : ''}">
                <span class="ps-seed">${t.seed ? '#' + t.seed : ''}</span>
                <span class="ps-name">${t.abbr || t.name}${isLad ? ' 🐻' : ''}</span>
                <span class="ps-rec">${t.w != null ? t.w + '-' + t.l : ''}</span>
                <span class="ps-wins">${wins != null ? wins : ''}</span>
            </div>`;
        }

        function psDots(series) {
            if (!series || !series.games || !series.games.length) return '';
            const dots = series.games.map(g => {
                if (!g.final) return `<span class="ps-dot ps-dot-soon" title="G${g.gameNumber} · ${g.beijing || '时间待定'} (北京时间) 未赛">·</span>`;
                const ladSide = g.away.id === 119 ? 'away' : (g.home.id === 119 ? 'home' : null);
                let cls = 'ps-dot', mark;
                if (ladSide) {
                    const won = ladSide === g.winnerSide;
                    mark = won ? 'W' : 'L';
                    cls += won ? ' ps-dot-w' : ' ps-dot-l';
                } else {
                    const w = g.winnerSide === 'away' ? g.away : g.home;
                    mark = (w.abbr || (w.name || '?')).slice(0, 3);
                    cls += ' ps-dot-n';
                }
                return `<span class="${cls}" title="G${g.gameNumber} ${g.away.name} ${g.away.score != null ? g.away.score : '-'} : ${g.home.score != null ? g.home.score : '-'} ${g.home.name}">${mark}</span>`;
            }).join('');
            return `<div class="ps-dots">${dots}</div>`;
        }

        function psCard(title, bestOf, rowsHtml, series, fallbackNote) {
            const played = series ? (series.gamesPlayed || 0) : 0;
            const next = series ? (series.games || []).find(g => !g.final) : null;
            let foot = fallbackNote || '';
            if (series) {
                if (next) foot = `G${next.gameNumber} · ${next.beijing || '时间待定'}（北京时间）`;
                else if (played) foot = '系列赛结束';
            }
            return `<div class="ps-series">
                <div class="ps-series-head"><span>${title}</span><span class="ps-bo">${bestOf} 战 ${Math.floor(bestOf / 2) + 1} 胜</span></div>
                ${rowsHtml}
                ${psDots(series)}
                <div class="ps-series-foot">${foot}</div>
            </div>`;
        }

        function psSeriesRows(series, teamA, teamB, phA, phB) {
            const w = tid => (series && series.wins && tid != null) ? (series.wins[tid] || 0) : null;
            return psRow(teamA, teamA ? w(teamA.id) : null, phA) + psRow(teamB, teamB ? w(teamB.id) : null, phB);
        }

        function psLeagueHtml(lg, bracket, rounds) {
            const R = ((rounds || {})[lg]) || {};
            const wc = R.wc || [null, null];
            const ds = R.ds || [null, null];
            const w3v6 = psWinnerId(wc[0], 3), w4v5 = psWinnerId(wc[1], 3);
            const wdsA = psWinnerId(ds[0], 5), wdsB = psWinnerId(ds[1], 5);
            const t3v6 = w3v6 ? psFindTeam(bracket, lg, w3v6) : null;
            const t4v5 = w4v5 ? psFindTeam(bracket, lg, w4v5) : null;
            const tdsA = wdsA ? psFindTeam(bracket, lg, wdsA) : null;
            const tdsB = wdsB ? psFindTeam(bracket, lg, wdsB) : null;
            const name = (bracket[lg] && bracket[lg].name) || lg;
            return `<div class="ps-league">
                <div class="ps-league-head">${name} · ${lg}</div>
                <div class="ps-round-label">外卡轮</div>
                ${psCard('外卡系列赛 A', 3, psSeriesRows(wc[0], psTeam(bracket, lg, 3), psTeam(bracket, lg, 6), '', ''), wc[0], '外卡轮待开赛')}
                ${psCard('外卡系列赛 B', 3, psSeriesRows(wc[1], psTeam(bracket, lg, 4), psTeam(bracket, lg, 5), '', ''), wc[1], '外卡轮待开赛')}
                <div class="ps-round-label">分区系列赛</div>
                ${psCard('分区系列赛 A', 5, psSeriesRows(ds[0], psTeam(bracket, lg, 1), t3v6, '', '#3/#6 胜者'), ds[0], '等待外卡结果')}
                ${psCard('分区系列赛 B', 5, psSeriesRows(ds[1], psTeam(bracket, lg, 2), t4v5, '', '#4/#5 胜者'), ds[1], '等待外卡结果')}
                <div class="ps-round-label">联盟冠军赛</div>
                ${psCard('联盟冠军赛', 7, psSeriesRows(R.cs || null, tdsA, tdsB, '分区赛 A 胜者', '分区赛 B 胜者'), R.cs || null, '等待分区赛结果')}
            </div>`;
        }

        async function renderPlayoffPage() {
            const content = $('#content');
            content.innerHTML = '<div class="schedule-loading"><div>⏳ 正在加载季后赛对阵...</div></div>';

            const { data, source } = await fetchJsonWithBak('data/postseason.json', 'data/postseason.json.bak');
            if (!data || !data.bracket) {
                content.innerHTML = `<div class="schedule-error"><strong>季后赛数据加载失败</strong><br>
                    请手动执行：<code>python D:\\baseball\\scripts\\fetch-postseason.py</code></div>`;
                return;
            }

            const generated = data.generatedAt ? new Date(data.generatedAt).toLocaleString('zh-CN') : '未知';
            const sourceBadge = source === 'backup' ? '<span class="tag tag-red">本地 checkpoint</span>' : '';
            const dod = data.dodgers || {};
            const published = !!data.postseasonPublished;
            const rounds = data.rounds || {};

            const nlWc0 = ((rounds.NL || {}).wc || [])[0], nlWc1 = ((rounds.NL || {}).wc || [])[1];
            const oppW = psWinnerId(nlWc0, 3), oppX = psWinnerId(nlWc1, 3);
            const ladDs = ((rounds.NL || {}).ds || [])[1];
            let ladNote = '轮空 → 分区系列赛（10/03 主场开打）';
            if (ladDs) {
                const next = (ladDs.games || []).find(g => !g.final);
                ladNote = next ? `分区系列赛进行中 · G${next.gameNumber} ${next.beijing || ''}（北京时间）`
                               : (ladDs.gamesPlayed ? '分区系列赛结束' : ladNote);
            } else if (oppW || oppX) {
                const t = oppW ? psFindTeam(data.bracket, 'NL', oppW) : (oppX ? psFindTeam(data.bracket, 'NL', oppX) : null);
                if (t) ladNote = `分区系列赛对手确定：${t.name}（${t.w}-${t.l}）`;
            }

            const ws = rounds.ws || null;
            const wsA = psWinnerId(((rounds.NL || {}).cs || null), 7);
            const wsB = psWinnerId(((rounds.AL || {}).cs || null), 7);
            const wsTeamA = wsA ? psFindTeam(data.bracket, 'NL', wsA) : null;
            const wsTeamB = wsB ? psFindTeam(data.bracket, 'AL', wsB) : null;

            content.innerHTML = `
                <div class="ps-banner">
                    <h2>🍂 OCTOBER BASEBALL · ${data.season} 季后赛对阵</h2>
                    <p><b style="color:#f5b942;">#${dod.seed} 道奇（${dod.record}）</b> — ${ladNote}</p>
                    <p style="color:var(--text-muted);font-size:0.85rem;">${dod.status || ''} · 数据时间 ${generated} ${sourceBadge}</p>
                </div>
                ${published ? '' : `<div class="ps-note">📋 MLB 尚未放出季后赛详细赛程（外卡轮预计 10/01 前后开打）。对阵树已按最终排名锁定，每日 12:00 自动刷新，赛程公布后此处自动显示比分与状态。</div>`}
                <div class="ps-grid">
                    ${psLeagueHtml('NL', data.bracket, rounds)}
                    ${psLeagueHtml('AL', data.bracket, rounds)}
                </div>
                <div class="ps-ws">
                    <div class="ps-round-label" style="margin-top:4px;">世界大赛 · WORLD SERIES</div>
                    ${psCard('世界大赛', 7, psSeriesRows(ws, wsTeamA, wsTeamB, '国联冠军', '美联冠军'), ws, '等待联盟冠军赛结果')}
                </div>
                <div class="data-age">数据时间：${generated} · 来源：MLB Stats API（standings + postseason schedule） ${sourceBadge}</div>
            `;
        }

        /* ---------- 常规赛总结（162 场封存） ---------- */
        function viewWeeklyArchive(name) {
            setPage('weekly');
            setTimeout(() => { try { selectFile('weekly', name); } catch (e) { } }, 400);
        }

        async function renderRecapPage() {
            const content = $('#content');
            content.innerHTML = '<div class="schedule-loading"><div>⏳ 正在加载常规赛总结...</div></div>';

            const [{ data: dash, source: dsrc }, { data: post, source: psrc }] = await Promise.all([
                fetchJsonWithBak('portal/dashboard-data.json', 'portal/dashboard-data.json.bak'),
                fetchJsonWithBak('data/postseason.json', 'data/postseason.json.bak')
            ]);
            if (!dash && !post) {
                content.innerHTML = '<div class="schedule-error"><strong>常规赛数据加载失败</strong><br>请先运行每日管线。</div>';
                return;
            }

            const st = (dash && dash.standings) || {};
            const nlWest = (dash && dash.nlStandings && dash.nlStandings.nlWest) || [];
            const leaders = (post && post.leaders) || {};
            const bracket = (post && post.bracket) || {};
            const weeklyFiles = ((window.FILE_INDEX || {}).weekly) || [];

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

            content.innerHTML = `
                <div class="dashboard-section">
                    <div class="dashboard-section-title">🏁 2026 常规赛最终封存 <span class="gh-tag">162 场完整战绩</span></div>
                    <div class="rc-hero">
                        <div class="dashboard-card"><div class="rc-num">${st.wins != null ? st.wins + '-' + st.losses : '-'}</div><div class="rc-label">最终战绩</div></div>
                        <div class="dashboard-card"><div class="rc-num">${st.pct || '-'}</div><div class="rc-label">胜率</div></div>
                        <div class="dashboard-card"><div class="rc-num">${st.leagueRank ? '国联 #' + st.leagueRank : '-'}</div><div class="rc-label">国联排名（2 号种子）</div></div>
                        <div class="dashboard-card"><div class="rc-num">${st.homeRecord || '-'}</div><div class="rc-label">主场</div></div>
                        <div class="dashboard-card"><div class="rc-num">${st.awayRecord || '-'}</div><div class="rc-label">客场</div></div>
                        <div class="dashboard-card"><div class="rc-num">${(st.streak && st.streak.streakCode) || '-'}</div><div class="rc-label">收官连胜</div></div>
                    </div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">📊 国联西区最终排名</div>
                    <div class="dashboard-card" style="overflow-x:auto;">
                        <table class="st-table compact">
                            <thead><tr><th></th><th>球队</th><th>W-L</th><th>胜率</th><th>GB</th><th>近况</th></tr></thead>
                            <tbody>${westRows}</tbody>
                        </table>
                    </div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">🎟️ 季后赛最终种子 <span class="gh-tag">分区冠军 1-3 · 外卡 4-6</span></div>
                    <div class="rc-leader-grid">
                        <div class="dashboard-card"><h3 style="margin-bottom:8px;">国联</h3>${seedBlock('NL') || '<p class="dc-stats">数据加载中...</p>'}</div>
                        <div class="dashboard-card"><h3 style="margin-bottom:8px;">美联</h3>${seedBlock('AL') || '<p class="dc-stats">数据加载中...</p>'}</div>
                    </div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">👑 球队领袖 <span class="gh-tag">2026 常规赛数据</span></div>
                    <div class="rc-leader-grid">${hitBlock}${pitBlock}</div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">📚 周战报全存档 <span class="gh-tag">点击跳转到周报阅读器</span></div>
                    <div class="dashboard-card">
                        <div class="module-file-list" style="max-height:320px;overflow-y:auto;">${weekItems || '<p class="dc-stats">暂无存档</p>'}</div>
                    </div>
                </div>
                <div class="data-age">来源：dashboard-data.json（${(dash && dash.generatedAt) || '?'}）+ postseason.json（${(post && post.generatedAt) || '?'}）</div>
            `;
        }

        /* ---------- 十月主题：赛程公布或进入 10 月自动启用 ---------- */
        async function applyOctoberTheme() {
            try {
                let oct = new Date().getMonth() === 9;
                try {
                    const res = await fetch('data/postseason.json?v=' + Date.now());
                    if (res.ok) {
                        const d = await res.json();
                        if (d.postseasonPublished) oct = true;
                    }
                } catch (e) { /* 文件不存在则仅按日期判断 */ }
                if (oct) {
                    document.body.classList.add('october');
                    const banner = $('#october-banner');
                    if (banner) banner.style.display = '';
                }
            } catch (e) { /* 主题失败不影响功能 */ }
        }

        async function refreshPlayoff() {
            await renderPlayoffPage();
        }
'''

def rep(old, new, count=1):
    global t
    n = t.count(old)
    assert n == count, f'anchor found {n}x (expect {count}): {old[:70]!r}'
    t = t.replace(old, new, count)
    print(f'ok: {old.strip()[:60]!r}')

# 1. CSS
css_end = t.find('</style>')
assert css_end > 0
t = t[:css_end] + NEW_CSS + '\n        ' + t[css_end:]
print('ok: CSS inserted')

# 2. 侧栏十月横幅
rep('''            </div>
            <nav>''',
'''            </div>
            <div class="october-banner" id="october-banner" style="display:none;">🍂 <b>OCTOBER BASEBALL</b><span>季后赛模式 · 金色十月</span></div>
            <nav>''')

# 3. 导航：季后赛页后加常规赛总结；内容组改名存档
rep('''                    <a class="nav-item" data-page="playoff">
                        <span class="nav-icon">🏆</span> 季后赛
                    </a>''',
'''                    <a class="nav-item" data-page="playoff">
                        <span class="nav-icon">🍂</span> 季后赛对阵
                    </a>
                    <a class="nav-item" data-page="recap">
                        <span class="nav-icon">🏁</span> 常规赛总结
                    </a>''')
rep('<div class="nav-group-title">内容</div>',
    '<div class="nav-group-title">内容 · 常规赛存档</div>')

# 4. 标题映射
rep("                playoff: '季后赛模拟器',",
    "                playoff: '季后赛对阵',\n                recap: '常规赛总结',")

# 5. 路由
rep('''            } else if (page === 'playoff') {
                renderPlayoffPage();
            } else if (page === 'depth') {''',
'''            } else if (page === 'playoff') {
                renderPlayoffPage();
            } else if (page === 'recap') {
                renderRecapPage();
            } else if (page === 'depth') {''')

# 6. 顶部刷新按钮
rep('refreshPlayoff()">🔄 刷新模拟器', 'refreshPlayoff()">🔄 刷新对阵数据')

# 7. 替换 renderPlayoffPage 整段（含 refreshPlayoff）
start = t.find('        /* ---------- 季后赛模拟器 ---------- */')
assert start > 0
end_anchor = '''        async function refreshPlayoff() {
            await renderPlayoffPage();
        }'''
end = t.find(end_anchor)
assert end > start
t = t[:start] + NEW_JS + t[end + len(end_anchor):]
print('ok: renderPlayoffPage replaced')

# 8. 命令面板
rep("            { id: 'playoff',       label: '季后赛模拟器',   icon: '🏟️' },",
    "            { id: 'playoff',       label: '季后赛对阵',     icon: '🍂' },\n            { id: 'recap',        label: '常规赛总结',     icon: '🏁' },")

# 9. 初始化挂主题
rep("        refreshFileIndex().finally(() => setPage('dashboard'));",
    "        applyOctoberTheme();\n        refreshFileIndex().finally(() => setPage('dashboard'));")

io.open(P, 'w', encoding='utf-8').write(t)
print(f'done: {orig_len} -> {len(t)} bytes')
