// 冒烟：胜利小调 / Charge 助威（20 秒版）调度与时长断言
const fs = require('fs');
const html = fs.readFileSync('D:/baseball/index.html', 'utf8');

const si = html.indexOf('/* ---------- 球场风琴');
const ei = html.indexOf('/* ---------- 球场风琴 END');
if (si < 0 || ei < 0) { console.error('SMOKE_FAIL: organ block not found'); process.exit(1); }
const code = html.slice(si, ei);

let lastStop = 0;
const stubParam = () => ({ value: 0, setValueAtTime() {}, linearRampToValueAtTime() {}, exponentialRampToValueAtTime() {} });
const ctx = {
    currentTime: 0, sampleRate: 44100, state: 'running', resume() {}, destination: {},
    createGain: () => ({ gain: stubParam(), connect() {} }),
    createOscillator: () => ({ type: '', frequency: stubParam(), connect() {}, start(t) { if (t > lastStop) lastStop = t; }, stop(t) { if (t > lastStop) lastStop = t; } }),
    createBuffer: () => ({ getChannelData: () => new Float32Array(8) }),
    createBufferSource: () => ({ buffer: null, connect() {}, start() {} }),
    createBiquadFilter: () => ({ type: '', frequency: stubParam(), Q: stubParam(), connect() {} })
};
let timers = [];
global.window = { AudioContext: function () { return ctx; } };
global.document = { querySelectorAll: () => [], addEventListener() {}, getElementById: () => ({ classList: { add() {}, remove() {}, toggle() {} } }) };
global.setTimeout = (fn, ms) => { timers.push(ms); return timers.length; };
global.clearTimeout = () => {};

eval(code + '\nglobalThis.ORGAN = ORGAN;');
const ORGAN = globalThis.ORGAN;

// 胜利小调：4 组模进（每组 6 音 + 4 音和弦 = 10 音符 × 4 谐波振荡器）+ 华彩 7 + 收尾和弦 5+6+6
lastStop = 0; timers = [];
ORGAN.ctx = ctx; ORGAN.master = { connect() {} };
ORGAN.start('victory');
const vOsc = 4 * (10 * 4) + 7 * 4 + (5 + 6 + 6) * 4; // 282
console.log('victory | timer', timers[0], '(exp 19500)', Math.round(timers[0]) === 19500 ? 'OK' : 'FAIL',
    '| last', lastStop.toFixed(2), '(exp ~19.2)', (lastStop > 18.5 && lastStop < 19.6) ? 'OK' : 'FAIL');

lastStop = 0; timers = [];
ORGAN.start('charge');
// charge：滚奏1 12 + 4×cycle(4[+4]+1+1+4和弦音) + 滚奏2 22 + 终章(4×2+1+1+1+7和弦)
const cOsc = 12 * 4 + (8 + 9 + 10 + 10) * 4 + 22 * 4 + (8 + 1 + 1 + 1 + 7) * 4;
console.log('charge  | timer', timers[0], '(exp 19500)', Math.round(timers[0]) === 19500 ? 'OK' : 'FAIL',
    '| last', lastStop.toFixed(2), '(exp ~19.1)', (lastStop > 18.4 && lastStop < 19.5) ? 'OK' : 'FAIL');

const vOk = Math.round(timers[0]) === 19500;
console.log(vOk ? 'SMOKE_OK jingles' : 'SMOKE_FAIL');
