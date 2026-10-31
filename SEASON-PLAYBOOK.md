# 道奇数据系统 · 赛季交接手册（Season Playbook）

> 创建：2026-09-28 · 适用范围：每个新赛季开始前统一过一遍
> 配套文档：`portal\README.md`（门户功能）、`portal\design-roadmap.md`（改造日志）、`MEMORY.md`（血泪教训）

---

## 〇、30 秒速览

| 事项 | 要不要动 | 说明 |
|------|----------|------|
| 门户年份切换/历年阵容/存档结构 | ❌ 不用动 | 全自动，新归档年份自动出现 |
| 每日管线（日报/伤病/transactions/季后赛对阵/历年阵容） | ❌ 不用动 | 赛季年份全部动态化（2026-09-28 已修） |
| 周报生成（generate-weekly.py） | ❌ 不用动 | 本来就是动态年份 |
| 日报 cron / 新闻 cron | ❌ 不用动 | 全年运行 |
| **周报 cron（季后赛版）** | ⚠️ 要看 | 道奇淘汰后由它生成告别总结，然后**停用** |
| **球员报告生成器** | ⚠️ 要看 | 新年份球员变了，需重新生成 |
| **季后赛页 / 十月皮肤** | ❌ 自动 | 11 月自动关闭，2027 年 10 月自动再开 |
| **archive-season.py 2026** | ✅ 必须 | 季后赛打完跑一次，完成 2026 封存 |

---

## 一、2026 收尾清单（2026 年 10-11 月，按顺序）

### 1. 季后赛期间（10 月）
- 门户「🍂 季后赛对阵」页每日自动更新比分，「📜 历年阵容」页照常每日刷新。
- 周一 12:00 的 **Dodgers Postseason Weekly Report** cron 自动生成系列赛战报到
  `seasons\2026\postseason\weekly\`——检查两次确认格式正常。
- **球员报告赛季更新**：用 `PLAYER-REPORTS-PLAN.md`（D:\baseball 根目录）做总控表——
  53 人常规赛批 + 季后赛批人名清单，更新完一个打一个勾，两批全部完成后按下面流程封存。
- 若用户要重新生成球员报告（含季后赛数据）：
  1. **先留底**：把 `report\` 整个复制为 `seasons\2026\players-regular\`
  2. 再重新生成到 `report\`（实时版）
  3. 跑一次 `python D:\baseball\portal\update-portal.py`
  4. 报告页版本选择器应出现「2026 常规赛版」+「2026 当前」两个选项

### 2. 世界大赛结束后（11 月初）
- [x] **封存 2026**（✅ 2026-10-28 完成，道奇 NLCS 出局后提前执行）：
  - 注意：`archive-season.py` 的 `archive_reports` 在 `seasons\YYYY\players` 已存在（哪怕是空目录）时会跳过迁移，需先删掉空目录再跑（本次踩到）。
  - 结果：日报 97 天 + 阵容快照全部入 `regular\daily\`（8 份季后赛期快照一并归入），36 个数据快照入 `snapshots\`，`report\` 598 文件整体迁入 `players\`，门户自动出现「2026 赛季总结版」。
- [x] **做年度总结**（✅ 2026-10-28）：`seasons\2026\2026-赛季总结.md`——战绩/分周轨迹/领袖/季后赛全记录/人员流动/存档清单。数据全部从 postseason.json + ps-postseason-final.json + 15 期周报还原核对。
  - ⚠️ `portal\dashboard-data.json` 在 10-15（常规赛结束后）就已含最终 standings，recap 页无需额外刷数据；重跑 fetch-dashboard-data.py 会清空 last7/赛程（休赛期正常现象）。
- [x] **停用季后赛周报 cron**（✅ 已是 disabled）。⚠️ 但发现 **三个 cron 全部 disabled**（日报监控、新闻摘要也是）——日报按手册应休赛期继续运行，是否恢复待用户定夺。
- [ ] **日报 cron 保持运行**——⚠️ 当前 disabled，待用户确认后重新 enable。

### 3. 休赛期（12 月 - 3 月）
- 系统全自动运转，无需干预。门户上 2026 年的所有内容已按年归档，可随时翻阅。
- 球员报告「当前」选项在 archive 后消失（report\ 已迁走）——属预期，新赛季重建报告后恢复。
- 若想做历年总结页：recap 页目前读现役数据文件，改读 `seasons\YYYY\snapshots\` 即可（预留接口，见 README）。

---

## 二、2027 新赛季清单（3 月春训 - 4 月开赛）

### 自动生效的部分（确认一下即可）
- [ ] 每日管线跑一次确认无报错：`powershell -NoProfile -ExecutionPolicy Bypass -File D:\baseball\scripts\run-daily-update.ps1`
  （若 ProxyError 127.0.0.1:7892 = Clash 没开，先 `$env:NO_PROXY='*'` 再跑）
- [ ] 周报生成：`python D:\baseball\scripts\generate-weekly.py`（第一周试试水）
- [ ] 门户 `start-portal.bat` 打开确认：年份选择器出现「2027」相关新文件自动归档前显示在「全部年份」

### 需要人工动的部分
- [ ] **重新生成球员报告**（名单大换血）：
  1. `python D:\baseball\scripts\generate-missing-reports.py`（新赛季新人）
  2. `python D:\baseball\scripts\build-dodgers-dashboard.py`（重建 report\index.html 总览）
  3. 深度图里的 reportUrl 由抓深度图的脚本生成，路径是球员 slug，不变则无需改
- [ ] **重建周报 cron**：把季后赛周报任务改回常规赛模式（或复制 2026 年 6 月原版 payload——
  关键区别：写 `weekly\YYYY-MM-DD-weekXX.md`、用 generate-weekly.py、红黑榜格式）。
   cron 历史里有原版可参考。
- [ ] **抽查一期周报质量**：对照 MEMORY.md「红黑榜铁律」——先核对伤病名单、区分当周/赛季、
  小样本标注、备注必须有具体分析。这页教训很贵，别丢。

### 球员报告的年度节奏（2027 起）
| 时间点 | 操作 | 产物 |
|--------|------|------|
| 全明星赛附近（7 月中） | 复制 report\ → `seasons\2027\players-asg\`，跑 update-portal.py | 「2027 全明星版」 |
| 赛季末（10 月初） | 重新生成 report\（常规赛最终版） | 「2027 当前」 |
| 若进季后赛 | 可选：复制为 `seasons\2027\players-postseason\` 或季后赛后再生成 | 「2027 季后赛版」 |
| 季后赛打完 | `archive-season.py 2027` | report\ 自动成为「2027 赛季总结版」 |

批次目录约定：`players-asg` / `players-regular` / `players-postseason` / `players-mid`（识别名见 update-portal.py 的 cn 映射，可加）。

---

## 三、cron 任务总表

| 任务 | 时间(北京) | 2026 末状态 | 新赛季动作 |
|------|-----------|-------------|-----------|
| Dodgers Roster Daily Monitor | 每日 12:00 | 运行中 | 不动 |
| dodgers-news-digest | 每日 07:04 | 运行中 | 不动 |
| Dodgers Postseason Weekly Report | 周一 12:00 | 淘汰后停用 | 2027-10 重建为季后赛模式 |

---

## 四、系统结构速查（2026-09-28 起）

```
D:\baseball\
├── seasons\YYYY\          按年归档（regular\weekly|daily、postseason\weekly、
│                          snapshots\=data快照、players\=球员报告、players-<批次>\）
├── weekly\ roster\        现役目录：当前赛季的周报/日报先落这里
├── data\                  当前态 JSON（season 字段全部动态化）
├── report\                球员报告（当前实时版）
├── portal\                index.html 单文件门户 + update-portal.py + server.py
└── scripts\               管线脚本（run-daily-update.ps1 是每日总入口）
```

**门户通用机制**（全部数据驱动，新年份零改动）：
- 战报/日报/季后赛战报：年份选择器 = `FILE_INDEX.years`
- 历年阵容：当前季读 `data\season-roster.json`，历史季读 `seasons\YYYY\snapshots\season-roster.json`
- 球员报告版本：`FILE_INDEX.reportEditions`（扫 report\ + seasons\YYYY\players[-批次]\）
- 季后赛对阵/十月皮肤：`postseason.json` 驱动，10 月自动启用、11 月自动关闭

---

## 五、验证三板斧（每次改完门户必跑）

```powershell
python D:\baseball\scripts\check-portal-js.py          # JS 语法
node D:\baseball\scripts\_smoke_postseason.js          # 季后赛页+总结页冒烟（断言 SMOKE_OK）
node D:\baseball\scripts\_smoke_year.js                # 年份选择器冒烟
node D:\baseball\scripts\_smoke_sr.js                  # 历年阵容冒烟
node D:\baseball\scripts\_smoke_recap.js               # 总结页存档列表+深度图链接+报告回退键冒烟（2026-10-29 新增）
# HTTP 探测：Start-Process python portal\server.py 8080 → Invoke-WebRequest 关键 URL → Stop-Process
```

冒烟脚本的已知噪音：结尾 TypeError（setPage 桩）无害，看断言和 SMOKE_OK 就行。

## 六、已知限制（别当成 bug 修）

1. MLB 多人交易的 transactions 记录 player 字段可能为空 → 历年阵容里该球员显示「季初在队」。
2. fetch-playoff.py（旧模拟器）还在每日管线里写 playoff.json，门户已不再使用——遗留无害，想清理可删（先确认无引用）。
3. `scripts\` 目录里有大量一次性脚本（backfill-*/fetch-09xx/check-*），不影响系统，清理时注意别删 `run-daily-update.ps1` 引用的 8 个。
4. 门户 index.html 是 232KB 单文件，改动一律走「Python 补丁脚本 + 备份 + 三板斧验证」，别手动大改。

## 七、2026-10-29 休赛期补丁（2027 前必读）

1. **`report\` 目录已不存在**（10-28 封存迁往 `seasons\2026\players`）：
   - `data\depth-chart.json` / `data\injuries.json` 的 `reportUrl` 已全部指向 `seasons\2026\players\<slug>\`（总结版），快照同步更新；**以后生成这两份数据的脚本若再写 `report/` 前缀即为回归**。
   - 门户所有「在新标签打开球员报告」按钮改走 `reportEditions()[0].path`（运行时解析，跨年自动跟随 currentSeason）。
   - update-portal.py 的 reportEditions 扫描 `report\` + `seasons\YYYY\players*`——`report\` 不存在时不报错，但 2027 赛季中新报告仍应写到 `report\`（现役），封存时再迁。
2. **报告页回退键**：三个批次 137 份 `*-scouting-report.html` 已在 `<body>` 后注入固定定位返回按钮（iframe 内 history.back()，新标签页回退到 `../index.html`）。**以后任何报告重生成脚本必须保留/重新注入该按钮**（判断标志：`history.back()`）。
3. **markdown-body 已改为深色主题变量**（原来是浅色稿：h1 #111827 黑字+浅灰表格，在深色门户上标题全 invisible）。改阅读器样式时以现有 var(--text)/var(--border) 为准。
4. **let 全局变量不挂 window**：`FILE_INDEX` 是 let 声明，`window.FILE_INDEX` 恒 undefined——10-29 总结页因此恒显示"暂无存档"。门户 JS 里引用一律 `(typeof FILE_INDEX !== 'undefined') ? FILE_INDEX : {}` 写法。
5. **fetch-postseason.py 状态推导**：dodgers.status 现按 rounds 实际比分推导（止步 NLDS/NLCS、世界大赛亚军/冠军），新增 dodgers.champion 字段（ws 4 胜球队 id 或 null）。世界大赛冠军=酿酒人（4-1 光芒），2026 全部季后赛数据已落 `data\postseason.json` + 快照。
6. **PowerShell `[IO.File]::WriteAllText UTF8 会写 BOM**——JSON 被写 BOM 后 python json.load 直接炸。写 JSON 用 `utf-8`（无 BOM）或写完跑 _strip-bom 类检查（已并入 _smoke_recap.js 断言）。

---

*最后更新：2026-10-29（赛季全部结束，季后赛终章+休赛期门户补丁）*
