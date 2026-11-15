// 离线渲染 8-bit 版 Take Me Out to the Ball Game 预览 WAV
// 数据直接从 index.html 提取，保证与门户在线播放一致
const fs = require('fs');
const html = fs.readFileSync('D:/baseball/index.html', 'utf8');

function extractArray(name) {
    const m = html.match(new RegExp('const ' + name + ' = \\[([\\s\\S]*?)\\];'));
    if (!m) throw new Error(name + ' not found');
    return eval('[' + m[1] + ']');
}
const MELODY = extractArray('MELODY');
const HARM = extractArray('HARM');
const beat = 0.42;
const SR = 22050;
const DUR = 41.0;
const n = Math.floor(SR * DUR);
const out = new Float32Array(n);

function envAmp(t, dur, peak) {
    // 对齐 Web Audio 版包络：attack 0.008s，exp 衰减到 0.55peak，结尾 0.07s release
    const atk = 0.008;
    const decT = Math.min(0.25, dur * 0.5);
    const relStart = Math.max(0.03, dur - 0.07);
    if (t < 0 || t > dur) return 0;
    if (t < atk) return peak * (t / atk);
    if (t < atk + decT) {
        const p = (t - atk) / decT;
        return peak * Math.pow(0.55, p);
    }
    if (t < relStart) return peak * 0.55;
    const p = (t - relStart) / (dur - relStart);
    return Math.max(peak * 0.55 * Math.pow(0.0001 / (peak * 0.55), p), 0);
}

function addLead(midi, t0, dur, vel) {
    const f = 440 * Math.pow(2, (midi - 69) / 12);
    const peak = 0.3 * vel;
    const s0 = Math.floor(t0 * SR), s1 = Math.min(n, Math.ceil((t0 + dur) * SR));
    for (let s = s0; s < s1; s++) {
        const t = s / SR - t0;
        const amp = envAmp(t, dur, peak);
        if (amp <= 0) continue;
        const ph = (s / SR) * f;
        const sq = 2 * (2 * Math.floor(ph) - Math.floor(2 * ph) + 1) - 1; // ±1 方波近似
        out[s] += amp * sq + amp * 0.1 * (2 * (2 * Math.floor(ph * 2) - Math.floor(4 * ph) + 1) - 1);
    }
}
function addBass(midi, t0, dur) {
    const f = 440 * Math.pow(2, (midi - 69) / 12);
    const peak = 0.24;
    const s0 = Math.floor(t0 * SR), s1 = Math.min(n, Math.ceil((t0 + dur) * SR));
    for (let s = s0; s < s1; s++) {
        const t = s / SR - t0;
        if (t < 0 || t > dur) continue;
        const atk = 0.012;
        let amp;
        if (t < atk) amp = peak * t / atk;
        else amp = peak * Math.pow(0.0001 / peak, (t - atk) / (dur - atk));
        out[s] += amp * (2 / Math.PI) * Math.asin(Math.sin(2 * Math.PI * f * s / SR)); // 三角波
    }
}

MELODY.forEach(([m, b, d]) => addLead(m, b * beat, d * beat * 0.92, 1));
HARM.forEach(([ch, root, pair], bar) => {
    const bt = bar * 3 * beat;
    addBass(root, bt, beat * 0.9);
    pair.forEach(mm => addLead(mm, bt + beat, 0.12, 0.32));
    pair.forEach(mm => addLead(mm, bt + 2 * beat, 0.12, 0.32));
});

// 归一化
let peak = 0;
for (let i = 0; i < n; i++) { const a = Math.abs(out[i]); if (a > peak) peak = a; }
const g = 0.89 / peak;
const pcm = Buffer.alloc(44 + n * 2);
pcm.write('RIFF', 0); pcm.writeUInt32LE(36 + n * 2, 4); pcm.write('WAVE', 8);
pcm.write('fmt ', 12); pcm.writeUInt32LE(16, 16); pcm.writeUInt16LE(1, 20);
pcm.writeUInt16LE(1, 22); pcm.writeUInt32LE(SR, 24); pcm.writeUInt32LE(SR * 2, 28);
pcm.writeUInt16LE(2, 32); pcm.writeUInt16LE(16, 34);
pcm.write('data', 36); pcm.writeUInt32LE(n * 2, 40);
for (let i = 0; i < n; i++) {
    let v = Math.max(-1, Math.min(1, out[i] * g));
    pcm.writeInt16LE(Math.round(v * 32767), 44 + i * 2);
}
fs.writeFileSync('D:/baseball/ballgame-8bit-preview.wav', pcm);
console.log('written', pcm.length, 'bytes, peak', peak.toFixed(3));
