# -*- coding: utf-8 -*-
"""把 ORGAN_TUNES + song() + 面板项注入 index.html（锚点唯一匹配 + assert 计数）"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

idx_path = r'D:\baseball\index.html'
html = io.open(idx_path, encoding='utf-8-sig').read()
tunes = io.open(r'D:\baseball\data\_organ_tunes.js.txt', encoding='utf-8').read().rstrip()

SONG_METHOD = '''            /* 曲库播放器：每小节 [旋律[[midi,单位数]...], [根音,三音,五音]]，弱起小节和声 [0,0,0] */
            song(t0, spec) {
                let t = t0;
                spec.bars.forEach(([mel, harm]) => {
                    const barSec = mel.reduce((s, n) => s + n[1], 0) * spec.unit;
                    if (harm[0]) {
                        this.bass(harm[0], t, barSec * 0.4);
                        const pair = [harm[1], harm[2]];
                        if (spec.meter === 3) { this.stab(pair, t + barSec / 3); this.stab(pair, t + 2 * barSec / 3); }
                        else if (spec.meter === 2) { this.stab(pair, t + barSec / 2); }
                        else { this.stab(pair, t + barSec / 4); this.stab(pair, t + 3 * barSec / 4); }
                    }
                    mel.forEach(([m, l]) => {
                        if (m !== null) this.lead(m, t, l * spec.unit * 0.92);
                        t += l * spec.unit;
                    });
                });
                return t - t0 + 0.5;
            },
'''

ANCHOR1 = '''            stab(midis, t0) {
                midis.forEach(m => this.lead(m, t0, 0.12, 0.32));
            },
'''
assert html.count(ANCHOR1) == 1, 'anchor1 count %d' % html.count(ANCHOR1)
html = html.replace(ANCHOR1, ANCHOR1 + SONG_METHOD)

ANCHOR2 = '        };\n\n        function organToggle() {'
assert html.count(ANCHOR2) == 1, 'anchor2 count %d' % html.count(ANCHOR2)
html = html.replace(ANCHOR2, '        };\n\n' + tunes + '\n\n        function organToggle() {')

ANCHOR3 = '''                    secs = 96 * beat + 0.6;
                } else { return; }'''
assert html.count(ANCHOR3) == 1, 'anchor3 count %d' % html.count(ANCHOR3)
html = html.replace(ANCHOR3, '''                    secs = 96 * beat + 0.6;
                } else if (ORGAN_TUNES[key]) {
                    secs = this.song(t0, ORGAN_TUNES[key]);
                } else { return; }''')

ANCHOR4 = '''        <div class="organ-item" id="organ-ballgame" onclick="organPlay('ballgame')"><span>⚾</span> 第八局之歌 · Take Me Out to the Ball Game<em>8-bit · 约 40 秒</em></div>'''
assert html.count(ANCHOR4) == 1, 'anchor4 count %d' % html.count(ANCHOR4)
ITEMS = ANCHOR4 + '''
        <div class="organ-item" id="organ-banner" onclick="organPlay('banner')"><span>🇺🇸</span> 星条旗国歌<em>8-bit · 约 41 秒</em></div>
        <div class="organ-item" id="organ-ssf" onclick="organPlay('ssf')"><span>🎺</span> 星条旗永不落<em>8-bit · 约 37 秒</em></div>
        <div class="organ-item" id="organ-grandold" onclick="organPlay('grandold')"><span>🚩</span> Grand Old Flag<em>8-bit · 约 29 秒</em></div>
        <div class="organ-item" id="organ-saints" onclick="organPlay('saints')"><span>😇</span> When the Saints<em>8-bit · 约 19 秒</em></div>'''
html = html.replace(ANCHOR4, ITEMS)

io.open(idx_path, 'w', encoding='utf-8', newline='\n').write(html)
print('INJECT_OK, new size', len(html))
