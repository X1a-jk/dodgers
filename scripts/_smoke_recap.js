// 冒烟：常规赛总结页（存档列表修复）+ 深度图链接
const fs = require('fs');
const path = require('path');
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
const elStub = (sel) => (stubMap[sel] = stubMap[sel] || { textContent: '', innerHTML: '', disabled: false, onclick: null, value: sel === '#rc-year' ? '2026' : '', style: {}, dataset: {}, classList: { toggle(){}, add(){} } });
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
const dash = JSON.parse(fs.readFileSync('D:/baseball/portal/dashboard-data.json', 'utf8'));
const post = JSON.parse(fs.readFileSync('D:/baseball/data/postseason.json', 'utf8'));
const summaryMd = fs.readFileSync('D:/baseball/seasons/2026/2026-赛季总结.md', 'utf8');
global.fetch = url => Promise.resolve({ ok: true, json: () => Promise.resolve(post), text: () => Promise.resolve(summaryMd) });
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
    console.log('[dbg] body length:', bodyHtml.length, '| has 周战报标题:', bodyHtml.includes('周战报全存档'));
    const weekItems = (bodyHtml.match(/viewWeeklyArchive/g) || []).length;
    const psItems = (bodyHtml.match(/viewPsArchive/g) || []).length;
    check('周战报存档列表 15 条', weekItems === 15);
    check('季后赛战报列表 9 条', psItems === 9);
    check('无"暂无存档"空态', !bodyHtml.includes('暂无存档'));
    check('无"暂无季后赛战报"空态', !bodyHtml.includes('暂无季后赛战报'));
    check('显示世界大赛种子区块', bodyHtml.includes('季后赛最终种子'));
    check('道奇状态=止步NLCS', post.dodgers.status.includes('止步国联冠军赛'));

    // 深度图链接检查：所有 reportUrl 指向存在的文件
    const dc = JSON.parse(fs.readFileSync('D:/baseball/data/depth-chart.json', 'utf8').replace(/^\uFEFF/, ''));
    let urls = [];
    const walk = o => {
      if (Array.isArray(o)) return o.forEach(walk);
      if (o && typeof o === 'object') {
        if (o.reportUrl) urls.push(o.reportUrl);
        Object.values(o).forEach(walk);
      }
    };
    walk(dc);
    const inj = JSON.parse(fs.readFileSync('D:/baseball/data/injuries.json', 'utf8').replace(/^\uFEFF/, ''));
    walk(inj);
    const bad = urls.filter(u => !u.startsWith('seasons/2026/players/') || !fs.existsSync(path.join('D:/baseball', u.replace(/\//g, path.sep))));
    check(`深度图+伤病 共 ${urls.length} 个 reportUrl 全部有效且指向赛季总结版`, urls.length > 0 && bad.length === 0);
    if (bad.length) console.log('BAD:', bad.slice(0, 5));
    check('深度图/伤病 JSON 无 BOM', !fs.readFileSync('D:/baseball/data/depth-chart.json').slice(0, 3).equals(Buffer.from([0xEF, 0xBB, 0xBF])) && !fs.readFileSync('D:/baseball/data/injuries.json').slice(0, 3).equals(Buffer.from([0xEF, 0xBB, 0xBF])));

    // 报告回退键检查
    const editions = ['players', 'players-regular', 'players-postseason'];
    let total = 0, noBtn = 0;
    for (const ed of editions) {
      const root = path.join('D:/baseball/seasons/2026', ed);
      for (const d of fs.readdirSync(root)) {
        const dir = path.join(root, d);
        if (!fs.statSync(dir).isDirectory()) continue;
        for (const f of fs.readdirSync(dir)) {
          if (f.endsWith('-scouting-report.html')) {
            total++;
            const s = fs.readFileSync(path.join(dir, f), 'utf8');
            if (!s.includes("history.back()")) noBtn++;
          }
        }
      }
    }
    check(`三个批次共 ${total} 份报告全部含回退键（缺 ${noBtn}）`, noBtn === 0 && total >= 137);

    // 报告 index 链接可达性
    for (const ed of editions) {
      check(`${ed}/index.html 存在`, fs.existsSync(path.join('D:/baseball/seasons/2026', ed, 'index.html')));
    }
    console.log(fails === 0 ? 'SMOKE_OK' : 'SMOKE_FAIL');
    process.exit(fails === 0 ? 0 : 1);
  } catch (e) { console.error('SMOKE_FAIL:', e.stack || e); process.exit(1); }
})();
