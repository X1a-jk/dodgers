# -*- coding: utf-8 -*-
"""index.html 补丁：新增「休赛期」导航组 + renderOffseasonPage 转会中心页。
老规矩：唯一锚点 + assert 计数。用法：python _patch-offseason-page.py"""
import shutil, sys, io, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(BASE, 'index.html')
BAK = P + '.bak-pre-offseason'

html = io.open(P, encoding='utf-8').read()
shutil.copy(P, BAK)
print('备份 ->', BAK)

CSS = """
        /* ===== 休赛期转会中心 (os-*) ===== */
        .os-chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0 14px; }
        .os-chip {
            padding: 5px 13px; border-radius: 999px; font-size: 0.8rem; cursor: pointer;
            border: 1px solid var(--border); background: rgba(255,255,255,0.04);
            color: var(--text-muted); transition: all .15s; user-select: none;
        }
        .os-chip:hover { background: rgba(255,255,255,0.09); color: var(--text); }
        .os-chip.on { background: rgba(0,90,156,0.35); color: #fff; border-color: rgba(79,195,247,0.5); font-weight: 600; }
        .os-row {
            display: flex; align-items: flex-start; gap: 12px;
            padding: 10px 14px; border: 1px solid var(--border); border-radius: 10px;
            margin-bottom: 8px; background: rgba(255,255,255,0.02);
        }
        .os-date { font-variant-numeric: tabular-nums; color: var(--text-muted); font-size: 0.78rem; white-space: nowrap; padding-top: 2px; min-width: 62px; }
        .os-badge { font-size: 0.72rem; padding: 2px 9px; border-radius: 999px; white-space: nowrap; font-weight: 600; margin-top: 1px; }
        .os-main { flex: 1; min-width: 0; }
        .os-name { font-weight: 700; font-size: 0.92rem; }
        .os-desc { color: var(--text-muted); font-size: 0.82rem; margin-top: 2px; line-height: 1.5; }
        .os-news { border-left: 3px solid var(--border); padding: 10px 16px; margin-bottom: 10px; background: rgba(255,255,255,0.02); border-radius: 0 10px 10px 0; }
        .os-news.rumor { border-left-color: #fbbf24; }
        .os-news.solid { border-left-color: #4fc3f7; }
        .os-news.official { border-left-color: #22c55e; }
        .os-news-text { font-size: 0.88rem; line-height: 1.6; margin: 4px 0; }
        .os-news-meta { font-size: 0.75rem; color: var(--text-muted); }
        .os-news-meta a { color: #7dd3fc; }
        .os-fa-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
        @media (max-width: 900px) { .os-fa-grid { grid-template-columns: 1fr; } }
        .os-man { display: inline-block; padding: 4px 11px; border-radius: 8px; font-size: 0.8rem; margin: 0 6px 6px 0; border: 1px solid var(--border); background: rgba(255,255,255,0.03); }
        .os-man.add { border-color: rgba(34,197,94,0.5); color: #86efac; }
        .os-man.del { border-color: rgba(239,68,68,0.45); color: #fca5a5; text-decoration: line-through; }
        /* ===== 休赛期转会中心 END ===== */
"""

JS = r"""
        /* ---------- 休赛期转会中心 ---------- */
        const OS_TYPE_COLOR = {
            signed_mlb: '#22c55e', signed_milb: '#4fc3f7', extension: '#a78bfa',
            declared_fa: '#ff9800', trade: '#60a5fa', dfa: '#ef4444',
            released: '#94a3b8', outright: '#fbbf24', selected: '#34d399',
            contract_purchased: '#34d399', other: '#94a3b8'
        };
        let OS_DATA = null;
        let OS_FILTER = 'all';
        let OS_QUERY = '';

        async function renderOffseasonPage() {
            const content = $('#content');
            content.innerHTML = '<div class="schedule-loading"><div>? 正在加载休赛期转会数据...</div></div>';
            let data = null, news = { items: [] };
            try {
                const res = await fetch('data/offseason.json?v=' + Date.now());
                if (!res.ok) throw new Error('无法读取 offseason.json (HTTP ' + res.status + ')');
                data = await res.json();
            } catch (err) {
                content.innerHTML = `
                    <div class="schedule-error">
                        <strong>休赛期数据加载失败</strong><br>
                        ${err.message}<br><br>
                        请先运行抓取脚本：<br>
                        <code>python D:\\baseball\\scripts\\fetch-offseason.py</code>
                    </div>`;
                return;
            }
            try {
                const nr = await fetch('data/offseason-news.json?v=' + Date.now());
                if (nr.ok) news = await nr.json();
            } catch (e) { /* 流言文件可选 */ }
            OS_DATA = data;

            const moves = (data.dodgers && data.dodgers.moves) || [];
            const r40 = (data.dodgers && data.dodgers.roster40) || { count: 0, added: [], removed: [] };
            const lg = ((data.league || {}).signings) || [];
            const fa = data.fa || { pending: [], reSigned: [] };
            const items = (news.items || []).filter(x => x.player !== '示例条目');

            const cnt = t => moves.filter(m => m.type === t).length;
            const signedCnt = moves.filter(m => m.type === 'signed_mlb' || m.type === 'signed_milb' || m.type === 'extension').length;
            const tradeCnt = cnt('trade');

            const gen = ((data.generatedAt || '').replace('T', ' ')).slice(0, 16) || '未知';
            const win = data.window || {};
            const windowTxt = (win.start && win.end) ? `${win.start} ~ ${win.end}` : '';

            const card = (num, label, color) => `
                <div class="dashboard-card" style="text-align:center;padding:14px;">
                    <div style="font-size:1.9rem;font-weight:900;color:${color};">${num}</div>
                    <div class="dc-stats">${label}</div>
                </div>`;

            const chip = (key, label) => `<span class="os-chip${OS_FILTER === key ? ' on' : ''}" onclick="osSetFilter('${key}')">${label}</span>`;

            content.innerHTML = `
                <div class="dashboard-section">
                    <div class="dashboard-section-title">⚾ 冬市总览 <span class="gh-tag">${windowTxt} · 更新于 ${gen}</span></div>
                    <div class="dashboard-grid" style="grid-template-columns:repeat(auto-fit,minmax(140px,1fr));">
                        ${card(signedCnt, '新签约/续约', '#22c55e')}
                        ${card(fa.declaredCount != null ? fa.declaredCount : cnt('declared_fa'), '宣布自由球员', '#ff9800')}
                        ${card(tradeCnt, '交易', '#60a5fa')}
                        ${card((r40.count || 0) + ' / 40', '40 人名单占用', '#4fc3f7')}
                        ${card(items.length, '流言/传闻', '#fbbf24')}
                    </div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">? 转会流水台 <span class="gh-tag">道奇相关全部操作 · 按 typeDesc 分类</span></div>
                    <div class="os-chip-row">
                        ${chip('all', '全部 ' + moves.length)}
                        ${chip('signed_mlb', '大联盟签约 ' + cnt('signed_mlb'))}
                        ${chip('signed_milb', '小联盟签约 ' + cnt('signed_milb'))}
                        ${chip('extension', '续约 ' + cnt('extension'))}
                        ${chip('declared_fa', '宣布FA ' + cnt('declared_fa'))}
                        ${chip('trade', '交易 ' + tradeCnt)}
                        ${chip('other', '其他 ' + moves.filter(m => !['signed_mlb','signed_milb','extension','declared_fa','trade'].includes(m.type)).length)}
                    </div>
                    <div class="module-search" style="margin-bottom:12px;">
                        <input type="text" placeholder="搜索球员姓名..." oninput="osSetQuery(this.value)">
                    </div>
                    <div id="os-feed"></div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">? 全联盟重磅 <span class="gh-tag">大联盟合约签约 + 交易 · 标注原道奇球员</span></div>
                    ${lg.length ? lg.map(s => `
                        <div class="os-row">
                            <span class="os-date">${s.date ? s.date.slice(5) : ''}</span>
                            <span class="os-badge" style="background:${s.kind === 'trade' ? 'rgba(96,165,250,0.15)' : 'rgba(34,197,94,0.15)'};color:${s.kind === 'trade' ? '#93c5fd' : '#86efac'};">${s.kind === 'trade' ? '交易' : '签约'}</span>
                            <div class="os-main">
                                <div class="os-name">${s.name}${s.exDodger ? ' <span class="tag tag-yellow" style="font-size:0.68rem;">原道奇</span>' : ''}</div>
                                <div class="os-desc">${s.fromTeam || ''}${s.kind === 'trade' ? ' → ' : ' → '}${s.toTeam || ''} · ${s.desc || ''}</div>
                            </div>
                        </div>`).join('') : '<p class="dc-stats">本窗口暂无全联盟重磅操作（自由市场刚开启，大合约签约通常要到 11 月中下旬）</p>'}
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">? 自由球员追踪 <span class="gh-tag">合同到期的道奇球员 · v1 仅跟踪宣布FA与回流</span></div>
                    <div class="os-fa-grid">
                        <div class="dashboard-card">
                            <h3 style="margin-bottom:10px;color:#ff9800;">? 待签约 (${fa.pending.length})</h3>
                            ${fa.pending.length ? fa.pending.map(p => `<div class="os-row"><span class="os-date">${p.date ? p.date.slice(5) : ''}</span><div class="os-main"><div class="os-name">${p.name}</div></div></div>`).join('') : '<p class="dc-stats">暂无</p>'}
                        </div>
                        <div class="dashboard-card">
                            <h3 style="margin-bottom:10px;color:#22c55e;">? 已回流 (${fa.reSigned.length})</h3>
                            ${fa.reSigned.length ? fa.reSigned.map(p => `<div class="os-row"><span class="os-date">${p.date ? p.date.slice(5) : ''}</span><div class="os-main"><div class="os-name">${p.name}</div><div class="os-desc">${p.note || ''}</div></div></div>`).join('') : '<p class="dc-stats">暂无（宣布自由球员后与道奇重签会自动进此列）</p>'}
                        </div>
                    </div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">? 流言雷达 <span class="gh-tag">非官方消息 · 官宣后由转会流水台坐实</span></div>
                    ${items.length ? items.map(n => `
                        <div class="os-news ${n.credibility || 'rumor'}">
                            <div class="os-news-meta">${n.date || ''} · ${n.player || ''} · 可信度：${({rumor:'传闻',solid:'较可靠',official:'已官宣'})[n.credibility] || '传闻'}${n.source ? ` · <a href="${n.source}" target="_blank">${n.sourceName || '来源'}</a>` : ''}</div>
                            <div class="os-news-text">${n.text || ''}</div>
                        </div>`).join('') : '<p class="dc-stats">暂无流言。喊助手"搜一下转会流言"即可更新。</p>'}
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">? 40 人名单守望 <span class="gh-tag">当前 ${r40.count || 0} 人 · 对比赛季结束快照</span></div>
                    <div class="dashboard-card">
                        ${(r40.added && r40.added.length) ? `<div style="margin-bottom:10px;"><b style="color:#86efac;font-size:0.85rem;">新增</b><br>${r40.added.map(n => `<span class="os-man add">${n}</span>`).join('')}</div>` : ''}
                        ${(r40.removed && r40.removed.length) ? `<div style="margin-bottom:10px;"><b style="color:#fca5a5;font-size:0.85rem;">移除</b><br>${r40.removed.map(n => `<span class="os-man del">${n}</span>`).join('')}</div>` : ''}
                        <b style="color:var(--text-muted);font-size:0.85rem;">在册名单</b><br>
                        <div style="margin-top:8px;">${(r40.list || []).map(n => `<span class="os-man">${n}</span>`).join('')}</div>
                    </div>
                </div>
            `;
            osRenderFeed();
        }

        function osSetFilter(k) { OS_FILTER = k; document.querySelectorAll('.os-chip').forEach(c => c.classList.remove('on')); event.target.classList.add('on'); osRenderFeed(); }
        function osSetQuery(v) { OS_QUERY = (v || '').trim().toLowerCase(); osRenderFeed(); }

        function osRenderFeed() {
            const el = document.getElementById('os-feed');
            if (!el || !OS_DATA) return;
            let moves = ((OS_DATA.dodgers || {}).moves) || [];
            if (OS_FILTER !== 'all') {
                if (OS_FILTER === 'other') {
                    moves = moves.filter(m => !['signed_mlb','signed_milb','extension','declared_fa','trade'].includes(m.type));
                } else {
                    moves = moves.filter(m => m.type === OS_FILTER);
                }
            }
            if (OS_QUERY) moves = moves.filter(m => (m.name || '').toLowerCase().includes(OS_QUERY));
            el.innerHTML = moves.length ? moves.map(m => `
                <div class="os-row">
                    <span class="os-date">${m.date ? m.date.slice(5) : ''}</span>
                    <span class="os-badge" style="background:${(OS_TYPE_COLOR[m.type] || '#94a3b8') + '22'};color:${OS_TYPE_COLOR[m.type] || '#94a3b8'};">${m.typeCn || m.type}</span>
                    <div class="os-main">
                        <div class="os-name">${m.name}</div>
                        <div class="os-desc">${m.desc || ''}</div>
                    </div>
                </div>`).join('') : '<p class="dc-stats">没有匹配的操作记录</p>';
        }
        /* ---------- 休赛期转会中心 END ---------- */
"""

NAV = """
                <div class="nav-group">
                    <div class="nav-group-title">休赛期</div>
                    <a class="nav-item" data-page="offseason">
                        <span class="nav-icon">⚾</span> 转会中心
                    </a>
                </div>
"""

def patch(anchor, repl, count=1):
    global html
    n = html.count(anchor)
    assert n == count, '锚点计数 %d != %d: %r' % (n, count, anchor[:60])
    html = html.replace(anchor, repl)
    print('  [OK] %r' % anchor.strip()[:50])

# A. 标题映射
patch("                transactions: '交易与人员变动'\n            };",
      "                transactions: '交易与人员变动',\n                offseason: '休赛期转会中心'\n            };")

# B. 路由
patch("""            } else if (page === 'transactions') {
                renderTransactionsPage();
            } else if (page === 'news') {
""",
"""            } else if (page === 'transactions') {
                renderTransactionsPage();
            } else if (page === 'offseason') {
                renderOffseasonPage();
            } else if (page === 'news') {
""")

# C. 导航组（内容组之后、</nav> 之前）
patch("""                </div>
            </nav>
""",
"""                </div>
""" + NAV + """            </nav>
""")

# D. 页面函数（插在 renderTransactionsPage 之前）
patch("        async function renderTransactionsPage() {",
      JS + "\n        async function renderTransactionsPage() {")

# E. CSS（插在 Markdown preview styling 注释之前）
patch("        /* Markdown preview styling */",
      CSS + "\n        /* Markdown preview styling */")

io.open(P, 'w', encoding='utf-8', newline='').write(html)
print('补丁完成，写入 %s (%d bytes)' % (P, len(html.encode('utf-8'))))
