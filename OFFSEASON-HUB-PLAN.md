# 休赛期转会中心 · 设计方案

> 建立：2026-11-01。用户已确认三项决策：**范围 = 道奇 + 全联盟重磅**；**流言板块 = 做**；**自动化 = 不做 cron，用户喊一声才抓**（"我喊你抓"）。
> 状态：**v1 已上线（2026-11-01，commit 2bf8161）**。页面 + fetch-offseason.py + 冒烟测试 _smoke_offseason.js 全部就绪并验证。

---

## 一、目标

门户新增「休赛期」导航组 + 「转会中心」单页，覆盖 2026-27 冬市（自由球员签约、交易、40 人名单操作、流言），2027 春训时随赛季封存归档。

## 二、数据源与 API 要点

### 1. 道奇相关操作
```
GET https://statsapi.mlb.com/api/v1/transactions?teamId=119&startDate=<世界大赛次日>&endDate=<今天>
```
- 返回字段：`person.fullName`、`date` / `effectiveDate`、`typeCode`、`typeDesc`、`description`、`fromTeam` / `toTeam`（交易时两队都有）
- **⚠️ typeCode 撞缩写陷阱**：「宣布成为自由球员」的 typeCode 也是 `DFA`（Declared Free Agency），与「指定让渡」（Designated for Assignment）相同。**分类一律按 `typeDesc` 匹配**，禁止按 typeCode。
- 实测 2026-10-28 ~ 11-01 已有 10 条（含 Alberto Santos 小联盟签约、Kris Bubic / Miguel Rojas 宣布 FA）。

### 2. 全联盟重磅签约
- transactions 端点支持 `sportId=1`（全联盟）但量大。做法：**拉全联盟当日/当周 transactions，只保留大联盟合约签约与重磅交易**（按 description 含 "major league contract" 或 fromTeam/toTeam 均为大联盟队过滤），每条标注是否原道奇球员。
- 节奏：道奇流每次必抓；全联盟流可隔几天抓一次汇总（无 cron，用户喊时一并抓）。

### 3. 流言（API 无此数据）
- 由我（助手）应用户要求 web 搜索维护 `data\offseason-news.json`：球员/内容/来源 URL/日期/可信度标签（传闻/较可靠/已官宣）。
- 已官宣的流言由下次 transactions 抓取自动坐实，页面可手动或定期清理。

### 4. 40 人名单快照
```
GET https://statsapi.mlb.com/api/v1/teams/119/roster?rosterType=40Man&season=2027
```
（休赛期 season 参数用新年份；若返回空则去掉 season 重试。）每次抓取存快照，与赛季结束快照（ season-roster.json / dodgers-roster.md ）对比得出新增/移除。

## 三、页面结构（单页 5 板块）

导航：侧边栏新增第 4 组「休赛期」，含 1 项「⚾ 转会中心」（data-page="offseason"，renderOffseasonPage()）。

1. **总览卡片行**：新签约数 / 离队 FA 数 / 交易数 / 40 人名单占用（x/40）
2. **转会流水台**（核心）：道奇全部操作按时间倒序；类型筛选 chips + 球员搜索；徽章区分 大联盟签约/小联盟签约/续约/宣布 FA/交易/DFA/释出/40人保护
3. **全联盟重磅**：其他队大合约签约与重磅交易列表，标注"原道奇"标签；实时性强，与道奇流分开展示
4. **自由球员追踪**：道奇到期合同球员清单（状态：已续约 / 已签别队 / 未签）。「已签别队」需按 personId 反查该球员 transactions（`?playerId=<id>`），**此为 v2**
5. **流言雷达**： offseason-news.json 渲染，可信度分色，附来源链接
6. **40 人名单守望**（可并入板块 1 下方或独立）：当前 40 人网格，新增绿标 / 移除红标（对比快照）

## 四、技术件清单

| 件 | 路径 | 说明 |
|---|---|---|
| 抓取脚本 | `scripts\fetch-offseason.py` | 道奇 transactions + 40Man 快照 + 全联盟重磅（可选开关）→ `data\offseason.json`；urllib 须 `ProxyHandler({})` 绕开本机失效代理（127.0.0.1:7892）；SSL EOF 重试≥3 次；写 JSON 用 Python（PS WriteAllText 会带 BOM 炸 json） |
| 数据文件 | `data\offseason.json` | `{ generatedAt, dodgers: { moves[], roster40: { count, added[], removed[] } }, league: { signings[] }, fa: { pending[], reSigned[], departed[] }, news: [] }` |
| 流言文件 | `data\offseason-news.json` | 助手搜索后维护（也可并入 offseason.json 的 news 键，二选一，倾向合并） |
| 门户页面 | index.html 补丁 | 新导航组 + renderOffseasonPage()；老规矩 Python 补丁脚本 + 唯一锚点 + assert 计数，先备份 |
| 存档衔接 | archive-season.py / SEASON-PLAYBOOK.md | 2027 春训时 offseason.json 入 seasons\2027\snapshots\；playbook 补交接节 |

## 五、运营 SOP（无 cron 模式）

用户喊"抓一下转会"时：
1. `python scripts\fetch-offseason.py`（道奇 + 全联盟 + 40Man 一次跑完）
2. 门户若本次有页面改动：补丁 + 三板斧验证（check-portal-js.py、_smoke 系列、HTTP 探测）；只更新数据则免
3. robocopy D→E（/E 禁 /MIR）→ Compare-Object 查 E 独有残留（E 盘前缀 'E:\baseball\dodgers\' 含尾斜杠 20 字符）→ git add/commit/push main
4. web_fetch 验证 github.io 可达（本机直连被墙，别用本机 curl）；GitHub API 确认 HEAD
5. 用户要流言时：web 搜索 → 追加 news 条目 → 走第 3 步发布

## 六、分期

- **v1**：板块 1/2/3/6 + 流言（5）——纯 API + 搜索驱动，一次交付
- **v2**：板块 4 的「已签别队」personId 反查 + 全联盟流定期汇总
- 2027 开赛前：归档 + playbook 交接

## 七、已知风险与对策

| 风险 | 对策 |
|---|---|
| typeCode DFA 撞车 | 按 typeDesc 分类（见二.1） |
| 球员签约别队后 teamId=119 查不到 | v2 personId 反查；v1 阶段流言板块兜底 |
| 全联盟 sportId=1 数据量大 | 只保留大联盟合约签约/重磅交易，本地过滤 |
| 本机代理 7892 失效致 urllib 失败 | 脚本内 ProxyHandler({}) 直连 |
| 休赛期 season 参数行为未验证 | 脚本里 try 2027 →  fallback 不带 season |
| 流言 json 手工维护漏更新 | 用户驱动（喊我抓），不背自动时效债 |

---

### 实现偏差记录（2026-11-01 v1 施工后更新）
1. **分类基于 description 而非 typeDesc**：小联盟/大联盟合约区分只存在于 description 字段（Santos 案例：typeDesc 同为 "Signed as Free Agent"）。classify() 入参 = description or typeDesc。
2. **流言独立文件**：`data\offseason-news.json` 与 offseason.json 分离（原计划倾向合并）——无 cron 模式下，只更流言不必重跑抓取脚本。
3. **全联盟交易合并**：API 对同一交易按球员各记一条且 from/to 方向相反（Rayo: OAK→BOS / Eaton: BOS→OAK），按 date+无序两队 frozenset 合并；无 person 的现金对价记录丢弃。
4. **40 人首跑基线**：用 2026 出场名单（53 人）近似，removed 会偏噪；第二次抓取起以上次 40Man 快照为基线，自动精确。

*开工前重读本文 + SEASON-PLAYBOOK.md。*
