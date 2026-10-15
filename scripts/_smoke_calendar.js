// 冒烟：日历弹窗日报链接（loadGameLocal 用北京时间索引 + FILE_INDEX.folder）
const fs = require('fs');
const html = fs.readFileSync('D:/baseball/index.html', 'utf8');
const m = html.match(/<script[^>]*>([\s\S]*?)<\/script>/g);
let code = '';
for (const block of m) {
  const body = block.replace(/^<script[^>]*>/, '').replace(/<\/script>$/, '');
  if (body.includes('renderPlayoffPage')) code = body;
}
const fileindex = JSON.parse(fs.readFileSync('D:/baseball/portal/file-index.json', 'utf8'));
// 找一个真实比赛日：2026-09-27（美西）-> 北京时间 2026-09-28 的日报
const target = fileindex.daily.find(x => x.date === '2026-09-28');
console.log('[cal] daily entry for 2026-09-28:', JSON.stringify(target));

let capturedHtml = '';
const gmLocal = { set innerHTML(v) { capturedHtml = v; }, get innerHTML() { return capturedHtml; } };
const created = [];
global.document = {
  getElementById: id => (id === 'gm-local' ? gmLocal : (id === 'gm-links' ? { appendChild(b){ created.push(b); } } : null)),
  querySelector: () => null, querySelectorAll: () => [], addEventListener: () => {},
  createElement: () => ({ className: '', textContent: '', href: '', target: '', rel: '', innerHTML: '', onclick: null, style: {} }),
  getElementsByTagName: () => [{ parentNode: { insertBefore(){} } }],
  body: { classList: { add(){} } },
};
global.window = global; global.open = () => {};
global.localStorage = { getItem: () => null, setItem: () => {} };
global.location = { hash: '' };
global.marked = { parse: md => '<p>' + md.slice(0, 40) + '</p>' };
global.FILE_INDEX = fileindex;
global.setPage = () => {}; global.selectFile = () => {}; global.closeGameModal = () => {};
const dailyMd = fs.readFileSync('D:/baseball/seasons/2026/regular/daily/2026-09-28.md', 'utf8');
global.fetch = url => {
  if (url.includes('seasons/2026/regular/daily/2026-09-28.md')) {
    return Promise.resolve({ ok: true, text: () => Promise.resolve(dailyMd) });
  }
  return Promise.resolve({ ok: false, text: () => Promise.resolve('') });
};
(async () => {
  try {
    eval(code);
    console.log('typeof loadGameLocal:', typeof loadGameLocal);
    await loadGameLocal('2026-09-27', '2026-09-28', { date: '2026-09-27', opponent: 'Giants' });
    console.log('[cal] snapshot loaded via folder:', capturedHtml.includes('道奇队40人名单快照'));
    console.log('[cal] no "不存在" note:', !capturedHtml.includes('不存在'));
    const dailyBtn = created.find(b => (b.textContent || '').includes('当日日报'));
    const weeklyBtn = created.find(b => (b.textContent || '').includes('所属周报'));
    console.log('[cal] daily button:', !!dailyBtn, dailyBtn ? dailyBtn.textContent : '');
    console.log('[cal] weekly button kept:', !!weeklyBtn, weeklyBtn ? weeklyBtn.textContent.slice(0, 30) : '');
    console.log('[cal] daily btn onclick wired:', !!(dailyBtn && dailyBtn.onclick));
    console.log('SMOKE_OK');
  } catch (e) { console.error('SMOKE_FAIL:', e.stack || e); process.exit(1); }
})();
