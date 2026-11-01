// 冒烟：年份选择器
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
const elStub = () => ({ textContent: '', innerHTML: '', disabled: false, onclick: null, value: '', style: {}, dataset: {}, classList: { toggle(){}, add(){} } });
global.$ = sel => (sel === '#content' ? contentStub : elStub(sel));
global.$$ = () => [];
global.document = {
  getElementById: () => null, querySelector: sel => (sel === '#content' ? contentStub : elStub(sel)),
  querySelectorAll: () => [], addEventListener: () => {},
  createElement: () => ({ style: {}, classList: { add(){}, toggle(){} }, appendChild(){}, setAttribute(){}, parentNode: { insertBefore(){} } }),
  getElementsByTagName: () => [{ parentNode: { insertBefore(){} } }],
  body: { classList: { add(){} } }, activeElement: null,
};
global.window = global; global.open = () => {};
global.localStorage = { getItem: () => null, setItem: () => {} };
global.location = { hash: '' };
const fileindex = JSON.parse(fs.readFileSync('D:/baseball/portal/file-index.json', 'utf8'));
global.fetch = url => Promise.resolve({ ok: true, json: () => Promise.resolve(fileindex), text: () => Promise.resolve('') });
global.refreshFileIndex = () => Promise.resolve(); global.setPage = () => {}; global.selectFile = () => {};
global.FILE_INDEX = fileindex;
(async () => {
  try {
    eval(code);
    renderModule('weekly');
    console.log('[year] years in index:', JSON.stringify(fileindex.years));
    console.log('[year] selector has 2026:', captured.includes('2026 赛季'));
    console.log('[year] items have data-season:', (captured.match(/data-season="2026"/g) || []).length, 'items');
    console.log('[year] hint shows count:', captured.includes('共 15 份'));
    renderModule('daily');
    console.log('[year] daily selector:', captured.includes('全部年份'));
    renderModule('postseason');
    console.log('[year] postseason module renders:', captured.includes('季后赛战报'));
    console.log('SMOKE_OK');
  } catch (e) { console.error('SMOKE_FAIL:', e.stack || e); process.exit(1); }
})();
