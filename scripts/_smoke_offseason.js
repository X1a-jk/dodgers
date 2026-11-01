// 冒烟：休赛期转会中心页
const fs = require('fs');
const html = fs.readFileSync('D:/baseball/index.html', 'utf8');
const m = html.match(/<script[^>]*>([\s\S]*?)<\/script>/g);
let code = '';
for (const block of m) {
  const body = block.replace(/^<script[^>]*>/, '').replace(/<\/script>$/, '');
  if (body.includes('renderOffseasonPage')) code = body;
}
if (!code) { console.error('SMOKE_FAIL: 找不到含 renderOffseasonPage 的 script 块'); process.exit(1); }

let captured = '';
const contentStub = { set innerHTML(v) { captured = v; }, get innerHTML() { return captured; } };
const stubMap = {};
const elStub = (key) => (stubMap[key] = stubMap[key] || { textContent: '', innerHTML: '', disabled: false, onclick: null, value: '', style: {}, dataset: {}, classList: { toggle(){}, add(){}, remove(){} } });
global.$ = sel => (sel === '#content' ? contentStub : elStub(sel));
global.$$ = () => [];
global.document = {
  getElementById: id => elStub('#' + id),
  querySelector: sel => (sel === '#content' ? contentStub : elStub(sel)),
  querySelectorAll: () => [], addEventListener: () => {},
  createElement: () => ({ style: {}, classList: { add(){}, toggle(){} }, appendChild(){}, setAttribute(){}, parentNode: { insertBefore(){} } }),
  getElementsByTagName: () => [{ parentNode: { insertBefore(){} } }],
  body: { classList: { add(){} } }, activeElement: null,
};
global.window = global; global.open = () => {};
global.localStorage = { getItem: () => null, setItem: () => {} };
global.location = { hash: '' };

const osData = JSON.parse(fs.readFileSync('D:/baseball/data/offseason.json', 'utf8'));
const newsData = JSON.parse(fs.readFileSync('D:/baseball/data/offseason-news.json', 'utf8'));
global.fetch = url => {
  if (url.includes('offseason-news')) return Promise.resolve({ ok: true, json: () => Promise.resolve(newsData) });
  return Promise.resolve({ ok: true, json: () => Promise.resolve(osData) });
};
global.marked = { parse: s => s };

let fails = 0;
const check = (label, cond) => { console.log((cond ? '[OK] ' : '[FAIL] ') + label); if (!cond) fails++; };
const rows = htmlStr => (htmlStr.match(/class="os-row"/g) || []).length;

(async () => {
  try {
    eval(code);
    await renderOffseasonPage();

    check('六板块标题齐全', ['冬市总览', '转会流水台', '全联盟重磅', '自由球员追踪', '流言雷达', '40 人名单守望'].every(t => captured.includes(t)));
    check('总览卡显示 37 / 40', captured.includes('37 / 40'));
    check('无加载失败提示', !captured.includes('休赛期数据加载失败'));

    const feed = (stubMap['#os-feed'] || {}).innerHTML || '';
    check('流水台默认渲染全部 10 条', rows(feed) === 10);
    check('筛选 chips 齐全', ['大联盟签约', '小联盟签约', '宣布FA', '交易'].every(t => captured.includes(t)));
    check('Santos 归类为小联盟签约', feed.includes('小联盟签约') && feed.includes('Alberto Santos'));
    check('typeDesc 分类非 typeCode（无"指定让渡"误标）', !feed.includes('指定让渡'));

    osSetQuery('rojas');
    const feed2 = (stubMap['#os-feed'] || {}).innerHTML || '';
    check('搜索 rojas 只剩 1 条', rows(feed2) === 1 && feed2.includes('Rojas'));
    osSetQuery('');
    const feed3 = (stubMap['#os-feed'] || {}).innerHTML || '';
    check('清空搜索恢复 10 条', rows(feed3) === 10);

    check('全联盟交易已合并（Rayo / Eaton 一条）', captured.includes('Jareth Rayo / Nate Eaton'));
    check('FA 待签约列 9 人', captured.includes('待签约 (9)') && captured.includes('Miguel Rojas'));
    check('流言示例条目被过滤+空态提示', !captured.includes('示例条目') && captured.includes('喊助手'));
    check('40 人新增绿标含 Gavin Stone', captured.includes('Gavin Stone'));
    check('40 人移除红标含 Miguel Rojas', (captured.match(/os-man del/g) || []).length >= 19);

    console.log(fails === 0 ? 'SMOKE_OK' : 'SMOKE_FAIL');
    process.exit(fails === 0 ? 0 : 1);
  } catch (e) { console.error('SMOKE_FAIL:', e.stack || e); process.exit(1); }
})();
