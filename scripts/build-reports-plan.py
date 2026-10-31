# -*- coding: utf-8 -*-
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

roster = json.load(open(r'D:\baseball\data\season-roster.json', encoding='utf-8'))
ps = json.load(open(r'D:\baseball\data\ps-participants.json', encoding='utf-8'))
rep = r'D:\baseball\report'

def has_report(name):
    slug = name.lower().replace(' ', '-').replace('.', '')
    folder = os.path.join(rep, slug)
    return os.path.isdir(folder) and len(os.listdir(folder)) > 0

STATUS_ORDER = {'活跃': 0, 'IL-60': 1, 'Forty Man': 2, '小联盟': 3, 'Outright': 4, '已离队': 5}

players = sorted(roster['players'],
                 key=lambda p: (STATUS_ORDER.get(p['statusCn'], 9), -p['g']))

L = []
L.append('# 球员报告更新计划（总控表）')
L.append('')
L.append('> 赛季收官阶段用：每更新完一个球员报告，把名字前的 `[ ]` 打成 `[x]`。')
L.append('> 按赛季组织，每个赛季分 **常规赛**、**季后赛** 两批。')
L.append('> 相关工具：报告生成（scouting-report skill / scripts\\generate-missing-reports.py）、')
L.append('> 批次封存（复制 report\\ → seasons\\YYYY\\players-<批次>\\）、门户刷新（portal\\update-portal.py）。')
L.append('')
L.append('## 使用规则')
L.append('')
L.append('1. **更新对象**：以 `data\\season-roster.json` 当年出场名单为准（本表已按 2026-10-15 快照生成）。')
L.append('2. **打勾时机**：报告按赛季最终数据重新生成/核对完毕（文件齐全：md + html + 图表）后打勾。')
L.append('   「现状」列的 ✅ 只表示报告目录已存在，不代表是赛季最终版。')
L.append('3. **批次封存**：该批全部打勾后——')
L.append('   - 常规赛批：复制 `report\\` → `seasons\\YYYY\\players-regular\\`')
L.append('   - 季后赛批（道奇淘汰后定稿）：复制 `report\\` → `seasons\\YYYY\\players-postseason\\`')
L.append('   - 然后跑 `python portal\\update-portal.py`，报告页版本选择器自动出现新批次')
L.append('4. **archive-season.py 年终封存**会把 `report\\` 整体迁为 `seasons\\YYYY\\players\\`（赛季总结版）。')
L.append('')

# ---------- 2026 常规赛批 ----------
L.append('---')
L.append('')
L.append('# 2026 赛季')
L.append('')
L.append(f'## 常规赛批（{len(players)} 人，数据快照：{roster["generatedAt"][:10]}）')
L.append('')
missing = [p for p in players if not has_report(p['name'])]
done = [p for p in players if has_report(p['name'])]
L.append(f'> 进度：0 / {len(players)}　|　已有报告目录 {len(done)} 人，**缺报告 {len(missing)} 人**')
L.append('')

cur_status = None
for p in players:
    if p['statusCn'] != cur_status:
        cur_status = p['statusCn']
        L.append(f'### {cur_status}')
        L.append('')
        L.append('| 完成 | 球员 | 位置 | 出场 | 赛季数据 | 现状 |')
        L.append('|---|---|---|---|---|---|')
    b, t = p.get('bat'), p.get('pit')
    stats = []
    if b:
        stats.append(f".{b['avg'].lstrip('.')} / {b['hr']}HR / {b['rbi']}RBI / OPS {b.get('ops','-')}")
    if t:
        stats.append(f"{t.get('era','-')} ERA, {t.get('w','-')}-{t.get('l','-')}")
    stat = '<br>'.join(stats) if stats else '—'
    state = '✅ 有目录' if has_report(p['name']) else '❌ 无报告'
    L.append(f"| [ ] | {p['name']} | {p['pos']} | {p['g']} | {stat} | {state} |")

# ---------- 2026 季后赛批 ----------
L.append('---')
L.append('')
L.append(f'## 季后赛批（进行中 · 截至 NLCS G3 已出场 {len(ps)} 人）')
L.append('')
L.append('> ⚠️ 道奇仍在季后赛中（NLCS 0-3），**名单随每轮更新**；道奇淘汰后做最终核对再生成报告。')
L.append('> 出场数据：7 场真实 boxscore 汇总（NLDS 4 场 + NLCS 3 场）。')
L.append('')
L.append('| 完成 | 球员 | 出场 | 角色 |')
L.append('|---|---|---|---|')
for name, e in sorted(ps.items(), key=lambda kv: (-kv[1]['games'], kv[0])):
    roles = '/'.join([r for r, ok in (('打', e['bat']), ('投', e['pit'])) if ok])
    L.append(f"| [ ] | {name} | {e['games']} | {roles} |")
L.append('')
L.append('> 赛后核对项：')
L.append('> - [ ] 道奇淘汰后重新跑出场名单汇总（全部季后赛场次），补进新增出场球员')
L.append('> - [ ] 确认世界大赛出场名单（如晋级）')
L.append('> - [ ] 全部核对完 → 复制 report\\ → seasons\\2026\\players-postseason\\ → update-portal.py')
L.append('')

# ---------- 未来赛季模板 ----------
L.append('---')
L.append('')
L.append('# 未来赛季（模板）')
L.append('')
L.append('> 新赛季开赛复制本文件结构：')
L.append('> 1. 跑 `scripts\\fetch-season-roster.py` 生成当年出场名单')
L.append('> 2. 用脚本重新生成本表的常规赛批名单（可复用本文件生成逻辑）')
L.append('> 3. 季后赛批等外卡名单确定后从 boxscore 汇总（复用 `scripts\\_ps-participants.py` 思路）')
L.append('')
L.append('```')
L.append('## YYYY 赛季')
L.append('')
L.append('### 常规赛批（N 人）')
L.append('| 完成 | 球员 | 位置 | 出场 | 赛季数据 | 现状 |')
L.append('| ... |')
L.append('')
L.append('### 季后赛批（N 人）')
L.append('| 完成 | 球员 | 出场 | 角色 |')
L.append('| ... |')
L.append('```')
L.append('')
L.append('---')
L.append(f'*生成时间：2026-10-15（出场名单快照 {roster["generatedAt"]}）*')

open(r'D:\baseball\PLAYER-REPORTS-PLAN.md', 'w', encoding='utf-8').write('\n'.join(L))
print('written, lines:', len(L))
print('missing reports:', [p['name'] for p in missing])
