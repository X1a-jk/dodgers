# 2025 赛季球员报告 · 计划与规则

> 建立：2026-11-01。任务：为 **2025 年所有为道奇出赛过的 62 名球员**补齐「当时视角」的球探报告，格式完全对齐 2026 总结版，并借这批报告把门户**年份切换**链路整个跑通验证。
> 状态：文档定稿，待开工。

---

## 一、视角铁律（最高优先级）

**写作时间点 = 2025 年 11 月 1 日（2025 世界大赛刚结束、休赛期开启）。报告作者「不知道 2026 年会发生什么」。**

1. ✅ 可以写：2025 及之前赛季的事实、数据、奖项；2025 赛季结束后已官宣的状态（自由球员身份、球队/球员选项执行与否——以当时 transactions 为准）
2. ❌ 禁止写：任何 2026 赛季的表现、伤病恢复结果、签约/交易结果（"最终与道奇续约""2026 年回流"这类后世视角一律不准出现）
3. ⚠️ 退役/生涯节点：只有 2025-11-01 前官方宣布的才写（例如 Kershaw 若当时未官宣退役，报告里不得写"生涯最后一季"，只能写"合同与去留引关注"）
4. 未来展望一节：只基于 ≤2025 表现做开放式展望，不下具体结论

## 二、名单（62 人，完成一个打一个勾）

名单已存 `data\season-roster-2025.json`（MLB API `/stats?stats=season&teamId=119&season=2025` 打击+投球合并，含两刀流）。

### 投手（37 人）

- [x] yoshinobu-yamamoto（山本由伸，173.2 IP，王牌）✅ 2026-11-01
- [x] clayton-kershaw（112.2 IP）✅ 2026-11-01
- [ ] dustin-may（104 IP）
- [ ] tyler-glasnow（90.1 IP）
- [ ] ben-casparius（77.2 IP）
- [ ] jack-dreyer（76.1 IP）
- [ ] emmet-sheehan（73.1 IP）
- [ ] justin-wrobleski（66.2 IP）
- [ ] anthony-banda（65 IP）
- [ ] blake-snell（61.1 IP）
- [ ] tanner-scott（57 IP）
- [ ] alex-vesia（59.2 IP）
- [ ] landon-knack（42.1 IP）
- [ ] kirby-yates（41.1 IP）
- [ ] roki-sasaki（36.1 IP）
- [ ] tony-gonsolin（36 IP）
- [ ] matt-sauer（29.2 IP）
- [ ] luis-garcia（27.1 IP）
- [ ] blake-treinen（26.2 IP）
- [ ] lou-trivino-iii（26.1 IP）
- [ ] edgardo-henriquez（19 IP）
- [ ] will-klein（15.1 IP）
- [ ] michael-kopech（11 IP）
- [ ] alexis-diaz（9 IP）
- [ ] noah-davis（6 IP）
- [ ] bobby-miller（5 IP）
- [ ] evan-phillips（5.2 IP）
- [ ] yoendrys-gomez（4.1 IP）
- [ ] chris-stratton（4 IP）
- [ ] jose-urena（3 IP）
- [ ] jack-little（3 IP）
- [ ] ryan-loutos（3 IP）
- [ ] brock-stewart（3.2 IP）
- [ ] andrew-heaney（2 IP）
- [ ] jp-feyereisen（2 IP）
- [ ] julian-fernandez（2 IP）
- [ ] paul-gervase（2 IP）

**第一批（5人）✅ 2026-11-01 完成**：mookie-betts / freddie-freeman / clayton-kershaw / yoshinobu-yamamoto / shohei-ohtani。下一批从这里继续：andy-pages

### 打者（24 人 + 二刀流 1 人）

- [x] mookie-betts（663 PA）✅ 2026-11-01
- [x] freddie-freeman（627 PA）✅ 2026-11-01
- [ ] andy-pages（624 PA）
- [ ] teoscar-hernandez（546 PA）
- [ ] michael-conforto（486 PA）
- [ ] will-smith（436 PA）
- [ ] max-muncy（388 PA）
- [ ] tommy-edman（377 PA）
- [ ] miguel-rojas（317 PA，另有 5 IP 垃圾时间登板）
- [ ] enrique-hernandez（256 PA，另有 5.1 IP mopup）
- [ ] dalton-rushing（155 PA）
- [ ] hyeseong-kim（170 PA）
- [ ] alex-freeland（97 PA）
- [ ] alex-call（85 PA）
- [ ] ben-rortvedt（58 PA）
- [ ] austin-barnes（44 PA）
- [ ] james-outman（44 PA）
- [ ] chris-taylor（35 PA）
- [ ] esteury-ruiz（23 PA）
- [ ] buddy-kennedy（18 PA）
- [ ] eddie-rosario（4 PA）
- [ ] hunter-feduccia（3 PA）
- [ ] chuckie-robinson（2 PA）
- [ ] justin-dean（2 PA）
- [x] **shohei-ohtani（727 PA + 47 IP，二刀流：打击+投球双区同报）** ✅ 2026-11-01

> 注：37 投 + 24 打 + Ohtani = 62，与 `data\season-roster-2025.json` 完全一致（slug 以 JSON 为准，勿手改）。

## 三、格式规范（完全对齐 2026 总结版）

### 目录与文件（`seasons\2025\players\<slug>\`）

| 文件 | 说明 |
|---|---|
| `<slug>-scouting-report.html` | 主报告（下述章节结构） |
| `<slug>-scouting-report.md` | 摘要（塔克 md 格式） |
| `<slug>_report_cover.png` | 封面：**旧版深蓝模板唯一标准**（深蓝底/橙色 SCOUTING REPORT/居中 4×2 数据格/中文标语），复用 `regen-covers-old-style.py` 样式，数据格用 2025 数据 |
| `<slug>_season_comparison.png` | 雷达/条形对比图：**2024 vs 2025**（2026 版是 2025 vs 2026，年份平移） |
| `<slug>_overall_grades.png` | 20-80 评分雷达图 |
| `<slug>_game_trends.png` | 逐年趋势图 |
| `<slug>_pitch_velocities.png` | 仅投手：2025 武器库图（API 数据版式，同今日重画规格） |
| `headshot.jpg` | 沿用 2026 目录（同人）或 MLBAM 抓取 |
| 回退键 | `<body>` 后注入（10-29 统一按钮），iframe 内 history.back() |

### HTML 章节顺序（固定）

基本信息 → 球探总评 → 生涯亮点 → 赛季统计卡片（2025）→ 2024vs2025 对比 → 投球武器库（投手）→ 球探分析 → 优势 vs 劣势 → 20-80 评分 → 未来展望 → 背景故事

- 投球武器库：**按 2025 赛季真实数据重写**（今天上午的 API 管线直接复用，年份参数平移），禁止沿用 2026 口径
- 分析引擎：数据驱动（复用 `generate-final-reports.py` 的 build_analysis 思路），AVG 分层、OBP-AVG 差、SLG/ISO、K率、ERA/WHIP/K9/BB9、角色推断、小样本警告、两年对比趋势——全部只喂 2024/2025 数据
- 中文输出，杜绝模板话（红黑榜教训）

## 四、数据源与脚本管线

| 数据 | 端点 |
|---|---|
| 2025 赛季数据 | `/api/v1/stats?stats=season&group=hitting,pitching&teamId=119&season=2025`（已存 season-roster-2025.json） |
| 2024 对比数据 | 同上 season=2024；非道奇球员用 `/people/{id}/stats?season=2024` |
| 武器库 | `/people/{id}/stats?stats=pitchArsenal&season=2025` |
| 个人信息 | `/people/{id}`（身高体重、左右惯用手、debut） |
| 生涯亮点 | `/people/{id}/stats?stats=career` + 历年 season |
| 合同/选项状态 | `/transactions?teamId=119`（2025-10-26 起窗口，官宣事实才用） |

**管线（2026-11-01 修订：用户裁定纯手工逐人，禁用批量脚本）**
1. 每批 5 人，一个一个做：抓数 → 手写 HTML/md → 单人图表 → 验证 → 计划文档打勾
2. 图表仍用单人 matplotlib 小脚本（update-player-charts.py 的 2025 变体），报告内容一律手写
3. 数据铁律：只喂 2024/2025；生成后 grep "2026" 自检（只允许出现在历年趋势表）
4. 2026 版报告 HTML 作骨架模板（结构照抄，年份平移，分析重写）

~~原管线（已废止）：批量 gen-2025-reports.py...~~

## 五、门户集成与年份切换验证

1. **报告批次下拉**：`seasons\2025\players\index.html` 由 `build-dodgers-dashboard.py`（DASH_REPORT_ROOT/DASH_ROSTER_JSON 指向 2025）离线生成 → `scan_report_editions()` 自动收录为「2025 赛季总结版」，**零改动**
2. **年份选择器**：现 `years` 只从 weekly/daily/postseason 条目推导 → 2025 不会自动出现。需小改 `portal\update-portal.py`：`years = 内容条目赛季 ∪ {seasons\* 目录名}`
3. **总结页（recap）2025 分支**：无快照时现有代码优雅降级（"总结数据不存在"提示，不崩）。为让年份切换有实感，用 `fetch-postseason.py` 2025 模式生成 `seasons\2025\snapshots\postseason.json`（2025 排名+季后赛对阵树，API 可拉）+ 手写一份短 `seasons\2025\2025-赛季总结.md`
4. 验证三板斧 + 本地服务器实测切换 2026↔2025（截图对比）

## 六、发布 SOP

每人完成 → 文档打勾 `[x]`（标注日期）→ 62/62 后：批次 dashboard → update-portal.py → 三板斧 → sync E 盘 → push → web_fetch 线上验证 → 总结进 SEASON-PLAYBOOK.md

## 七、风险与对策

| 风险 | 对策 |
|---|---|
| 后世视角泄漏（写了 2026 才知道的事） | 生成 prompt/模板里年份硬约束 + 抽查时专门 grep "2026"（报告内只允许出现在「历年趋势」数据表） |
| 2025 -only 球员无 2026 目录可抄封面/头像 | 封面脚本参数化年份；头像走 MLBAM 图片接口 |
| 山本/Kershaw 等 2025 数据量大、叙事重 | 正常权重处理，分析引擎数据驱动保底 |
| Ohtani 二刀流 | 一份 HTML 内同时渲染打击+投球两区（对照 2026 版 Ohtani 报告结构） |
| 2025 赛季本文无周报/日报存档 | 年份切换后内容列表为空属预期，总结页靠 postseason.json + 总结 md 撑 |

---

*开工前重读本文。勾选用 git 提交历史 + 本文进度表双记录。*
