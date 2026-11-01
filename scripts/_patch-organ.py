# -*- coding: utf-8 -*-
"""球场风琴：Web Audio 实时合成（零音频文件/零版权风险）。
浮动 🎵 按钮 + 三个 chip（胜利小调 / Charge / 人浪节拍），补丁注入 index.html。"""
import shutil, io, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(BASE, 'index.html')
BAK = P + '.bak-pre-organ'

html = io.open(P, encoding='utf-8').read()
shutil.copy(P, BAK)

CSS = """
        /* ===== 球场风琴 (organ-*) ===== */
        .organ-fab {
            position: fixed; right: 22px; bottom: 22px; z-index: 990;
            width: 48px; height: 48px; border-radius: 50%;
            background: linear-gradient(135deg, #1e88e5, #0d47a1);
            border: 1px solid rgba(79, 195, 247, 0.5);
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.45);
            display: flex; align-items: center; justify-content: center;
            font-size: 1.25rem; cursor: pointer; transition: transform .15s, box-shadow .15s;
            user-select: none;
        }
        .organ-fab:hover { transform: scale(1.08); box-shadow: 0 6px 22px rgba(30, 136, 229, 0.5); }
        .organ-fab.playing { background: linear-gradient(135deg, #ef6c00, #b71c1c); }
        .organ-panel {
            position: fixed; right: 22px; bottom: 80px; z-index: 990;
            width: 248px; border-radius: 14px; overflow: hidden;
            background: rgba(13, 27, 48, 0.96); border: 1px solid rgba(79, 195, 247, 0.35);
            box-shadow: 0 10px 34px rgba(0, 0, 0, 0.55);
            display: none;
        }
        .organ-panel.open { display: block; }
        .organ-title { padding: 12px 16px 8px; font-weight: 700; font-size: 0.9rem; }
        .organ-title span { display: block; font-weight: 400; font-size: 0.68rem; color: var(--text-muted); margin-top: 2px; }
        .organ-item {
            padding: 10px 16px; font-size: 0.86rem; cursor: pointer;
            display: flex; align-items: center; gap: 10px;
            border-left: 3px solid transparent; transition: background .12s;
        }
        .organ-item:hover { background: rgba(255, 255, 255, 0.06); }
        .organ-item.on { background: rgba(30, 136, 229, 0.18); border-left-color: #4fc3f7; }
        .organ-item em { margin-left: auto; font-style: normal; font-size: 0.7rem; color: var(--text-muted); }
        .organ-foot { padding: 8px 16px 12px; font-size: 0.68rem; color: var(--text-muted); border-top: 1px solid var(--border); margin-top: 6px; }
        /* ===== 球场风琴 END ===== */
"""

JS = r"""
        /* ---------- 球场风琴（Web Audio 实时合成，零音频文件） ---------- */
        const ORGAN = {
            ctx: null, master: null, current: null,
            ensure() {
                if (!this.ctx) {
                    const AC = window.AudioContext || window.webkitAudioContext;
                    this.ctx = new AC();
                    this.master = this.ctx.createGain();
                    this.master.gain.value = 0.22;
                    this.master.connect(this.ctx.destination);
                }
                if (this.ctx.state === 'suspended') this.ctx.resume();
            },
            note(midi, t0, dur, vel) {
                const f = 440 * Math.pow(2, (midi - 69) / 12);
                const v = (vel == null ? 1 : vel);
                const g = this.ctx.createGain();
                g.connect(this.master);
                g.gain.setValueAtTime(0.0001, t0);
                g.gain.exponentialRampToValueAtTime(0.35 * v, t0 + 0.025);
                g.gain.setValueAtTime(0.35 * v, t0 + Math.max(0.03, dur - 0.09));
                g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
                [[1, .5], [2, .26], [3, .14], [4, .07]].forEach(([h, a]) => {
                    const o = this.ctx.createOscillator();
                    o.type = 'sine';
                    o.frequency.value = f * h;
                    const og = this.ctx.createGain();
                    og.gain.value = a;
                    o.connect(og); og.connect(g);
                    o.start(t0); o.stop(t0 + dur + 0.05);
                });
            },
            chord(midis, t0, dur, vel) { midis.forEach(m => this.note(m, t0, dur, vel)); },
            clap(t0) {
                const len = Math.floor(this.ctx.sampleRate * 0.2);
                const buf = this.ctx.createBuffer(1, len, this.ctx.sampleRate);
                const d = buf.getChannelData(0);
                for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 2.4);
                const src = this.ctx.createBufferSource();
                src.buffer = buf;
                const bp = this.ctx.createBiquadFilter();
                bp.type = 'bandpass'; bp.frequency.value = 1400; bp.Q.value = 0.9;
                const g = this.ctx.createGain(); g.gain.value = 0.9;
                src.connect(bp); bp.connect(g); g.connect(this.master);
                src.start(t0);
            },
            stop() {
                if (this.current && this.current.timer) clearTimeout(this.current.timer);
                this.current = null;
                document.querySelectorAll('.organ-item').forEach(el => el.classList.remove('on'));
                const fab = document.getElementById('organ-fab');
                if (fab) fab.classList.remove('playing');
            },
            start(key) {
                this.ensure();
                this.stop();
                const t0 = this.ctx.currentTime + 0.06;
                let secs = 0;
                if (key === 'victory') {
                    // 胜利小调：上行动机 ×2 → 终止和弦
                    this.note(60, t0, 0.2);            // C4
                    this.note(64, t0 + 0.2, 0.2);      // E4
                    this.note(67, t0 + 0.4, 0.2);      // G4
                    this.note(72, t0 + 0.6, 0.42);     // C5
                    this.note(67, t0 + 1.1, 0.18);     // G4
                    this.note(72, t0 + 1.3, 0.6);      // C5
                    this.chord([72, 76, 79, 84], t0 + 2.05, 1.1, 1.1); // C 大和弦收尾
                    secs = 3.3;
                } else if (key === 'charge') {
                    // Charge 助威：五连顿音 → 号召和弦
                    this.note(55, t0, 0.1);            // G3
                    this.note(55, t0 + 0.12, 0.1);
                    this.note(55, t0 + 0.24, 0.1);
                    this.note(55, t0 + 0.36, 0.1);
                    this.note(60, t0 + 0.5, 0.3);      // C4
                    this.note(55, t0 + 0.84, 0.14);    // G3
                    this.chord([60, 64, 67, 72], t0 + 1.05, 1.0, 1.15); // CHARGE!
                    secs = 2.3;
                } else if (key === 'clap') {
                    // 人浪节拍：100 BPM × 8 小节，2/4 拍手 + 变化小节
                    const beat = 0.6;
                    const barPat = [
                        [2, 4], [2, 4], [1, 2, 3, 4], [2, 4, 4.5],
                        [2, 4], [2, 4], [1, 2, 3, 4], [2, 2.5, 4, 4.5],
                    ];
                    let beats = 0;
                    for (let bar = 0; bar < 8; bar++) {
                        for (const b of barPat[bar % barPat.length]) {
                            this.clap(t0 + (beats + b - 1) * beat);
                        }
                        beats += 4;
                    }
                    secs = beats * beat + 0.5;
                } else { return; }
                this.current = { key, timer: setTimeout(() => this.stop(), secs * 1000) };
                const item = document.getElementById('organ-' + key);
                if (item) item.classList.add('on');
                const fab = document.getElementById('organ-fab');
                if (fab) fab.classList.add('playing');
            }
        };

        function organToggle() {
            const p = document.getElementById('organ-panel');
            if (p) p.classList.toggle('open');
        }
        function organPlay(key) {
            if (ORGAN.current && ORGAN.current.key === key) { ORGAN.stop(); return; }
            ORGAN.start(key);
        }
        document.addEventListener('keydown', e => {
            if (e.key === 'Escape' && ORGAN.current) ORGAN.stop();
        });
        /* ---------- 球场风琴 END ---------- */
"""

HTML_WIDGET = """
    <div class="organ-fab" id="organ-fab" onclick="organToggle()" title="球场风琴">🎵</div>
    <div class="organ-panel" id="organ-panel">
        <div class="organ-title">🏟️ 球场风琴<span>Web Audio 实时合成 · 零音频文件</span></div>
        <div class="organ-item" id="organ-victory" onclick="organPlay('victory')"><span>🏆</span> 胜利小调<em>3 秒</em></div>
        <div class="organ-item" id="organ-charge" onclick="organPlay('charge')"><span>📣</span> Charge 助威<em>2 秒</em></div>
        <div class="organ-item" id="organ-clap" onclick="organPlay('clap')"><span>👏</span> 人浪节拍<em>循环 19 秒</em></div>
        <div class="organ-foot">再点一次停止 · Esc 也可停止</div>
    </div>
"""


def patch(anchor, repl, count=1):
    global html
    n = html.count(anchor)
    assert n == count, '锚点计数 %d != %d: %r' % (n, count, anchor[:60])
    html = html.replace(anchor, repl)
    print('  [OK] %r' % anchor.strip()[:50])

# CSS：插在休赛期 CSS 之前
patch("        /* ===== 休赛期转会中心 (os-*) ===== */",
      CSS + "\n        /* ===== 休赛期转会中心 (os-*) ===== */")

# JS：插在 // Initialize 之前
patch("        // Initialize\n        $$('.nav-item')",
      JS + "\n        // Initialize\n        $$('.nav-item')")

# HTML：</body> 前
patch("</body>\n</html>", HTML_WIDGET + "</body>\n</html>")

io.open(P, 'w', encoding='utf-8', newline='').write(html)
print('写入 %s (%d bytes)' % (P, len(html.encode('utf-8'))))
