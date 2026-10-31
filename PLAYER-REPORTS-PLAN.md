# 球员报告更新计划（总控表）

> 赛季收官阶段用：每更新完一个球员报告，把名字前的 `[ ]` 打成 `[x]`。
> 按赛季组织，每个赛季分 **常规赛**、**季后赛** 两批。
> 相关工具：报告生成（scouting-report skill / scripts\generate-missing-reports.py）、
> 批次封存（复制 report\ → seasons\YYYY\players-<批次>\）、门户刷新（portal\update-portal.py）。

## 使用规则

1. **更新对象**：以 `data\season-roster.json` 当年出场名单为准（本表已按 2026-10-15 快照生成）。
2. **打勾时机**：报告按赛季最终数据重新生成/核对完毕（文件齐全：md + html + 图表）后打勾。
   「现状」列的 ✅ 只表示报告目录已存在，不代表是赛季最终版。
3. **批次封存**：该批全部打勾后——
   - 常规赛批：复制 `report\` → `seasons\YYYY\players-regular\`
   - 季后赛批（道奇淘汰后定稿）：复制 `report\` → `seasons\YYYY\players-postseason\`
   - 然后跑 `python portal\update-portal.py`，报告页版本选择器自动出现新批次
4. **archive-season.py 年终封存**会把 `report\` 整体迁为 `seasons\YYYY\players\`（赛季总结版）。

---

# 2026 赛季

## 常规赛批（53 人，数据快照：2026-10-15）

> 进度：**53 / 53 全部完成（2026-10-28）**　|　旧版风格报告已从 report.bak-20261017 还原，逐人在旧版基础上更新最终数据（常规赛+季后赛）后打勾。
> 53 人全部验证通过（verify-reports.py 0 bad）。批次封存已用最终版重同步 seasons\2026\players-regular\。
> （数据驱动分析引擎：备注/优劣/评分全部由最终数据生成），8 人此前已补齐；53 人全部验证通过
> （md + html + 图表 ≥3 + 数据抽查一致）。已封存 seasons\2026\players-regular\。
>
> ✅ **缺报告问题已解决（2026-10-17）**：generate-missing-reports.py 已修——main() 单人 try/except、API 6 次重试、slug 去重音。本次 8/8 成功（含首次补的 Espinal / Robinson / Irvin / Eder）。
> 另注：本机注册表代理 127.0.0.1:7892 已失效（连接拒绝），脚本已改为 ProxyHandler({}) 直连。教训全文见 MEMORY.md「球员报告生成经验」。

### 活跃

| 完成 | 球员 | 位置 | 出场 | 赛季数据 | 现状 |
|---|---|---|---|---|---|
| [x] | Kyle Tucker | RF | 154 | .233 / 17HR / 70RBI / OPS .715 | ✅ 10-17 旧版更新 |
| [x] | Freddie Freeman | 1B | 153 | .288 / 16HR / 70RBI / OPS .792 | ✅ 10-17 旧版更新 |
| [x] | Max Muncy | 3B | 149 | .252 / 29HR / 76RBI / OPS .838 | ✅ 10-17 旧版更新 |
| [x] | Shohei Ohtani | DH | 139 | .275 / 30HR / 81RBI / OPS .889<br>1.79 ERA, 8-2 | ✅ 10-24 旧版更新 |
| [x] | Andy Pages | CF | 134 | .274 / 23HR / 85RBI / OPS .811 | ✅ 10-24 旧版更新 |
| [x] | Teoscar Hernández | LF | 125 | .267 / 16HR / 64RBI / OPS .759 | ✅ 10-24 旧版重写 |
| [x] | Mookie Betts | SS | 123 | .257 / 23HR / 69RBI / OPS .780 | ✅ 10-24 旧版重写 |
| [x] | Miguel Rojas | 2B | 107 | .267 / 4HR / 23RBI / OPS .703<br>13.50 ERA, 0-0 | ✅ 10-17 旧版更新 |
| [x] | Tommy Edman | 2B | 84 | .247 / 8HR / 42RBI / OPS .714 | ✅ 10-24 旧版重写 |
| [x] | Will Smith | C | 73 | .260 / 10HR / 34RBI / OPS .781 | ✅ 10-24 旧版重写 |
| [x] | Alex Vesia | P | 72 | 2.64 ERA, 3-1 | ✅ 10-24 旧版重写 |
| [x] | Tanner Scott | P | 69 | 2.69 ERA, 1-6 | ✅ 10-24 旧版重写 |
| [x] | Edgardo Henriquez | P | 61 | 2.85 ERA, 4-1 | ✅ 10-24 旧版重写 |
| [x] | Enrique Hernández | 3B | 41 | .222 / 4HR / 12RBI / OPS .671<br>0.00 ERA, 0-0 | ✅ 10-24 旧版重写 |
| [x] | Hunter Feduccia | C | 33 | .197 / 1HR / 7RBI / OPS .585 | ✅ 10-24 旧版重写 |
| [x] | Evan Phillips | P | 31 | 3.46 ERA, 3-2 | ✅ 10-24 旧版重写 |
| [x] | Yoshinobu Yamamoto | P | 28 | 2.53 ERA, 14-9 | ✅ 10-24 旧版重写 |
| [x] | Brock Stewart | P | 28 | 2.70 ERA, 1-2 | ✅ 10-24 旧版重写 |
| [x] | Justin Wrobleski | P | 28 | 3.66 ERA, 12-5 | ✅ 10-24 旧版重写 |
| [x] | Roki Sasaki | P | 26 | 4.49 ERA, 5-5 | ✅ 10-24 旧版重写 |
| [x] | Edwin Díaz | P | 21 | 8.68 ERA, 2-2 | ✅ 10-24 旧版重写 |
| [x] | Tyler Glasnow | P | 13 | 3.53 ERA, 5-2 | ✅ 10-24 旧版重写 |
| [x] | Josue De Paula | DH | 11 | .323 / 1HR / 7RBI / OPS 1.081 | ✅ 10-24 旧版重写 |
| [x] | Tarik Skubal | P | 10 | 2.61 ERA, 5-2 | ✅ 10-24 旧版重写 |
| [x] | Blake Snell | P | 9 | 1.90 ERA, 4-1 | ✅ 10-24 旧版重写 |
| [x] | Kris Bubic | P | 5 | 0.00 ERA, 1-0 | ✅ 10-24 旧版重写 |
### IL-60

| 完成 | 球员 | 位置 | 出场 | 赛季数据 | 现状 |
|---|---|---|---|---|---|
| [x] | Will Klein | P | 36 | 3.67 ERA, 3-4 | ✅ 10-24 旧版重写 |
| [x] | Eric Lauer | P | 14 | 4.50 ERA, 7-2 | ✅ 10-24 旧版重写 |
| [x] | Ben Casparius | P | 5 | 9.64 ERA, 0-1 | ✅ 10-24 旧版重写 |
### Forty Man

| 完成 | 球员 | 位置 | 出场 | 赛季数据 | 现状 |
|---|---|---|---|---|---|
| [x] | Alex Freeland | 2B | 89 | .234 / 4HR / 21RBI / OPS .652 | ✅ 10-24 旧版重写 |
| [x] | Alex Call | LF | 88 | .233 / 1HR / 20RBI / OPS .656 | ✅ 10-24 旧版重写 |
| [x] | Dalton Rushing | C | 80 | .246 / 12HR / 36RBI / OPS .788 | ✅ 10-24 旧版重写 |
| [x] | Jack Dreyer | P | 67 | 3.20 ERA, 5-2 | ✅ 10-24 旧版重写 |
| [x] | Kyle Hurt | P | 44 | 4.14 ERA, 4-1 | ✅ 10-24 旧版重写 |
| [x] | Hyeseong Kim | SS | 43 | .259 / 1HR / 11RBI / OPS .651 | ✅ 10-24 旧版重写 |
| [x] | Blake Treinen | P | 36 | 3.64 ERA, 4-1 | ✅ 10-24 旧版重写 |
| [x] | Emmet Sheehan | P | 23 | 4.57 ERA, 5-8 | ✅ 10-24 旧版重写 |
| [x] | Eliezer Alfonzo | C | 13 | .179 / 0HR / 4RBI / OPS .429 | ? ✅ 10-26 旧版重写 |
| [x] | Paul Gervase | P | 4 | 2.35 ERA, 0-0 | ? ✅ 10-26 旧版重写 |
| [x] | Landon Knack | P | 4 | 3.86 ERA, 1-0 | ? ✅ 10-26 旧版重写 |
| [x] | Bobby Miller | P | 3 | 3.68 ERA, 1-0 | ? ✅ 10-26 旧版重写 |
### 小联盟

| 完成 | 球员 | 位置 | 出场 | 赛季数据 | 现状 |
|---|---|---|---|---|---|
| [x] | Seth Halvorsen | P | 11 | 8.10 ERA, 1-1 | ✅ 10-27 旧版重写，10-28 核对 |
### Outright

| 完成 | 球员 | 位置 | 出场 | 赛季数据 | 现状 |
|---|---|---|---|---|---|
| [x] | Santiago Espinal | 3B | 36 | .268 / 1HR / 7RBI / OPS .651 | ✅ 10-27 旧版重写，10-28 核对 |
| [x] | Ben Rortvedt | C | 16 | .185 / 0HR / 1RBI / OPS .370 | ✅ 10-27 旧版重写，10-28 核对 |
| [x] | Jonathan Hernández | P | 16 | 5.68 ERA, 0-0 | ✅ 10-27 旧版重写，10-28 核对 |
| [x] | Chuckie Robinson | C | 8 | .087 / 0HR / 1RBI / OPS .174 | ✅ 10-27 旧版重写，10-28 核对 |
| [x] | Alek Thomas | CF | 7 | .211 / 0HR / 3RBI / OPS .513 | ✅ 10-27 旧版重写，10-28 核对 |
| [x] | Charlie Barnes | P | 4 | 6.30 ERA, 0-1 | ✅ 10-28 旧版重写（评分区转 stat-card + 图表补齐） |
| [x] | Cole Irvin | P | 1 | 9.00 ERA, 0-1 | ✅ 10-27 旧版重写，10-28 核对 |
### 已离队

| 完成 | 球员 | 位置 | 出场 | 赛季数据 | 现状 |
|---|---|---|---|---|---|
| [x] | Ryan Ward | LF | 20 | .218 / 3HR / 12RBI / OPS .738 | ✅ 10-27 旧版重写，10-28 核对 |
| [x] | Wyatt Mills | P | 6 | 5.68 ERA, 0-0 | ✅ 10-27 旧版重写，10-28 核对 |
| [x] | Jake Eder | P | 4 | 2.25 ERA, 1-0 | ✅ 10-28 旧版重写（html 10-27 + md/图表 10-28 补齐） |
| [x] | Chayce McDermott | P | 2 | 7.71 ERA, 0-0 | ✅ 10-28 旧版更新（赛季收官补丁 + md/图表补齐） |
---

## 季后赛批（25 人，2026-10-17 定稿）

> ✅ **已完成**：道奇 NLDS 3-1 晋级、NLCS 0-4 止步（共 8 场）。25 人出场名单从全部 8 场真实 boxscore
> 重新汇总（`scripts\fetch-ps-final.py`），报告已追加「2026 季后赛表现」章节（`scripts\generate-ps-reports.py`），
> 25/25 验证通过，已封存 `seasons\2026\players-postseason\`，门户出现「2026 季后赛版」。

| 完成 | 球员 | 出场 | 角色 |
|---|---|---|---|
| [x] | Will Smith | 8 | 打 |
| [x] | Kyle Tucker | 8 | 打 |
| [x] | Max Muncy | 8 | 打 |
| [x] | Freddie Freeman | 8 | 打 |
| [x] | Shohei Ohtani | 8 | 打 |
| [x] | Teoscar Hernández | 8 | 打 |
| [x] | Andy Pages | 8 | 打 |
| [x] | Mookie Betts | 8 | 打 |
| [x] | Tommy Edman | 7 | 打 |
| [x] | Tanner Scott | 6 | 投 |
| [x] | Alex Vesia | 5 | 投 |
| [x] | Evan Phillips | 5 | 投 |
| [x] | Enrique Hernández | 5 | 打 |
| [x] | Edwin Díaz | 4 | 投 |
| [x] | Miguel Rojas | 4 | 打 |
| [x] | Brock Stewart | 3 | 投 |
| [x] | Edgardo Henriquez | 3 | 投 |
| [x] | Josue De Paula | 3 | 打 |
| [x] | Roki Sasaki | 3 | 投 |
| [x] | Tarik Skubal | 2 | 投 |
| [x] | Kris Bubic | 2 | 投 |
| [x] | Blake Snell | 2 | 投 |
| [x] | Yoshinobu Yamamoto | 2 | 投 |
| [x] | Tyler Glasnow | 2 | 投 |
| [x] | Justin Wrobleski | 2 | 投 |

> 赛后核对项：
> - [x] 道奇淘汰后重新跑出场名单汇总（全部季后赛场次）——25 人，与 NLCS G3 快照同名单，出场数有更新
> - [x] 世界大赛出场名单——未晋级（NLCS 0-4），无需处理
> - [x] 全部核对完 → 复制 report\ → seasons\2026\players-postseason\ → update-portal.py

---

### ⚠️ 头图风格返工（2026-10-18）

**用户裁定：** 报告头图用旧版风格（`report.bak-20261017\kyle-tucker\tucker_report_cover.png`：深蓝 #1a1a2e 底、居中排版、橙色 SCOUTING REPORT 2026、8 格数据、中文标语、页脚），**不要** 10-17 最终版生成的新风格（笑脸印章式，`generate-final-reports.py` 的 generate_cover）。

**已执行：**
- 新脚本 `scripts\regen-covers-old-style.py`：数据全本地（final-stats.json + season-roster.json + depth-chart.json，零网络），53 人全部重绘（含已打勾的 Tucker / Freeman / Muncy / Rojas 四人返工），目录下所有 `*_report_cover.png`（含短名残留）统一覆盖，HTML 不动。
- 封存批次同步：`seasons\2026\players-regular`（53 人）与 `players-postseason`（25 人）封面全部覆盖为旧版风格。
- Charlie Barnes 的 HTML 无 <img> 引用（历史遗留，不显示头图），封面文件仍补齐旧版风格（`_oneoff-barnes-cover.py`）。

**技术教训：**
1. 同一球员目录可能并存两个封面文件（如 `tucker_report_cover.png` 与 `kyle-tucker_report_cover.png`），且 **live report\ 与封存批次的 HTML 引用文件名不一致**（live 引短名、封存引 slug 名）——同步时必须把目录下所有 `*_report_cover.png` 全部复制，不能只复制 HTML 引用的那个（`_oneoff-sync-covers.py` 的校验逻辑可复用）。
2. 国联投手有打击数据（PA 很少），判断"二刀流"必须用 `plateAppearances >= 50` 且投球 >=5 场门槛，否则 Vesia 这类后援会被误判成二刀流。
3. 非名单内 6 目录（gavin-stone 等）未动，封面本就是旧版风格。

*更新：2026-10-18*

---

# 未来赛季（模板）

> 新赛季开赛复制本文件结构：
> 1. 跑 `scripts\fetch-season-roster.py` 生成当年出场名单
> 2. 用脚本重新生成本表的常规赛批名单（可复用本文件生成逻辑）
> 3. 季后赛批等外卡名单确定后从 boxscore 汇总（复用 `scripts\ps-participants.py` 思路）

```
## YYYY 赛季

### 常规赛批（N 人）
| 完成 | 球员 | 位置 | 出场 | 赛季数据 | 现状 |
| ... |

### 季后赛批（N 人）
| 完成 | 球员 | 出场 | 角色 |
| ... |
```

---
*生成时间：2026-10-15（出场名单快照 2026-10-15T20:55:14.067793）*