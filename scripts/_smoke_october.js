// 冒烟：applyOctoberTheme 窗口逻辑（11/15 关、10/20 开、11/5 开、10/1 开）
const fs = require('fs');
const html = fs.readFileSync('D:/baseball/index.html', 'utf8');
const i = html.indexOf('async function applyOctoberTheme');
const j = html.indexOf('/* 主题失败不影响功能 */ }\n        }', i) + '/* 主题失败不影响功能 */ }\n        }'.length;
const fn = html.slice(i, j);

function runWithDate(y, m, d) {
    const classes = new Set();
    const banner = { style: { display: 'none' } };
    global.$ = sel => (sel === '#october-banner' ? banner : null);
    global.document = { body: { classList: { add: c => classes.add(c), remove: c => classes.delete(c) } } };
    const RealDate = Date;
    global.Date = class extends RealDate {
        constructor(...a) { super(...a); }
        static now() { return new RealDate(y, m - 1, d).getTime(); }
    };
    global.Date.prototype = RealDate.prototype;
    // new Date() 无参 → 用 fake now
    const patched = fn.replace(/new Date\(\)/g, `new Date(${y}, ${m - 1}, ${d})`);
    const f = eval('(' + patched.replace('async function applyOctoberTheme', 'async function') + ')');
    return f().then(() => ({ on: classes.has('october'), banner: banner.style.display }));
}

(async () => {
    const cases = [
        [2026, 11, 15, false], [2026, 10, 20, true], [2026, 11, 5, true],
        [2026, 10, 1, true], [2026, 11, 11, false], [2026, 9, 30, false],
    ];
    let ok = true;
    for (const [y, m, d, exp] of cases) {
        const r = await runWithDate(y, m, d);
        const pass = r.on === exp;
        console.log(`${y}-${m}-${d} -> october=${r.on} (exp ${exp}) ${pass ? 'OK' : 'FAIL'}`);
        if (!pass) ok = false;
    }
    console.log(ok ? 'SMOKE_OK october-window' : 'SMOKE_FAIL');
    process.exit(ok ? 0 : 1);
})();
