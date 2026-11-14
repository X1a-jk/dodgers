// 冒烟：recap 总结页 2025（ postseason.json 快照 + 总结 md 阅读入口）
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
const stubMap = {};
const elStub = (sel) => (stubMap[sel] = stubMap[sel] || { textContent: '', innerHTML: '', disabled: false, onclick: null, value: sel === '#rc-year' ? '2025' : '', style: {}, dataset: {}, classList: { toggle(){}, add(){} } });
global.$ = sel => (sel === '#content' ? contentStub : elStub(sel));
global.$$ = () => [];
global.document = {
  getElementById: () => null,
  querySelector: sel => (sel === '#content' ? contentStub : elStub(sel)),
  querySelectorAll: () => [], addEventListener: () => {},
  createElement: () => ({ style: {}, classList: { add(){}, toggle(){} }, appendChild(){}, setAttribute(){}, parentNode: { insertBefore(){} } }),
  getElementsByTagName: () => [{ parentNode: { insertBefore(){} } }],
  body: { classList: { add(){} } }, activeElement: null,
};
global.window = global; global.open = () => {};
global.localStorage = { getItem: () => null, setItem: () => {} };
global.location = { hash: '' };
const fileindex = JSON.parse(fs.readFileSync('D:/baseball/portal/file-index.json', 'utf8'));
const post = JSON.parse(fs.readFileSync('D:/baseball/seasons/2025/snapshots/postseason.json', 'utf8'));
const summaryMd = fs.readFileSync('D:/baseball/seasons/2025/2025-赛季总结.md', 'utf8');
global.fetch = url => {
  if (url.includes('seasons/2025/snapshots/postseason.json'))
    return Promise.resolve({ ok: true, json: () => Promise.resolve(post), text: () => Promise.resolve(summaryMd) });
  if (url.includes('2025-赛季总结.md'))
    return Promise.resolve({ ok: true, json: () => Promise.resolve({}), text: () => Promise.resolve(summaryMd) });
  if (url.includes('file-index.json')) return new Promise(() => {});
  return Promise.resolve({ ok: false, json: () => Promise.resolve({}), text: () => Promise.resolve('') });
};
global.refreshFileIndex = () => Promise.resolve(); global.setPage = () => {}; global.selectFile = () => {};
global.FILE_INDEX = fileindex;
global.marked = { parse: s => s };
let fails = 0;
const check = (label, cond) => { console.log((cond ? '[OK] ' : '[FAIL] ') + label); if (!cond) fails++; };
(async () => {
  try {
    eval(code);
    await renderRecapContent();
    const bodyHtml = (stubMap['#rc-body'] || {}).innerHTML || '';
    const hint = (stubMap['#rc-hint'] || {}).textContent || '';
    check('无降级错误', !bodyHtml.includes('总结数据不存在'));
    check('hint=季后赛数据', hint.includes('季后赛数据'));
    check('季后赛最终种子区块', bodyHtml.includes('季后赛最终种子'));
    check('红人出现在 6 号种子', bodyHtml.includes('Cincinnati Reds'));
    check('蓝鸟出现在种子区块', bodyHtml.includes('Toronto Blue Jays'));
    check('道奇战绩标签(93-69)', bodyHtml.includes('93-69'));
    check('阅读 2025 赛季总结入口', bodyHtml.includes('阅读 2025 赛季总结'));
    check('打击领袖(55轰)', bodyHtml.includes('55'));
    check('道奇状态=世界大赛冠军', post.dodgers.status.includes('世界大赛冠军'));
    check('冠军=道奇(119)', post.dodgers.champion === 119);
    check('道奇种子=3', post.dodgers.seed === 3);
    console.log(fails ? 'SMOKE_FAIL' : 'SMOKE_OK');
    if (fails) process.exit(1);
  } catch (e) { console.error('SMOKE_FAIL:', e.stack || e); process.exit(1); }
})();
