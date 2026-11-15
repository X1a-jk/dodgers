// 冒烟测试：桩掉 Web Audio + DOM，调用 ORGAN.start('ballgame') 验证调度
const fs = require('fs');
const html = fs.readFileSync('D:/baseball/index.html', 'utf8');

const startMark = '/* ---------- 球场风琴';
const endMark = '/* ---------- 球场风琴 END';
const si = html.indexOf(startMark), ei = html.indexOf(endMark);
if (si < 0 || ei < 0) { console.error('SMOKE_FAIL: markers not found'); process.exit(1); }
const code = html.slice(si, ei);

let oscCount = 0, lastStop = 0;
const stubParam = () => ({
    value: 0,
    setValueAtTime() {}, linearRampToValueAtTime() {}, exponentialRampToValueAtTime() {}
});
function makeOsc() {
    oscCount++;
    return { type: '', frequency: stubParam(), connect() {}, start(t) { if (t > lastStop) lastStop = t; }, stop(t) { if (t > lastStop) lastStop = t; } };
}
const ctx = {
    currentTime: 0,
    sampleRate: 44100,
    state: 'running',
    resume() {},
    destination: {},
    createGain: () => ({ gain: stubParam(), connect() {} }),
    createOscillator: makeOsc,
    createBuffer: () => ({ getChannelData: () => new Float32Array(8) }),
    createBufferSource: () => ({ buffer: null, connect() {}, start() {} }),
    createBiquadFilter: () => ({ type: '', frequency: stubParam(), Q: stubParam(), connect() {} })
};
let timers = [];
global.window = { AudioContext: function () { return ctx; } };
global.document = {
    querySelectorAll: () => [],
    addEventListener() {},
    getElementById: () => ({ classList: { add() {}, remove() {}, toggle() {} } })
};
global.setTimeout = (fn, ms) => { timers.push(ms); return timers.length; };
global.clearTimeout = () => {};

eval(code + '\nglobalThis.ORGAN = ORGAN;');

const ORGAN = globalThis.ORGAN;
if (typeof ORGAN === 'undefined' || !ORGAN) { console.error('SMOKE_FAIL: ORGAN undefined'); process.exit(1); }
ORGAN.ctx = ctx; ORGAN.master = { connect() {} };
ORGAN.start('ballgame');

// 期望：旋律 60 音×2 osc + 贝斯 32 + 击奏 128 音×2 osc = 408
console.log('oscillators scheduled:', oscCount);
console.log('last event at(s):', lastStop.toFixed(2));
console.log('stop timer(ms):', timers[0]);
if (oscCount !== 408) { console.error('SMOKE_FAIL: osc count', oscCount, '!== 408'); process.exit(1); }
if (lastStop < 39.5 || lastStop > 40.6) { console.error('SMOKE_FAIL: last event time out of range'); process.exit(1); }
if (timers[0] !== 40920) { console.error('SMOKE_FAIL: stop timer', timers[0]); process.exit(1); }
console.log('SMOKE_OK ballgame');
