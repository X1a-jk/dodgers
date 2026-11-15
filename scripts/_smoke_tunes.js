// 冒烟：4 首新曲全部调度无异常 + 时长断言
const fs = require('fs');
const html = fs.readFileSync('D:/baseball/index.html', 'utf8');
const si = html.indexOf('/* ---------- 球场风琴');
const ei = html.indexOf('/* ---------- 球场风琴 END');
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

eval(code + '\nglobalThis.ORGAN = ORGAN; globalThis.ORGAN_TUNES = ORGAN_TUNES;');
const ORGAN = globalThis.ORGAN, ORGAN_TUNES = globalThis.ORGAN_TUNES;

const EXPECT = {
    banner:   { timer: 41240, range: [40.5, 41.5] },
    ssf:      { timer: 36900, range: [36.3, 37.3] },
    grandold: { timer: 28660, range: [28.1, 29.1] },
    saints:   { timer: 19400, range: [18.8, 19.8] },
};
let ok = true;
for (const key of Object.keys(EXPECT)) {
    if (!ORGAN_TUNES[key]) { console.error('MISSING tune', key); ok = false; continue; }
    lastStop = 0; timers = [];
    ORGAN.ctx = ctx; ORGAN.master = { connect() {} };
    ORGAN.start(key);
    const e = EXPECT[key];
    const tOk = Math.round(timers[0]) === e.timer;
    const rOk = lastStop >= e.range[0] && lastStop <= e.range[1];
    console.log(key, '| timer', timers[0], '(exp', e.timer + ')', tOk ? 'OK' : 'FAIL',
        '| last', lastStop.toFixed(2), '(exp', e.range[0] + '-' + e.range[1] + ')', rOk ? 'OK' : 'FAIL');
    if (!tOk || !rOk) ok = false;
}
console.log(ok ? 'SMOKE_OK tunes×4' : 'SMOKE_FAIL');
process.exit(ok ? 0 : 1);
