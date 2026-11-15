// 离线渲染 胜利小调 + Charge 助威（20 秒版）试听，数据与门户一致
const fs = require('fs');
const html = fs.readFileSync('D:/baseball/index.html', 'utf8');
const si = html.indexOf('/* ---------- 球场风琴');
const ei = html.indexOf('/* ---------- 球场风琴 END');
const code = html.slice(si, ei);

// 提取 start() 中 victory/charge 两个分支的调度逻辑：直接用 ORGAN 桩运行并收集事件
const events = [];
let lastStop = 0;
const stubParam = () => ({ value: 0, setValueAtTime() {}, linearRampToValueAtTime() {}, exponentialRampToValueAtTime() {} });
const ctx = {
    currentTime: 0, sampleRate: 44100, state: 'running', resume() {}, destination: {},
    createGain: () => ({ gain: stubParam(), connect() {} }),
    createOscillator: () => ({ type: '', frequency: stubParam(), connect() {}, start() {}, stop() {} }),
    createBuffer: () => ({ getChannelData: () => new Float32Array(8) }),
    createBufferSource: () => ({ buffer: null, connect() {}, start() {} }),
    createBiquadFilter: () => ({ type: '', frequency: stubParam(), Q: stubParam(), connect() {} })
};
global.window = { AudioContext: function () { return ctx; } };
global.document = { querySelectorAll: () => [], addEventListener() {}, getElementById: () => ({ classList: { add() {}, remove() {}, toggle() {} } }) };
global.setTimeout = () => 0;
global.clearTimeout = () => {};

// 捕获每个音符事件
const NOTE = [];
const origStart = Object.getPrototypeOf;
eval(code + '\nglobalThis.ORGAN = ORGAN;');
const ORGAN = globalThis.ORGAN;
ORGAN.ctx = ctx; ORGAN.master = { connect() {} };
const realNote = ORGAN.note.bind(ORGAN);
const realChord = ORGAN.chord.bind(ORGAN);
ORGAN.note = (m, t, d, v) => { NOTE.push([m, t, d, v == null ? 1 : v]); };
ORGAN.chord = (midis, t, d, v) => midis.forEach(m => NOTE.push([m, t, d, v == null ? 1 : v]));

for (const key of ['victory', 'charge']) {
    const before = NOTE.length;
    ORGAN.start(key);
    const dur = key === 'victory' ? 19.5 : 19.5;
    console.log(key, 'notes', NOTE.length - before, 'dur', dur);
}

const SR = 22050, GAP = 1;
const total = 19.5 + GAP + 19.5 + 1;
const n = Math.floor(SR * total);
const out = new Float32Array(n);

function addNote(midi, t0, dur, vel, offset) {
    const f = 440 * Math.pow(2, (midi - 69) / 12);
    const peak = 0.35 * vel * 0.5; // master 0.22 归一
    const s0 = Math.floor((offset + t0) * SR), s1 = Math.min(n, Math.ceil((offset + t0 + dur) * SR));
    for (let s = s0; s < s1; s++) {
        const t = s / SR - offset - t0;
        if (t < 0 || t > dur) continue;
        let amp;
        if (t < 0.025) amp = peak * Math.exp(Math.log(0.0001 / peak) * (1 - t / 0.025)) * (t / 0.025);
        else if (t < Math.max(0.03, dur - 0.09)) amp = peak;
        else amp = peak * Math.exp(Math.log(0.0001 / peak) * ((t - Math.max(0.03, dur - 0.09)) / (dur - Math.max(0.03, dur - 0.09))));
        const tt = s / SR;
        out[s] += amp * (Math.sin(2 * Math.PI * f * tt) + 0.26 * Math.sin(2 * Math.PI * f * 2 * tt) + 0.14 * Math.sin(2 * Math.PI * f * 3 * tt) + 0.07 * Math.sin(2 * Math.PI * f * 4 * tt));
    }
}
let off = 0;
for (const key of ['victory', 'charge']) {
    const before = NOTE.length;
    ORGAN.start(key);
    for (let i = before; i < NOTE.length; i++) { const [m, t, d, v] = NOTE[i]; addNote(m, t, d, v, off); }
    off += 19.5 + GAP;
}
let peak = 0;
for (let i = 0; i < n; i++) { const a = Math.abs(out[i]); if (a > peak) peak = a; }
const g = 0.89 / peak;
const pcm = Buffer.alloc(44 + n * 2);
pcm.write('RIFF', 0); pcm.writeUInt32LE(36 + n * 2, 4); pcm.write('WAVE', 8);
pcm.write('fmt ', 12); pcm.writeUInt32LE(16, 16); pcm.writeUInt16LE(1, 20);
pcm.writeUInt16LE(1, 22); pcm.writeUInt32LE(SR, 24); pcm.writeUInt32LE(SR * 2, 28);
pcm.writeUInt16LE(2, 32); pcm.writeUInt16LE(16, 34);
pcm.write('data', 36); pcm.writeUInt32LE(n * 2, 40);
for (let i = 0; i < n; i++) { const v = Math.max(-1, Math.min(1, out[i] * g)); pcm.writeInt16LE(Math.round(v * 32767), 44 + i * 2); }
fs.writeFileSync('D:/baseball/jingles-20s-preview.wav', pcm);
console.log('written', pcm.length, 'bytes,', total.toFixed(1) + 's, peak', peak.toFixed(2));
