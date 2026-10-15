// 冒烟：历年阵容页 + 球员报告版本切换
const fs = require('fs');
const html = fs.readFileSync('D:/baseball/index.html', 'utf8');
const m = html.match(/<script[^>]*>([\s\S]*?)<\/script>/g);
let code = '';
for (const block of m) {
  const body = block.replace(/^<script[^>]*>/, '').replace(/<\/script>$/, '');
  if (body.includes('renderPlayoffPage')) code = body;
}
let captured = '';
let bodyCaptured = '';
let hintCaptured = '';
const contentStub = { set innerHTML(v) { captured = v; }, get innerHTML() { return captured; } };
const bodyStub = { set innerHTML(v) { bodyCaptured = v; }, get innerHTML() { return bodyCaptured; } };
const hintStub = { set textContent(v) { hintCaptured = v; }, get textContent() { return hintCaptured; } };
const elStub = () => ({ textContent: '', innerHTML: '', disabled: false, onclick: null, value: '2026', style: {}, dataset: {}, classList: { toggle(){}, add(){} } });
global.$ = sel => (sel === '#content' ? contentStub
  : sel === '#sr-year' ? { value: '2026' }
  : sel === '#sr-body' ? bodyStub
  : sel === '#sr-hint' ? hintStub
  : elStub());
global.$$ = () => [];
global.document = {
  getElementById: () => null,
  querySelector: sel => (sel === '#content' ? contentStub
    : sel === '#sr-body' ? bodyStub
    : sel === '#sr-hint' ? hintStub
    : elStub()),
  querySelectorAll: () => [], addEventListener: () => {},
  createElement: () => ({ style: {}, classList: { add(){}, toggle(){} }, appendChild(){}, setAttribute(){}, parentNode: { insertBefore(){} } }),
  getElementsByTagName: () => [{ parentNode: { insertBefore(){} } }],
  body: { classList: { add(){} } }, activeElement: null,
};
global.window = global; global.open = () => {};
global.localStorage = { getItem: () => null, setItem: () => {} };
global.location = { hash: '' };
const sr = JSON.parse(fs.readFileSync('D:/baseball/data/season-roster.json', 'utf8'));
const fi = JSON.parse(fs.readFileSync('D:/baseball/portal/file-index.json', 'utf8'));
// 注意：file-index.json 请求挂起——阻止 eval 顶层 init 的 setPage('dashboard') 覆盖被测渲染输出
global.fetch = url => {
  if (url.includes('file-index.json')) return new Promise(() => {});
  return Promise.resolve({ ok: !url.includes('snapshots'), json: () => {
    if (url.includes('season-roster')) return Promise.resolve(sr);
    return Promise.resolve({});
  }, text: () => Promise.resolve('') });
};
global.refreshFileIndex = () => Promise.resolve(); global.setPage = () => {}; global.selectFile = () => {};
global.FILE_INDEX = fi;
(async () => {
  try {
    eval(code);
    await renderSeasonRosterPage();
    const srHtml = bodyCaptured;
    console.log('[sr] title:', captured.includes('历年阵容'));
    console.log('[sr] year select has 2026:', captured.includes('2026 赛季'));
    console.log('[sr] summary chips:', srHtml.includes('中途加入'));
    console.log('[sr] departed row (Alek Thomas):', srHtml.includes('Alek Thomas') && srHtml.includes('Outright 下放'));
    console.log('[sr] joined chip:', srHtml.includes('交易获得 05/12'));
    console.log('[sr] Ohtani two-way:', srHtml.includes('Shohei Ohtani'));
    console.log('[sr] count hint:', hintCaptured.includes('53 人'));
    // 球员报告版本
    const editions = reportEditions();
    console.log('[rep] editions:', JSON.stringify(editions.map(e => e.label)));
    console.log('[rep] fallback ok:', editions.length >= 1 && editions[0].path === 'report/index.html');
    console.log('SMOKE_OK');
  } catch (e) { console.error('SMOKE_FAIL:', e.stack || e); process.exit(1); }
})();
