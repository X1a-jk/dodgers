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
- [x] dustin-may（104 IP）✅ 2026-11-03
- [x] tyler-glasnow（90.1 IP）✅ 2026-11-03
- [x] ben-casparius（77.2 IP）✅ 2026-11-03
- [x] jack-dreyer（76.1 IP）✅ 2026-11-03
- [x] emmet-sheehan（73.1 IP）✅ 2026-11-03
- [x] justin-wrobleski（66.2 IP）✅ 2026-11-06
- [x] anthony-banda（65 IP）✅ 2026-11-06
- [x] blake-snell（61.1 IP）✅ 2026-11-06
- [x] tanner-scott（57 IP）✅ 2026-11-06
- [x] alex-vesia（59.2 IP）✅ 2026-11-06
- [x] landon-knack（42.1 IP）✅ 2026-11-06
- [x] kirby-yates（41.1 IP）✅ 2026-11-06
- [x] roki-sasaki（36.1 IP）✅ 2026-11-06
- [x] tony-gonsolin（36 IP）✅ 2026-11-06
- [x] matt-sauer（29.2 IP）✅ 2026-11-06
- [x] luis-garcia（27.1 IP，道奇段 28 场 5.27 ERA，7/4 释出后天使 2.00/国民 0.90）✅ 2026-11-07
- [x] blake-treinen（26.2 IP）✅ 2026-11-07
- [x] lou-trivino-iii（26.1 IP）✅ 2026-11-07
- [x] edgardo-henriquez（19 IP）✅ 2026-11-07
- [x] will-klein（15.1 IP）✅ 2026-11-07
- [x] michael-kopech（11 IP，肩伤+膝伤夹击仅 14 场，11/2 选择自由球员）✅ 2026-11-07
- [x] alexis-diaz（9 IP，5/29 红人交易加盟，7-8 月与哥哥 Edwin 同队，9/4 DFA 勇士认领）✅ 2026-11-07
- [x] noah-davis（6 IP，3/27 现金自红袜购入，7/14 交易至双城）✅ 2026-11-07
- [x] bobby-miller（5 IP，整季 3A、9 月底扩编召回 2 场）✅ 2026-11-07
- [x] evan-phillips（5.2 IP，右肩旋转肌袖伤季末回归 7 场零失分）✅ 2026-11-07
- [x] yoendrys-gomez（4.1 IP）✅ 2026-11-07
- [x] chris-stratton（4 IP）✅ 2026-11-07
- [x] jose-urena（3 IP）✅ 2026-11-07
- [x] jack-little（3 IP）✅ 2026-11-07
- [x] ryan-loutos（3 IP）✅ 2026-11-07
- [x] brock-stewart（3.2 IP）✅ 2026-11-13
- [x] andrew-heaney（2 IP）✅ 2026-11-13
- [x] jp-feyereisen（2 IP）✅ 2026-11-13
- [x] julian-fernandez（2 IP）✅ 2026-11-13
- [x] paul-gervase（2 IP）✅ 2026-11-13

**第一批（5人）✅ 2026-11-01 完成**：mookie-betts / freddie-freeman / clayton-kershaw / yoshinobu-yamamoto / shohei-ohtani。
**第二批（7人）✅ 2026-11-01 完成**：andy-pages / teoscar-hernandez / michael-conforto / max-muncy / will-smith / tommy-edman / miguel-rojas / enrique-hernandez / dalton-rushing / hyeseong-kim（打者 10 人，同日完成）。
**第三批（5人）✅ 2026-11-01 完成**：alex-freeland / alex-call / ben-rortvedt / austin-barnes / james-outman。
**第四批（5人）✅ 2026-11-03 完成**：dustin-may / tyler-glasnow / ben-casparius / jack-dreyer / emmet-sheehan（投手批次；脚本新增 comparison_p.labels 自定义年份支持）。
**第五批（5人）✅ 2026-11-06 完成**：anthony-banda / blake-snell / tanner-scott / alex-vesia / landon-knack（投手批次；计划原注明下批从 banda 起，wrobleski 被跳过待下批；tanner-scott/landon-knack 季末伤病缺席季后赛的叙事来自 11-02 transactions 激活记录 + 季后赛 boxscore 缓存零出场互证）。**第六批（5人）✅ 2026-11-06 完成**：justin-wrobleski / kirby-yates / roki-sasaki / tony-gonsolin / matt-sauer（wrobleski 为上一批跳过的补位；Yates 背号以 2025 roster 为准 = #38；Gonsolin 用 2023vs2025 对比因 2024 整季报销；Sasaki 无 2024 MLB 数据，用「联盟均值(估)vs2025」版式沿用 dreyer 先例；Sauer 无背号记录写「—」；⚠️ career 聚合含 2026 赛季，本批报告一律用 2024+2025 自算或不用）。下一批从这里继续：luis-garcia

**第七批（5人）✅ 2026-11-07 完成**：luis-garcia / blake-treinen / lou-trivino-iii / edgardo-henriquez / will-klein（投手批次；本批 5 人 2025 年都经历过交易/释出/伤病，叙事核心是「流浪与重生」：garcia 道奇段 5.27 被释出后天使 2.00→国民 0.90；treinen 前臂伤缺席三个月后复出、K/9 12.15 与 BB/9 6.41 的反向冲刺、NLCS G1 救援成功；trivino 伤停两年后回归、一季三队曲线 5.84→3.76→2.00；henriquez 春训左脚骨折后复出 2.37、双百哩速球、季后赛满垒失控；klein 6/2 小交易加盟、WS G3 四局救火拿胜投。⚠️ 教训：season 端点返回全季数据（跨队合并），必须按 team id=119 过滤 split；季后赛聚合要用 outs/ER 而非 IP 字符串；trivino 对比图用「2025全季 vs 2025道奇」版式）。下一批从这里继续：michael-kopech

**第八批（5人）✅ 2026-11-07 完成**：michael-kopech / alexis-diaz / noah-davis / bobby-miller / evan-phillips（投手批次；本批全是小样本/伤病/流浪叙事：kopech 肩+膝两处伤病全年仅 11 局但 6 中继、11/2 跳出合同；diaz 从 37 救援全明星到一年三队、道奇段 WHIP 1.00 但 2 轰改命；davis 6 局 19.50 的六球种博物馆（含罕见螺旋球）；miller 整季 3A 后 5 局 12.60、双九七速球天赋未折旧；phillips 肩伤大半年后 7 场零失分回归。⚠️ 教训：transactions 端点宽窗口会截断/分页，必须 10 天粒度小窗扫；"2026 赛季"这种「年份+空格+赛季」形态 regex 不覆盖，展望措辞直接用「下赛季」规避）。下一批从这里继续：yoendrys-gomez

**第九批（5人）✅ 2026-11-07 完成**：yoendrys-gomez / chris-stratton / jose-urena / jack-little / ryan-loutos（投手批次；本批主题「waiver 浮萍与新生」：gomez 七球种 93.8 mph、被道奇 waiver 后白袜捡走；stratton 第 11 季第 7 队的老兵金融保险；urena 34 岁漂流者 6/11 被释出后流浪三队；little 两次大联盟一天游、6/6 被海盗认领；loutos 6'7" 火球巨塔 6/10 交易至国民、华盛顿 10 场 12.00 ERA。⚠️ 口径确认：展望节可直接用「2026 年」前瞻措辞（第七、八批已核实同先例），铁律禁的是后世事实泄漏。计划勾选与摘要 11-13 补记）。下一批从这里继续：brock-stewart

**第十批（5人）✅ 2026-11-13 完成**：brock-stewart / andrew-heaney / jp-feyereisen / julian-fernandez / paul-gervase（投手收官批，全员 ≤4 场的极小样本批；主题「归来与初来」：stewart 双城 39 场 2.38 后 7/31 被 Outman 单换回家、右肩发炎错过季后赛；heaney 海盗 26 场先发后 9/1 小联盟约回归、9/29 两局垃圾时间谢幕；feyereisen 从 2022 无失分赛季坠落到 5/25 DFA、11/2 被重新激活；fernandez TJ 三年沉默后道奇给唯一合约、国民段拿生涯首胜、gervase 6'10" 现役最高、7/31 与 Rortvedt/Serwinowski 打包换 Feduccia。⚠️ 口径：展望节「2026 年」前瞻措辞沿用第七、八、九批先例；对比图版式三种——stewart 用 2024双城vs2025双城、fernandez 用 2025道奇vs2025国民（trivino 式）、gervase 无 2024 数据用联盟均值(估)式（sasaki/dreyer 先例）。⚠️ 教训：⚠️ 本批所有「手术」叙事只写"手肘韧带重建"不写次数年份（避免无出处细节）；投手 season split 字段里的 obp/slg 是对手上垒/长打率，可作「被打击率/被长打率」引用）。投手 37/37 全部完成，剩打者 7 人。下一批从这里继续：chris-taylor

**第十一批（4人）✅ 2026-11-13 完成**：chris-taylor / esteury-ruiz / buddy-kennedy / eddie-rosario（打者批次；主题「老将谢幕与流浪补丁」：taylor 十年道奇 1007 场 108 轰后 5/18 被释、同城转天使；ruiz 2023 美联盗垒王 67 盗、在道奇被压成专职代跑（19 G 仅 23 PA、4/4 盗）；kennedy 一年三队（PHI/TOR/LAD）、8/15 认领 8/25 即 DFA；rosario 2019 年 32 轰 + 2021 NLCS MVP，道奇段仅 48 小时 2 场、回亚特兰大告别。⚠️ 教训：生涯累计数（1007 场/108 轰/169 轰/保送率 4.8%）必须从 yearByYear 逐年加总计算、写前重算一遍，凭印象写必错；打者对比图用 comparison 键（AVG/OBP/SLG/OPS 值域 0-1），跨队年份用合并行并在表头标注。）下一批从这里继续：hunter-feduccia

*更新：2026-11-13（第十、十一批）*

### 打者（24 人 + 二刀流 1 人）

- [x] mookie-betts（663 PA）✅ 2026-11-01
- [x] freddie-freeman（627 PA）✅ 2026-11-01
- [x] andy-pages（624 PA）✅ 2026-11-01
- [x] teoscar-hernandez（546 PA）✅ 2026-11-01
- [x] michael-conforto（486 PA）✅ 2026-11-01
- [x] will-smith（436 PA）✅ 2026-11-01
- [x] max-muncy（388 PA）✅ 2026-11-01
- [x] tommy-edman（377 PA）✅ 2026-11-01
- [x] miguel-rojas（317 PA，另有 5 IP 垃圾时间登板）✅ 2026-11-01
- [x] enrique-hernandez（256 PA，另有 5.1 IP mopup）✅ 2026-11-01
- [x] dalton-rushing（155 PA）✅ 2026-11-01
- [x] hyeseong-kim（170 PA）✅ 2026-11-01
- [x] alex-freeland（97 PA）✅ 2026-11-01
- [x] alex-call（85 PA，8/1 自国民交易激活）✅ 2026-11-01
- [x] ben-rortvedt（58 PA，9/4 自 3A 选入，7/31 自光芒交易获得）✅ 2026-11-01
- [x] austin-barnes（44 PA，5/14 DFA → 5/20 释出，十年老兵谢幕）✅ 2026-11-01
- [x] james-outman（44 PA，7/31 被交易至双城换 Brock Stewart）✅ 2026-11-01
- [x] chris-taylor（35 PA）✅ 2026-11-13
- [x] esteury-ruiz（23 PA）✅ 2026-11-13
- [x] buddy-kennedy（18 PA）✅ 2026-11-13
- [x] eddie-rosario（4 PA）✅ 2026-11-13
- [x] hunter-feduccia（3 PA）✅ 2026-11-14
- [x] chuckie-robinson（2 PA）✅ 2026-11-14
- [x] justin-dean（2 PA）✅ 2026-11-14

### 第十二批（收官批）
- 批次主题：「农场的最后一瞥」
- 名单：hunter-feduccia / chuckie-robinson / justin-dean（捕手×2 + 外野，全部 ≤3 PA 极小样本，叙事重于数据）
- 数据锚点：feduccia 是 7/31 Gervase 三人包裹交易被送走的一端（交易链闭环！）OKC 生涯年 .290/.399/.467；robinson 全年 waiver 线五体系流浪、道奇段唯一一场 2 PA 跑回 1 分、11/6 首次主动选 FA；dean 八年农场 255 盗、2024 年 3A 单季 61 盗、2025 3A 生涯年 .289/.378/.431 换得 8/8 MLB 首演（18 场 2 PA 守备专员）、11/6 被巨人认领

**第十二批（3人）✅ 2026-11-14 完成**：62 人全部完成 🎉。⚠️ 教训：① 三人 playerId 全错——id 必须先用 /people/search?names= 校验，凭记忆/旧表写必 404；② people/{id}/transactions 端点对无交易球员返回 404，多球员连抓要用 /api/v1/transactions?playerId= 模式；③ robinson/dean 无 MLB 官方真头像（img.mlbstatic 返回通用占位图 11714B），已存占位图（HTML 不引用头像，非视觉影响）；④ 赛后累计数（Dean 255 盗、Robinson 52 场 MLB）逐年加总。

**发布 SOP（62/62 后触发）**：① build-dodgers-dashboard.py 生成 2025 批次 index.html（DASH_REPORT_ROOT 指向 seasons\2025\players）；② update-portal.py 刷新 FILE_INDEX/reportEditions；③ 三板斧验证（check-portal-js.py + 冒烟桩 + HTTP 探测）；④ E 盘 robocopy → git add/commit/push；⑤ web_fetch 线上验证。
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
