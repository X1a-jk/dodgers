# 道奇数据门户 (Dodgers Analytics Hub)

单页门户入口，整合三个模块：球员报告、每周战报、每日阵容。

> 📕 **赛季交接**：新老赛季切换流程见 `D:\baseball\SEASON-PLAYBOOK.md`（每年开赛/收官各过一遍）

## 文件结构

```
D:\baseball\
├── index.html              # 门户入口（单页应用）
├── portal\
│   ├── marked.min.js       # Markdown 渲染引擎
│   ├── update-portal.py    # 扫描 weekly/roster 并更新文件索引
│   ├── start-portal.bat    # Windows 批处理启动脚本
│   ├── start-portal.ps1    # PowerShell 启动脚本
│   └── README.md           # 本文件
├── report\
│   └── index.html          # 球员报告模块
├── weekly\                  # 每周战报 Markdown
└── roster\                 # 每日阵容/日报 Markdown
```

## 快速启动（推荐）

双击运行或在 PowerShell / CMD 里执行：

```powershell
D:\baseball\portal\start-portal.bat
```

或 PowerShell：

```powershell
D:\baseball\portal\start-portal.ps1
```

脚本会：
1. 运行 `update-portal.py` 刷新文件列表
2. 启动本地服务器（端口 8080）
3. 自动打开浏览器访问 `http://localhost:8080`

## 手动启动

```powershell
cd D:\baseball
python portal\update-portal.py   # 刷新索引
python -m http.server 8080        # 启动服务器
# 浏览器打开 http://localhost:8080
```

## 为什么建议用服务器访问？

直接用 `file://` 打开 `index.html` 也能看到界面，但浏览器会限制本地文件读取，周报/日报内容可能无法加载。通过 `http://localhost:8080` 访问可以避免这个问题。

## 更新文件索引

当新增周报或日报后，运行：

```powershell
python D:\baseball\portal\update-portal.py
```

脚本会自动扫描 `weekly/` 和 `roster/` 目录，把最新文件列表写回 `index.html`。

- **季后赛对阵（ postseason ）**：双联盟完整 bracket，外卡轮→分区赛→联盟冠军赛→世界大赛，系列赛状态实时追踪
- **常规赛总结（recap）**：162 场最终封存——战绩卡、分区排名、季后赛种子、球队领袖、周战报存档
- **十月皮肤**：季后赛期间自动切换金色主题（10 月或赛程公布时启用）

## 按年分档存档（Seasons Archive）

```
seasons\YYYY\
├── regular\weekly\      # 常规赛周报
├── regular\daily\       # 每日阵容快照
├── postseason\weekly\   # 季后赛系列赛战报
├── snapshots\           # 年终封存的数据 JSON 快照
└── players\             # 年终封存的球员报告
```

- **进行中**：新文件先落现役目录（weekly\、roster\），门户索引同时扫描现役 + 所有 seasons\ 年份
- **赛季末**：运行 `python D:\baseball\scripts\archive-season.py YYYY` 一次性迁入（支持 `--dry-run` 预演）
- 门户阅读器按 FILE_INDEX 条目的 folder 字段取文件，跨年浏览无缝

## 季后赛内容存放

- 季后赛战报：`D:\baseball\seasons\2026\postseason\weekly\YYYY-MM-DD-ps-<轮次>.md`
- 季后赛数据：`D:\baseball\data\postseason.json`（由 `scripts/fetch-postseason.py` 每日刷新）

## 年份切换（预留接口）

战报/日报阅读器（每周战报、每日阵容、季后赛战报）顶部有**年份选择器**：

- 选项由 `FILE_INDEX.years` 自动生成——`update-portal.py` 扫描现役目录 + 所有 `seasons\YYYY\`，发现新年份归档后**自动出现**，无需改门户代码
- 每个索引条目带 `season` 字段，选择器按它过滤，可与关键词搜索叠加
- 选择器兜底逻辑：即使旧版 file-index.json 没有 `years` 字段，也会从条目的 `season` 字段推导

**新赛季上线流程（明年 3 月）**：
1. 什么都不用改，周报/日报照常生成到现役目录（weekly\、roster\），条目自动带新年份
2. 赛季末跑一次 `python D:\baseball\scripts\archive-season.py 2027`
3. 门户阅读器自动多出「2027 赛季」选项

**已预留、待启用**：
- 历年常规赛总结：renderRecapPage 目前读现役数据文件；将来可按同样思路加年份参数，改读 `seasons/<year>\snapshots\` 里的封存快照

## 历年阵容（Season Roster）

阵容组「📜 历年阵容」页：某赛季**所有为道奇出场过的球员**，含中途签来、DFA、交易离队者。

- 数据：`scripts\fetch-season-roster.py`（每日管线）→ `data\season-roster.json`
  - 出场名单：MLB `/stats` playerPool=ALL（打击+投球合并，二刀流合一）
  - 现状：depth-chart.json（活跃/伤病/小联盟）；不在其中 = 已离队
  - 轨迹：transactions.json 全量解析（签约/交易获得/上调/DFA/Outright/释出，带日期）
- 年份切换：下拉框选年份；当前赛季读实时数据，历史年份读 `seasons\YYYY\snapshots\season-roster.json`（archive-season.py 自动快照）
- 2026 实况：53 人出场，中途加入 21 人，离队 11 人
- 已知限制：部分多人交易在 MLB transactions 里 player 字段为空，无法归属到具体球员（该球员显示「季初在队」）

## 球员报告版本切换

球员报告页顶部新增**版本选择器**：

- 版本清单由 `update-portal.py` 扫描生成（`FILE_INDEX.reportEditions`），约定：
  - `report\index.html` → 当前赛季（实时更新）
  - `seasons\YYYY\players\index.html` → 该年赛季总结版（archive-season.py 自动迁入）
  - `seasons\YYYY\players-<edition>\index.html` → 批次版（手动放）：`asg` 全明星版 / `regular` 常规赛版 / `postseason` 季后赛版 / `mid` 季中版
- **未来每年更新两次（或三次）的操作**：全明星赛附近把 `report\` 复制为 `seasons\YYYY\players-asg\`；赛季末重新生成后由 archive-season.py 归档为 `players\`；若打季后赛再做 `players-postseason\`——复制完跑一次 `update-portal.py`，下拉框自动出现
- 2026 特别说明：当前 report\ 是常规赛版；若之后几周重新生成（含季后赛数据），建议先把现状复制为 `seasons\2026\players-regular\` 留存，新版本留在 report\ 实时更新，赛季末 archive-season.py 自动把它变成赛季总结版

## 功能说明

- **首页概览**：三个模块入口卡片，并展示最新周报/日报快捷列表
- **球员报告**：iframe 嵌入 `report/index.html`
- **每周战报**：左侧选择周报期数，右侧实时渲染 Markdown
- **每日阵容**：左侧选择日期，右侧实时渲染 40 人名单快照
