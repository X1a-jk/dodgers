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
- 若用户要重新生成球员报告（含季后赛数据）：
  1. **先留底**：把 `report\` 整个复制为 `seasons\2026\players-regular\`
  2. 再重新生成到 `report\`（实时版）
  3. 跑一次 `python D:\baseball\portal\update-portal.py`
  4. 报告页版本选择器应出现「2026 常规赛版」+「2026 当前」两个选项

### 2. 世界大赛结束后（11 月初）
- [ ] **封存 2026**：`python D:\baseball\scripts\archive-season.py 2026 --dry-run` 先看计划，确认无误后去掉 `--dry-run` 正式跑。
  - 效果：当年战报/日报迁入 `seasons\2026\`，data 快照进 `seasons\2026\snapshots\`，球员报告进 `seasons\2026\players\`（成为「2026 赛季总结版」），门户索引自动刷新。
- [ ] **做年度总结**：素材位置——
  - 全程比分+球队领袖：`seasons\2026\snapshots\postseason.json`
  - 最终排名/战绩：`seasons\2026\snapshots\dashboard-data.json`
  - 战报：15 期常规赛周报 + 每日阵容快照 + 季后赛系列赛战报（都在 seasons\2026\ 下）
  - 球员报告：`seasons\2026\players\`（+ 可能的 players-regular 等批次）
  - 人员名单轨迹：`seasons\2026\snapshots\season-roster.json`（53 人出场、中途加入 21、离队 11）
- [ ] **停用季后赛周报 cron**：等它最后跑一次（会生成赛季告别总结并询问），然后在 OpenClaw 里 disable 或删除该任务。
  到 2027 年 10 月再重建（或直接复制本任务改描述）。
- [ ] **日报 cron 保持运行**（休赛期也有 roster/伤病变动，日报照样有价值）。

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
# HTTP 探测：Start-Process python portal\server.py 8080 → Invoke-WebRequest 关键 URL → Stop-Process
```

冒烟脚本的已知噪音：结尾 TypeError（setPage 桩）无害，看断言和 SMOKE_OK 就行。

## 六、已知限制（别当成 bug 修）

1. MLB 多人交易的 transactions 记录 player 字段可能为空 → 历年阵容里该球员显示「季初在队」。
2. fetch-playoff.py（旧模拟器）还在每日管线里写 playoff.json，门户已不再使用——遗留无害，想清理可删（先确认无引用）。
3. `scripts\` 目录里有大量一次性脚本（backfill-*/fetch-09xx/check-*），不影响系统，清理时注意别删 `run-daily-update.ps1` 引用的 8 个。
4. 门户 index.html 是 232KB 单文件，改动一律走「Python 补丁脚本 + 备份 + 三板斧验证」，别手动大改。

---

*最后更新：2026-09-28（2026 赛季存档完成后请在本手册补记实际情况）*
