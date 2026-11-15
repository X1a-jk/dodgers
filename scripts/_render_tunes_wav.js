// 离线渲染 4 首新曲试听（数据与门户一致，1 秒间隔连播）
const fs = require('fs');
const html = fs.readFileSync('D:/baseball/index.html', 'utf8');

const m = html.match(/const ORGAN_TUNES = \{[\s\S]*?\n        \};/);
if (!m) throw new Error('ORGAN_TUNES not found');
const ORGAN_TUNES = eval('(' + m[0].replace('const ORGAN_TUNES =', '').replace(/;\s*$/, '') + ')');

const SR = 22050;
const seq = ['banner', 'ssf', 'grandold', 'saints'];
let span = 0;
const songs = seq.map(k => {
    const spec = ORGAN_TUNES[k];
    let u = 0;
    const ev = [];
    spec.bars.forEach(([mel, harm]) => {
        const barSec = mel.reduce((s, n) => s + n[1], 0) * spec.unit;
        const t = u * spec.unit;
        if (harm[0]) {
            ev.push({ k: 'bass', m: harm[0], t, d: barSec * 0.4 });
            const pair = [harm[1], harm[2]];
            if (spec.meter === 3) { ev.push({ k: 'stab', m: pair, t: t + barSec / 3 }); ev.push({ k: 'stab', m: pair, t: t + 2 * barSec / 3 }); }
            else if (spec.meter === 2) { ev.push({ k: 'stab', m: pair, t: t + barSec / 2 }); }
            else { ev.push({ k: 'stab', m: pair, t: t + barSec / 4 }); ev.push({ k: 'stab', m: pair, t: t + 3 * barSec / 4 }); }
        }
        mel.forEach(([mm, l]) => { if (mm !== null) ev.push({ k: 'lead', m: mm, t: t, d: l * spec.unit * 0.92 }); u += l; });
    });
    const dur = u * spec.unit + 0.5;
    return { key: k, ev, dur };
});
const total = songs.reduce((s, x) => s + x.dur + 1, 0);
const n = Math.floor(SR * total);
const out = new Float32Array(n);

function envAmp(t, dur, peak) {
    const atk = 0.008, decT = Math.min(0.25, dur * 0.5), relStart = Math.max(0.03, dur - 0.07);
    if (t < 0 || t > dur) return 0;
    if (t < atk) return peak * (t / atk);
    if (t < atk + decT) return peak * Math.pow(0.55, (t - atk) / decT);
    if (t < relStart) return peak * 0.55;
    return Math.max(peak * 0.55 * Math.pow(0.0001 / (peak * 0.55), (t - relStart) / (dur - relStart)), 0);
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
        const sq = 2 * (2 * Math.floor(ph) - Math.floor(2 * ph) + 1) - 1;
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
        const amp = t < 0.012 ? peak * t / 0.012 : peak * Math.pow(0.0001 / peak, (t - 0.012) / (dur - 0.012));
        out[s] += amp * (2 / Math.PI) * Math.asin(Math.sin(2 * Math.PI * f * s / SR));
    }
}
let offset = 0;
songs.forEach(x => {
    x.ev.forEach(e => {
        if (e.k === 'lead') addLead(e.m, offset + e.t, e.d, 1);
        else if (e.k === 'bass') addBass(e.m, offset + e.t, e.d);
        else e.m.forEach(mm => addLead(mm, offset + e.t, 0.12, 0.32));
    });
    console.log(x.key, 'dur', x.dur.toFixed(1) + 's', 'events', x.ev.length);
    offset += x.dur + 1;
});
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
    const v = Math.max(-1, Math.min(1, out[i] * g));
    pcm.writeInt16LE(Math.round(v * 32767), 44 + i * 2);
}
fs.writeFileSync('D:/baseball/organ-tunes-preview.wav', pcm);
console.log('written', pcm.length, 'bytes,', total.toFixed(1) + 's');
