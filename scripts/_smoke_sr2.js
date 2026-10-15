// debug: print captured after renderSeasonRosterPage
const fs = require('fs');
const html = fs.readFileSync('D:/baseball/index.html', 'utf8');
const m = html.match(/<script[^>]*>([\s\S]*?)<\/script>/g);
let code = '';
for (const block of m) {
  const body = block.replace(/^<script[^>]*>/, '').replace(/<\/script>$/, '');
  if (body.includes('renderPlayoffPage')) code = body;
}
let captured = 'UNSET';
const contentStub = { set innerHTML(v) { captured = v; }, get innerHTML() { return captured; } };
const bodyStub = { innerHTML: '' };
global.$ = sel => (sel === '#content' ? contentStub : (sel === '#sr-body' ? bodyStub : { value: '2026', textContent: '', style: {} }));
global.$$ = () => [];
global.document = { getElementById: () => null, querySelector: s => (s === '#content' ? contentStub : { value: '2026' }), querySelectorAll: () => [], addEventListener: () => {}, getElementsByTagName: () => [{ parentNode: { insertBefore(){} } }], body: { classList: { add(){} } }, createElement: () => ({ style: {}, classList: { add(){}, toggle(){} }, parentNode: { insertBefore(){} } }) };
global.window = global; global.open = () => {};
global.localStorage = { getItem: () => null, setItem: () => {} };
global.location = { hash: '' };
const sr = JSON.parse(fs.readFileSync('D:/baseball/data/season-roster.json', 'utf8'));
const fi = JSON.parse(fs.readFileSync('D:/baseball/portal/file-index.json', 'utf8'));
global.fetch = url => Promise.resolve({ ok: !url.includes('snapshots'), json: () => Promise.resolve(url.includes('season-roster') ? sr : fi) });
global.refreshFileIndex = () => Promise.resolve(); global.setPage = () => {}; global.selectFile = () => {};
global.FILE_INDEX = fi;
(async () => {
  try {
    eval(code);
    console.log('typeof:', typeof renderSeasonRosterPage, typeof renderSeasonRosterTable);
    await renderSeasonRosterPage();
    console.log('captured len:', captured.length);
    console.log('first 300:', captured.slice(0, 300).replace(/\n/g, ' '));
    console.log('body len:', bodyStub.innerHTML.length);
    console.log('SMOKE_OK');
  } catch (e) { console.error('FAIL:', e.stack || e); }
})();
