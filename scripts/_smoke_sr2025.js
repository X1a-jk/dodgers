// 冒烟：历年阵容页 2025（快照模式）
const fs = require('fs');
const html = fs.readFileSync('D:/baseball/index.html', 'utf8');
const m = html.match(/<script[^>]*>([\s\S]*?)<\/script>/g);
let code = '';
for (const block of m) {
  const body = block.replace(/^<script[^>]*>/, '').replace(/<\/script>$/, '');
  if (body.includes('renderPlayoffPage')) code = body;
}
let captured = ''; let bodyCaptured = ''; let hintCaptured = '';
const contentStub = { set innerHTML(v) { captured = v; }, get innerHTML() { return captured; } };
const bodyStub = { set innerHTML(v) { bodyCaptured = v; }, get innerHTML() { return bodyCaptured; } };
const hintStub = { set textContent(v) { hintCaptured = v; }, get textContent() { return hintCaptured; } };
const elStub = () => ({ textContent: '', innerHTML: '', disabled: false, onclick: null, value: '2025', style: {}, dataset: {}, classList: { toggle(){}, add(){}, remove(){} } });
global.$ = sel => (sel === '#content' ? contentStub
  : sel === '#sr-year' ? { value: '2025' }
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
const sr = JSON.parse(fs.readFileSync('D:/baseball/seasons/2025/snapshots/season-roster.json', 'utf8'));
const fi = JSON.parse(fs.readFileSync('D:/baseball/portal/file-index.json', 'utf8'));
global.fetch = url => {
  if (url.includes('file-index.json')) return new Promise(() => {});
  if (url.includes('seasons/2025/snapshots/season-roster.json'))
    return Promise.resolve({ ok: true, json: () => Promise.resolve(sr), text: () => Promise.resolve('') });
  return Promise.resolve({ ok: false, json: () => Promise.resolve({}), text: () => Promise.resolve('') });
};
global.refreshFileIndex = () => Promise.resolve(); global.setPage = () => {}; global.selectFile = () => {};
global.FILE_INDEX = fi;
(async () => {
  try {
    eval(code);
    await renderSeasonRosterTable();
    const a = [];
    a.push(['hint 年份+人数', hintCaptured.includes('2025 赛季') && hintCaptured.includes('62 人')]);
    a.push(['无降级错误', !bodyCaptured.includes('数据不存在')]);
    a.push(['Ohtani 行', bodyCaptured.includes('Shohei Ohtani')]);
    a.push(['Kershaw 宣布自由球员标签', bodyCaptured.includes('宣布自由球员')]);
    a.push(['Outman 交易离队标签', bodyCaptured.includes('交易离队')]);
    a.push(['Stewart 交易获得标签', bodyCaptured.includes('交易获得')]);
    a.push(['统计行(ERA)', bodyCaptured.includes('ERA')]);
    let fail = 0;
    for (const [name, ok] of a) { console.log(ok ? ' ok ' : 'FAIL', name); if (!ok) fail++; }
    console.log(fail ? 'SMOKE_FAIL' : 'SMOKE_OK');
    if (fail) process.exit(1);
  } catch (e) { console.error('SMOKE_FAIL:', e.stack || e); process.exit(1); }
})();
