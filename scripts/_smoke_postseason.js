// 冒烟测试：桩掉 DOM/浏览器 API，执行 index.html 内嵌脚本并调用新页面渲染函数
const fs = require('fs');
const html = fs.readFileSync('D:/baseball/index.html', 'utf8');
const m = html.match(/<script[^>]*>([\s\S]*?)<\/script>/g);
let code = '';
for (const block of m) {
  const body = block.replace(/^<script[^>]*>/, '').replace(/<\/script>$/, '');
  if (body.includes('renderPlayoffPage')) code = body;
}

let captured = '';
const contentStub = { set innerHTML(v) { captured = v; }, get innerHTML() { return captured; } };
let rcCaptured = '';
const rcBodyStub = { set innerHTML(v) { rcCaptured = v; }, get innerHTML() { return rcCaptured; } };

// recap 页 v2：renderRecapPage 出壳到 #content，正文进 #rc-body，年份读 #rc-year
//（对齐历年阵容页 sr-year 的桩法）
global.$ = sel => (sel === '#content' ? contentStub
  : sel === '#rc-year' ? { value: '2026' }
  : sel === '#rc-body' ? rcBodyStub
  : sel === '#rc-hint' ? { textContent: '' }
  : null);
global.$$ = () => [];
global.document = {
  getElementById: () => null,
  querySelector: sel => (sel === '#content' ? contentStub
    : sel === '#rc-year' ? { value: '2026' }
    : sel === '#rc-body' ? rcBodyStub
    : sel === '#rc-hint' ? { textContent: '' }
    : null),
  querySelectorAll: () => [],
  addEventListener: () => {},
  createElement: () => ({ style: {}, classList: { add(){}, toggle(){} }, appendChild(){}, setAttribute(){}, parentNode: { insertBefore(){} } }),
  getElementsByTagName: () => [{ parentNode: { insertBefore(){} } }],
  body: { classList: { add(){} } },
  activeElement: null,
};
global.window = global;
global.open = () => {};
global.localStorage = { getItem: () => null, setItem: () => {} };
global.location = { hash: '' };

const postseason = JSON.parse(fs.readFileSync('D:/baseball/data/postseason.json', 'utf8'));
const dashboard = JSON.parse(fs.readFileSync('D:/baseball/portal/dashboard-data.json', 'utf8'));
const fileindex = JSON.parse(fs.readFileSync('D:/baseball/portal/file-index.json', 'utf8'));

global.fetch = url => Promise.resolve({ ok: true, json: () => {
  if (url.includes('postseason')) return Promise.resolve(postseason);
  if (url.includes('dashboard')) return Promise.resolve(dashboard);
  if (url.includes('file-index')) return Promise.resolve(fileindex);
  return Promise.resolve({});
}, text: () => Promise.resolve('') });

global.refreshFileIndex = () => Promise.resolve();
global.setPage = () => {};
global.selectFile = () => {};
global.FILE_INDEX = fileindex;

(async () => {
  try {
    eval(code);
    await renderPlayoffPage();
    const ps = captured;
    console.log('[playoff] rendered length:', ps.length);
    console.log('[playoff] has NL league card:', ps.includes('国联 · NL'));
    console.log('[playoff] has Brewers:', ps.includes('MIL'));
    console.log('[playoff] has Dodgers row:', ps.includes('ps-lad'));
    console.log('[playoff] has unpublished note:', ps.includes('尚未放出季后赛详细赛程'));
    console.log('[playoff] has WS card:', ps.includes('世界大赛'));
    await renderRecapPage();
    const rcShell = captured;
    console.log('[recap] shell has year select:', rcShell.includes('rc-year'));
    console.log('[recap] shell has rc-body:', rcShell.includes('rc-body'));
    const rc = rcCaptured;
    console.log('[recap] rendered length:', rc.length);
    console.log('[recap] has 100-62:', rc.includes('100-62'));
    console.log('[recap] has Ohtani HR leader:', rc.includes('Shohei Ohtani'));
    console.log('[recap] has weekly archive:', rc.includes('Week 26'));
    console.log('[recap] has ps archive:', rc.includes('NLCS'));
    console.log('[recap] has seed chips:', rc.includes('#4') && rc.includes('San Diego Padres'));
    console.log('[recap] has season-summary entry:', rc.includes('赛季总结') && rc.includes('viewSeasonSummary'));
    console.log('SMOKE_OK');
  } catch (e) {
    console.error('SMOKE_FAIL:', e.stack || e);
    process.exit(1);
  }
})();
