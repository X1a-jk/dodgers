# -*- coding: utf-8 -*-
"""投球武器库全面核对：
1. 提取 players\ 下全部报告的武器库现状（兼容 OLD/NEW 两种格式）
2. 从 MLB Stats API pitchArsenal 端点抓真实球种数据（2026，无数据回退 2025）
3. 逐人比对球种清单与球速，输出差异报告 data\_arsenal_audit.json
"""
import io, json, os, re, sys, time, urllib.request, urllib.parse

sys.stdout.reconfigure(encoding='utf-8')
BASE = r'D:\baseball\seasons\2026\players'
ROSTER = json.load(io.open(r'D:\baseball\data\season-roster.json', encoding='utf-8'))
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

PITCH_CN = {
    'FF': '四缝线速球', 'SI': '伸卡球（二缝线）', 'FC': '卡特球', 'SL': '滑球',
    'ST': '横扫滑球', 'CU': '曲球', 'KC': '曲球（指关节型）', 'CB': '曲球',
    'CH': '变速球', 'FS': '快速指叉球', 'FO': '分叉快速球', 'SV': '螺旋球',
    'KN': '蝴蝶球', 'SC': '螺旋球', 'EP': '鳗鱼球', 'FA': '快速球',
}
EN_KEYS = {  # 报告里的英文名 -> API code
    'four-seam fastball': 'FF', 'four-seamer': 'FF', 'fastball': 'FF', 'sinker': 'SI',
    'two-seam fastball': 'SI', 'cutter': 'FC', 'slider': 'SL', 'sweeper': 'ST',
    'curveball': 'CU', 'knuckle curve': 'KC', 'curve': 'CU', 'changeup': 'CH',
    'change': 'CH', 'splitter': 'FS', 'split-finger': 'FS', 'forkball': 'FO',
    'slurve': 'SL', 'screwball': 'SV', 'knuckleball': 'KN', 'slow curve': 'CU',
    'slurve slider': 'ST',
}
CN_TO_CODE = {v: k for k, v in PITCH_CN.items()}
CN_TO_CODE.update({'伸卡球': 'SI', '二缝线快速球': 'SI', '伸卡球 / 二缝线快速球': 'SI',
                   '四缝线快速球': 'FF', '滑球（横扫）': 'ST', '指叉球': 'FS'})


def get_json(url, tries=4):
    last = None
    for i in range(tries):
        try:
            with opener.open(url, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            last = e
            time.sleep(1.2 * (i + 1))
    raise RuntimeError(str(last))


def find_pid(name):
    for p in ROSTER['players']:
        if p['name'] == name:
            return p['id']
    q = urllib.parse.quote(name)
    d = get_json(f'https://statsapi.mlb.com/api/v1/people/search?names={q}&sportIds=1&activeStatus=Y')
    for person in d.get('people', []):
        if person.get('fullName', '').lower() == name.lower():
            return person['id']
    for person in d.get('people', []):
        return person['id']
    return None


def fetch_arsenal(pid):
    for season in (2026, 2025):
        try:
            d = get_json(f'https://statsapi.mlb.com/api/v1/people/{pid}/stats?stats=pitchArsenal&group=pitching&season={season}')
            splits = (d.get('stats') or [{}])[0].get('splits', [])
            out = []
            for s in splits:
                st = s.get('stat', {})
                t = st.get('type', {})
                if not st.get('count'):
                    continue
                out.append({
                    'code': t.get('code'), 'desc': t.get('description'),
                    'cn': PITCH_CN.get(t.get('code'), t.get('description')),
                    'count': st['count'], 'pct': round(st.get('percentage', 0) * 100, 1),
                    'avgSpeed': round(st.get('averageSpeed', 0), 1),
                })
            out.sort(key=lambda x: -x['count'])
            if out:
                return season, out
        except Exception:
            pass
    return None, []


def extract_current(html):
    """从报告 HTML 提取武器库条目，兼容两种格式。"""
    m = re.search(r'(?s)<div class="pitch-arsenal">(.*?)</div>\s*</div>\s*</div>', html)
    if not m:
        m = re.search(r'(?s)<div class="pitch-arsenal">(.*)', html)
    if not m:
        return []
    sec = m.group(1)
    items = []
    # NEW: <h3>名字 <span class="grade grade-x">G</span></h3> <div class="velocity">R</div>
    for pm in re.finditer(r'(?s)<div class="pitch-card">\s*<h3>(.*?)</h3>\s*(?:<div class="velocity">(.*?)</div>|<p><strong>球速：</strong>(.*?)</p>\s*<p><strong>评分：([^<]*)</strong></p>)', sec):
        h3 = pm.group(1)
        gm = re.search(r'class="grade grade-[^"]*">([^<]*)</span>', h3)
        grade = gm.group(1) if gm else (pm.group(4) or '?')
        name = re.sub(r'<span.*?</span>', '', h3).strip()
        vel = pm.group(2) or pm.group(3) or ''
        # 识别球种 code
        en = re.search(r'\(([A-Za-z\- /]+)\)', name)
        code = None
        if en:
            code = EN_KEYS.get(en.group(1).strip().lower())
        if not code:
            cn = re.sub(r'[\U0001F300-\U0001FAFF☀-➿\(\)A-Za-z /]', '', name).strip()
            cn = re.sub(r'^[^\u4e00-\u9fff]+', '', name.split('(')[0]).strip()
            code = CN_TO_CODE.get(cn) or CN_TO_CODE.get(name.split('(')[0].strip())
        items.append({'name': name, 'code': code, 'vel': vel.strip(), 'grade': grade.strip()})
    return items


def main():
    audit = {}
    slugs = sorted(os.listdir(BASE))
    for slug in slugs:
        d = os.path.join(BASE, slug)
        if not os.path.isdir(d):
            continue
        f = [x for x in os.listdir(d) if x.endswith('-scouting-report.html')]
        if not f:
            continue
        html = io.open(os.path.join(d, f[0]), encoding='utf-8').read()
        if '投球武器库' not in html:
            continue
        cfg_path = os.path.join(d, 'charts_config.json')
        pname = slug.replace('-', ' ').title()
        if os.path.exists(cfg_path):
            pname = json.load(io.open(cfg_path, encoding='utf-8')).get('player_name', pname)
        pid = find_pid(pname)
        season, truth = fetch_arsenal(pid) if pid else (None, [])
        current = extract_current(html)
        cur_codes = [c['code'] for c in current if c['code']]
        truth_sig = [t for t in truth if t['pct'] >= 2.0]
        truth_codes = [t['code'] for t in truth_sig]
        missing_in_report = [t for t in truth_sig if t['code'] not in cur_codes and t['code'] != 'PO']
        phantom = [c for c in current if c['code'] and c['code'] not in truth_codes]
        audit[slug] = {
            'name': pname, 'pid': pid, 'season': season,
            'current': current, 'truth': truth,
            'missingInReport': missing_in_report, 'phantom': phantom,
        }
        flag = '⚠️ ' if (missing_in_report or phantom) else '✓ '
        print(f"{flag}{slug:24s} 报告{len(current)}球 vs API{len(truth_sig)}球(≥2%)", end='')
        if phantom:
            print(f"  幽灵球: {[c['name'] for c in phantom]}", end='')
        if missing_in_report:
            print(f"  漏球: {[t['cn'] for t in missing_in_report]}", end='')
        print()
        time.sleep(0.25)
    out = r'D:\baseball\data\_arsenal_audit.json'
    json.dump(audit, io.open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\n已写', out)


if __name__ == '__main__':
    main()
