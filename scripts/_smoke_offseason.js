// 冒烟：休赛期转会中心页 v2（细致版）
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

    check('六板块标题齐全（中文名）', ['冬市总览', '转会流水台', '全联盟重磅动向', '自由球员追踪', '流言雷达', '40 人名单守望'].every(t => captured.includes(t)));
    check('总览卡显示 37 / 40', captured.includes('37 / 40'));
    check('无加载失败提示', !captured.includes('休赛期数据加载失败'));

    // 时间轴
    check('休赛期时间轴存在（冬季会议）', captured.includes('冬季会议'));
    check('时间轴含 6 个节点', (captured.match(/os-tl-item/g) || []).length === 6);

    // 流水台：日期分组 + 中文摘要
    const feed = (stubMap['#os-feed'] || {}).innerHTML || '';
    check('流水台渲染全部 10 条', rows(feed) === 10);
    check('日期分组存在', (feed.match(/os-date-group/g) || []).length === 2 && feed.includes('10月29日'));
    check('中文摘要（选择成为自由球员）', feed.includes('选择成为自由球员'));
    check('中文摘要（小联盟合约签下）', feed.includes('小联盟合约签下') && feed.includes('Alberto Santos'));
    check('位置标签（左投/游击手）', feed.includes('左投') && feed.includes('游击手'));
    check('筛选 chips 含名单操作', captured.includes('名单操作'));

    // 搜索
    osSetQuery('rojas');
    const feed2 = (stubMap['#os-feed'] || {}).innerHTML || '';
    check('搜索 rojas 只剩 1 条', rows(feed2) === 1 && feed2.includes('Rojas'));
    osSetQuery('');
    check('清空搜索恢复 10 条', rows((stubMap['#os-feed'] || {}).innerHTML || '') === 10);

    // 筛选（other 应只剩 0 条名单操作 -> 显示空态；用 signed_milb 筛 1 条）
    osSetFilter('signed_milb', null);
    const feed3 = (stubMap['#os-feed'] || {}).innerHTML || '';
    check('筛选小联盟签约只剩 Santos', rows(feed3) === 1 && feed3.includes('Santos'));
    osSetFilter('all', null);
    check('恢复全部筛选', rows((stubMap['#os-feed'] || {}).innerHTML || '') === 10);

    // 全联盟重磅
    check('全联盟交易合并（Rayo / Eaton）', captured.includes('Jareth Rayo / Nate Eaton'));
    check('全联盟中文摘要', captured.includes('交易至红袜'));

    // FA 追踪
    check('待签约 9 人', captured.includes('待签约（9 人）'));
    check('Rojas 用打击数据（非 ERA）', captured.includes('打击率 .267') && !captured.includes('ERA 13.50'));
    check('Vesia 投手数据', captured.includes('ERA 2.64'));

    // 流言
    check('流言示例条目被过滤+空态提示', !captured.includes('示例条目') && captured.includes('搜一下转会流言'));

    // 40 人守望
    check('40 人进度条存在', captured.includes('os-progress-bar'));
    check('剩余名额提示', captured.includes('剩余 3 个名额'));
    check('40 人新增红绿标渲染数与数据一致', (captured.match(/os-man del/g) || []).length === (osData.dodgers.roster40.removed || []).length && (captured.match(/os-man add/g) || []).length === (osData.dodgers.roster40.added || []).length);
    check('40 人移除与 JSON 一致（当前应为 0：上次快照已含变动）', (captured.match(/os-man del/g) || []).length === 0 || captured.includes((osData.dodgers.roster40.removed || [])[0] || ''));

    console.log(fails === 0 ? 'SMOKE_OK' : 'SMOKE_FAIL');
    process.exit(fails === 0 ? 0 : 1);
  } catch (e) { console.error('SMOKE_FAIL:', e.stack || e); process.exit(1); }
})();
