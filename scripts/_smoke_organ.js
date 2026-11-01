// 冒烟：球场风琴（Web Audio 合成逻辑）
const fs = require('fs');
const html = fs.readFileSync('D:/baseball/index.html', 'utf8');

let fails = 0;
const check = (label, cond) => { console.log((cond ? '[OK] ' : '[FAIL] ') + label); if (!cond) fails++; };

check('浮动按钮 HTML 存在', html.includes('id="organ-fab"'));
check('三个 chip 存在', ['organ-victory', 'organ-charge', 'organ-clap'].every(x => html.includes(x)));

const m = html.match(/<script[^>]*>([\s\S]*?)<\/script>/g);
let code = '';
for (const block of m) {
  const body = block.replace(/^<script[^>]*>/, '').replace(/<\/script>$/, '');
  if (body.includes('ORGAN')) code = body;
}
if (!code) { console.error('SMOKE_FAIL: 找不到 ORGAN 代码'); process.exit(1); }

const COUNTS = { ctx: 0, osc: 0, gain: 0, buf: 0, start: 0 };
function FakeParam(v) { return { value: v, setValueAtTime() {}, exponentialRampToValueAtTime() {} }; }
function fakeNode() {
  return { connect() {}, start() { COUNTS.start++; }, stop() {},
    gain: FakeParam(1), frequency: FakeParam(0), Q: FakeParam(0), type: '', buffer: null };
}
class FakeAC {
  constructor() { this.currentTime = 0; this.state = 'running'; this.sampleRate = 44100; this.destination = {}; COUNTS.ctx++; }
  resume() {}
  createGain() { COUNTS.gain++; return fakeNode(); }
  createOscillator() { COUNTS.osc++; return fakeNode(); }
  createBufferSource() { COUNTS.buf++; return fakeNode(); }
  createBiquadFilter() { return fakeNode(); }
  createBuffer(ch, len) { return { getChannelData: () => new Float32Array(len) }; }
}

let captured = '';
const contentStub = { set innerHTML(v) { captured = v; }, get innerHTML() { return captured; } };
const stubMap = {};
const elStub = (key) => (stubMap[key] = stubMap[key] || { textContent: '', innerHTML: '', disabled: false, onclick: null, value: '', style: {}, dataset: {}, classList: { toggle() {}, add() {}, remove() {} } });
global.$ = sel => (sel === '#content' ? contentStub : elStub(sel));
global.$$ = () => [];
global.document = {
  getElementById: id => elStub('#' + id),
  querySelector: sel => (sel === '#content' ? contentStub : elStub(sel)),
  querySelectorAll: () => [], addEventListener: () => {},
  createElement: () => ({ style: {}, classList: { add() {}, toggle() {} }, appendChild() {}, setAttribute() {}, parentNode: { insertBefore() {} } }),
  getElementsByTagName: () => [{ parentNode: { insertBefore() {} } }],
  body: { classList: { add() {} } }, activeElement: null,
};
global.window = global;
global.AudioContext = FakeAC;
global.localStorage = { getItem: () => null, setItem: () => {} };
global.location = { hash: '' };

(async () => {
  try {
    eval(code + '\nglobalThis.__ORGAN = ORGAN;');
    const ORGAN = globalThis.__ORGAN;

    organPlay('victory');
    check('胜利小调启动（current=victory）', ORGAN.current && ORGAN.current.key === 'victory');
    check('胜利小调产生振荡器', COUNTS.osc >= 24);
    if (ORGAN.current && ORGAN.current.timer) ORGAN.current.timer.unref();

    organPlay('charge');
    check('切换 Charge（current=charge）', ORGAN.current && ORGAN.current.key === 'charge');
    if (ORGAN.current && ORGAN.current.timer) ORGAN.current.timer.unref();

    organPlay('charge');
    check('再点同 chip 停止', ORGAN.current === null);

    const oscBefore = COUNTS.osc;
    organPlay('clap');
    check('人浪节拍启动', ORGAN.current && ORGAN.current.key === 'clap');
    check('拍手 = 噪声源（8小节 >40 次）', COUNTS.buf - (COUNTS.bufBefore || 0) >= 40 || COUNTS.start > 40);
    if (ORGAN.current && ORGAN.current.timer) ORGAN.current.timer.unref();

    ORGAN.start('victory');
    ORGAN.stop();
    check('ORGAN.stop 清空状态', ORGAN.current === null);

    console.log('  [dbg] osc=%d gain=%d buf=%d ctx=%d', COUNTS.osc, COUNTS.gain, COUNTS.buf, COUNTS.ctx);
    console.log(fails === 0 ? 'SMOKE_OK' : 'SMOKE_FAIL');
    process.exit(fails === 0 ? 0 : 1);
  } catch (e) { console.error('SMOKE_FAIL:', e.stack || e); process.exit(1); }
})();
