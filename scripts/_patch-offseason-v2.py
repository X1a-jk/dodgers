# -*- coding: utf-8 -*-
"""休赛期转会中心 v2：整段替换 index.html 中 renderOffseasonPage 区块（BEGIN/END 标记之间）。
更细致、全中文：日期分组流水台、中文摘要、休赛期时间轴、40人进度条。"""
import shutil, io, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(BASE, 'index.html')
BAK = P + '.bak-pre-offseason-v2'

html = io.open(P, encoding='utf-8').read()
shutil.copy(P, BAK)

BEGIN = '        /* ---------- 休赛期转会中心 ---------- */'
END = '        /* ---------- 休赛期转会中心 END ---------- */'
i = html.find(BEGIN)
j = html.find(END)
assert i > 0 and j > i, '找不到休赛期标记区块'

NEW = r'''        /* ---------- 休赛期转会中心 ---------- */
        const OS_TYPE_COLOR = {
            signed_mlb: '#22c55e', signed_milb: '#4fc3f7', extension: '#a78bfa',
            declared_fa: '#ff9800', trade: '#60a5fa', dfa: '#ef4444',
            released: '#94a3b8', outright: '#fbbf24', selected: '#34d399',
            contract_purchased: '#34d399', other: '#94a3b8'
        };
        let OS_DATA = null;
        let OS_FILTER = 'all';
        let OS_QUERY = '';

        const OS_WEEK = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
        function osCnDate(d) {
            if (!d) return '';
            const dt = new Date(d + 'T00:00:00');
            if (isNaN(dt)) return d;
            return (dt.getMonth() + 1) + '月' + dt.getDate() + '日 ' + OS_WEEK[dt.getDay()];
        }
        const OS_CRED_CN = { rumor: '传闻', solid: '较可靠', official: '已官宣' };

        // 休赛期关键节点时间轴（每年 10 月底 ~ 次年 2 月）
        const OS_TIMELINE = [
            ['10 月底', '世界大赛落幕，自由球员市场正式开启；球队/球员选项、提前续约谈判启动'],
            ['11 月中', '合格报价（QO）截止；大牌自由球员开始陆续签约'],
            ['12 月初', '薪资仲裁不 Tender 截止，40 人名单大幅瘦身'],
            ['12 月上中', '冬季会议（Winter Meetings）：全年交易最高峰，规则五选秀'],
            ['1 月', '薪资仲裁数字交换截止，大部分仲裁球员提前续约避免开庭'],
            ['2 月中', '投手捕手报到，春训开营，新赛季倒计时'],
        ];

        async function renderOffseasonPage() {
            const content = $('#content');
            content.innerHTML = '<div class="schedule-loading"><div>⏳ 正在加载休赛期转会数据...</div></div>';
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
            const windowTxt = (win.start && win.end) ? `${win.start} 至 ${win.end}` : '';
            const pct40 = Math.round((r40.count || 0) / 40 * 100);

            const card = (num, label, color, sub) => `
                <div class="dashboard-card" style="text-align:center;padding:14px;">
                    <div style="font-size:1.9rem;font-weight:900;color:${color};">${num}</div>
                    <div class="dc-stats">${label}</div>
                    ${sub ? `<div style="font-size:0.72rem;color:var(--text-muted);margin-top:4px;">${sub}</div>` : ''}
                </div>`;

            const chip = (key, label) => `<span class="os-chip${OS_FILTER === key ? ' on' : ''}" onclick="osSetFilter('${key}', this)">${label}</span>`;

            content.innerHTML = `
                <div class="dashboard-section">
                    <div class="dashboard-section-title">🏟️ 冬市总览 <span class="gh-tag">统计窗口：${windowTxt} · 数据更新于 ${gen}</span></div>
                    <div class="dashboard-grid" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr));">
                        ${card(signedCnt, '新签约 / 续约', '#22c55e', '大联盟 ' + cnt('signed_mlb') + ' · 小联盟 ' + cnt('signed_milb'))}
                        ${card(fa.declaredCount != null ? fa.declaredCount : cnt('declared_fa'), '合同到期成为自由球员', '#ff9800', '其中回流 ' + fa.reSigned.length + ' 人')}
                        ${card(tradeCnt, '交易', '#60a5fa', '送出与换回均计入')}
                        ${card((r40.count || 0) + ' / 40', '40 人名单占用', '#4fc3f7', '剩余名额 ' + (40 - (r40.count || 0)))}
                        ${card(items.length, '流言 / 传闻在追', '#fbbf24', '官宣后自动坐实')}
                    </div>
                    <div class="dashboard-card" style="margin-top:14px;">
                        <h3 style="margin-bottom:12px;">📅 休赛期关键节点</h3>
                        <div class="os-timeline">
                            ${OS_TIMELINE.map(([when, what]) => `
                                <div class="os-tl-item">
                                    <span class="os-tl-when">${when}</span>
                                    <span class="os-tl-what">${what}</span>
                                </div>`).join('')}
                        </div>
                    </div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">📋 转会流水台 <span class="gh-tag">道奇全部操作 · 按日期分组 · 中文摘要</span></div>
                    <div class="os-chip-row">
                        ${chip('all', '全部 ' + moves.length)}
                        ${chip('signed_mlb', '大联盟签约 ' + cnt('signed_mlb'))}
                        ${chip('signed_milb', '小联盟签约 ' + cnt('signed_milb'))}
                        ${chip('extension', '续约 ' + cnt('extension'))}
                        ${chip('declared_fa', '成为自由球员 ' + cnt('declared_fa'))}
                        ${chip('trade', '交易 ' + tradeCnt)}
                        ${chip('other', '名单操作 ' + moves.filter(m => !['signed_mlb','signed_milb','extension','declared_fa','trade'].includes(m.type)).length)}
                    </div>
                    <div class="module-search" style="margin-bottom:12px;">
                        <input type="text" placeholder="搜索球员姓名（中文或英文）..." oninput="osSetQuery(this.value)">
                    </div>
                    <div id="os-feed"></div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">🌐 全联盟重磅动向 <span class="gh-tag">其他队的大联盟合约签约与交易 · 与原道奇球员高亮</span></div>
                    ${lg.length ? lg.map(s => `
                        <div class="os-row">
                            <span class="os-date">${s.date ? s.date.slice(5).replace('-', '/') : ''}</span>
                            <span class="os-badge" style="background:${s.kind === 'trade' ? 'rgba(96,165,250,0.15)' : 'rgba(34,197,94,0.15)'};color:${s.kind === 'trade' ? '#93c5fd' : '#86efac'};">${s.kind === 'trade' ? '交易' : '签约'}</span>
                            <div class="os-main">
                                <div class="os-name">${s.name}${s.exDodger ? ' <span class="tag tag-yellow" style="font-size:0.68rem;">原道奇</span>' : ''}${s.posCn ? ` <span style="font-size:0.75rem;color:var(--text-muted);font-weight:400;">${s.posCn}</span>` : ''}</div>
                                <div class="os-desc">${s.cn || s.desc || ''}</div>
                            </div>
                        </div>`).join('') : '<p class="dc-stats">本窗口暂无全联盟重磅操作。自由市场刚开启，大合约签约通常要到 11 月中下旬才会陆续出现。</p>'}
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">🎯 自由球员追踪 <span class="gh-tag">合同到期的道奇球员 · 标注 2026 赛季表现</span></div>
                    <div class="os-fa-grid">
                        <div class="dashboard-card">
                            <h3 style="margin-bottom:10px;color:#ff9800;">🔓 待签约（${fa.pending.length} 人）</h3>
                            ${fa.pending.length ? fa.pending.map(p => `
                                <div class="os-row">
                                    <div class="os-main">
                                        <div class="os-name">${p.name}${p.posCn ? ` <span style="font-size:0.75rem;color:var(--text-muted);font-weight:400;">${p.posCn}</span>` : ''}</div>
                                        <div class="os-desc">${p.stats || '2026 赛季未代表道奇出场'} · ${osCnDate(p.date)} 成为自由球员</div>
                                    </div>
                                </div>`).join('') : '<p class="dc-stats">暂无待签约的自由球员</p>'}
                        </div>
                        <div class="dashboard-card">
                            <h3 style="margin-bottom:10px;color:#22c55e;">🏠 已回流（${fa.reSigned.length} 人）</h3>
                            ${fa.reSigned.length ? fa.reSigned.map(p => `
                                <div class="os-row">
                                    <div class="os-main">
                                        <div class="os-name">${p.name}${p.posCn ? ` <span style="font-size:0.75rem;color:var(--text-muted);font-weight:400;">${p.posCn}</span>` : ''}</div>
                                        <div class="os-desc">${p.note || ''}</div>
                                    </div>
                                </div>`).join('') : '<p class="dc-stats">暂无。宣布自由球员后与道奇重签（大联盟或小联盟合约）会自动移入此列。</p>'}
                        </div>
                    </div>
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">📰 流言雷达 <span class="gh-tag">非官方消息，仅供参考 · 官宣后由转会流水台坐实</span></div>
                    ${items.length ? items.map(n => `
                        <div class="os-news ${n.credibility || 'rumor'}">
                            <div class="os-news-meta">${n.date || ''} · ${n.player || ''} · 可信度：${OS_CRED_CN[n.credibility] || '传闻'}${n.source ? ` · <a href="${n.source}" target="_blank">${n.sourceName || '消息来源'}</a>` : ''}</div>
                            <div class="os-news-text">${n.text || ''}</div>
                        </div>`).join('') : '<p class="dc-stats">暂无在追的流言。想看流言时喊助手「搜一下转会流言」即可更新此板块。</p>'}
                </div>

                <div class="dashboard-section">
                    <div class="dashboard-section-title">👥 40 人名单守望 <span class="gh-tag">对比赛季结束名单 · 每次抓取自动存快照</span></div>
                    <div class="dashboard-card">
                        <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-bottom:6px;">
                            <span>名额占用</span><b>${r40.count || 0} / 40</b>
                        </div>
                        <div class="os-progress"><div class="os-progress-bar" style="width:${pct40}%;"></div></div>
                        <div style="font-size:0.75rem;color:var(--text-muted);margin:8px 0 14px;">剩余 ${40 - (r40.count || 0)} 个名额可用于签约、Rule 5 保护与交易补强</div>
                        ${(r40.added && r40.added.length) ? `<div style="margin-bottom:10px;"><b style="color:#86efac;font-size:0.85rem;">🟢 新增进名单</b><br>${r40.added.map(n => `<span class="os-man add">${n}</span>`).join('')}</div>` : ''}
                        ${(r40.removed && r40.removed.length) ? `<div style="margin-bottom:10px;"><b style="color:#fca5a5;font-size:0.85rem;">🔴 离开名单</b><br>${r40.removed.map(n => `<span class="os-man del">${n}</span>`).join('')}</div>` : ''}
                        <b style="color:var(--text-muted);font-size:0.85rem;">在册球员</b>
                        <div style="margin-top:8px;">${(r40.list || []).map(n => `<span class="os-man">${n}</span>`).join('')}</div>
                    </div>
                </div>
            `;
            osRenderFeed();
        }

        function osSetFilter(k, el) {
            OS_FILTER = k;
            if (el) {
                document.querySelectorAll('.os-chip').forEach(c => c.classList.remove('on'));
                el.classList.add('on');
            }
            osRenderFeed();
        }
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
            if (!moves.length) {
                el.innerHTML = '<p class="dc-stats">没有匹配的操作记录</p>';
                return;
            }
            // 按日期分组渲染
            let out = '', lastDate = null;
            for (const m of moves) {
                if (m.date !== lastDate) {
                    if (lastDate !== null) out += '';
                    out += `<div class="os-date-group">${osCnDate(m.date)}</div>`;
                    lastDate = m.date;
                }
                out += `
                <div class="os-row">
                    <span class="os-badge" style="background:${(OS_TYPE_COLOR[m.type] || '#94a3b8') + '22'};color:${OS_TYPE_COLOR[m.type] || '#94a3b8'};">${m.typeCn || m.type}</span>
                    <div class="os-main">
                        <div class="os-name">${m.name}${m.posCn ? ` <span style="font-size:0.75rem;color:var(--text-muted);font-weight:400;">${m.posCn}</span>` : ''}</div>
                        <div class="os-desc">${m.cn || m.desc || ''}</div>
                    </div>
                </div>`;
            }
            el.innerHTML = out;
        }
'''

CSS_ADD = """
        /* 休赛期 v2 增补 */
        .os-date-group { font-weight: 700; font-size: 0.88rem; color: var(--text); margin: 16px 0 8px; padding-left: 2px; border-left: 3px solid var(--dodgers-blue); padding-left: 10px; }
        .os-timeline { display: flex; flex-direction: column; gap: 0; }
        .os-tl-item { display: flex; gap: 14px; padding: 8px 0; border-bottom: 1px dashed var(--border); align-items: baseline; }
        .os-tl-item:last-child { border-bottom: none; }
        .os-tl-when { min-width: 76px; font-weight: 700; color: #4fc3f7; font-size: 0.85rem; white-space: nowrap; }
        .os-tl-what { color: var(--text-muted); font-size: 0.84rem; line-height: 1.55; }
        .os-progress { height: 10px; border-radius: 999px; background: rgba(255,255,255,0.07); overflow: hidden; }
        .os-progress-bar { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #1e88e5, #4fc3f7); transition: width .4s; }
"""

# 替换 JS 区块
old_block = html[i:j]
html = html[:i] + NEW + html[j:]
print('  [OK] JS 区块替换（%d -> %d 字符）' % (len(old_block), len(NEW)))

# 增补 CSS（插在旧休赛期 CSS 的 END 标记后）
CSS_ANCHOR = '        /* ===== 休赛期转会中心 END ===== */'
assert html.count(CSS_ANCHOR) == 1
html = html.replace(CSS_ANCHOR, CSS_ANCHOR + '\n' + CSS_ADD)
print('  [OK] CSS 增补')

io.open(P, 'w', encoding='utf-8', newline='').write(html)
print('写入 %s (%d bytes)' % (P, len(html.encode('utf-8'))))
