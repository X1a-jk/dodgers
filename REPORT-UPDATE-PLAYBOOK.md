# 球员报告更新 Playbook（2026-10-17 旧版风格更新）

## 目标
在**旧版风格报告**（已从 report.bak-20261017 还原到 D:\baseball\report\）基础上，把数据更新到 2026 赛季最终（常规赛+季后赛），酌情修正评价文字。**保持原报告的结构、排版、文风、图表风格不变**。禁止改动 D:\baseball\report.bak-20261017\。

## 数据源（都是本地 JSON，不要直接打 MLB API）
- `D:\baseball\data\season-roster.json` → players[]：{id, name, pos, g, bat{avg,hr,rbi,ops,sb,hits}, pit{...}, status}
- `D:\baseball\data\final-stats.json` → hitting_2026 / pitching_2026 / hitting_2025 / pitching_2025，按 **player id 字符串** 索引，是全量计数数据（gamesPlayed/atBats/runs/hits/doubles/triples/homeRuns/rbi/stolenBases/baseOnBalls/strikeOuts/avg/obp/slg/ops；投球含 era/whip/wins/losses/saves/strikeOuts/inningsPitched/gamesStarted 等）
- `D:\baseball\data\ps-postseason-final.json` → participants[]：25 名季后赛出场者的逐人聚合（games, bat{plateAppearances,avg,obp,slg,ops,homeRuns,rbi,baseOnBalls,strikeOuts,stolenBases}, pit{ip,era,whip,wins,losses,saves,strikeOuts,baseOnBalls,gamesStarted}, gs）

## 操作对象
- HTML 主文档：`D:\baseball\report\<slug>\<slug>-scouting-report.html`（主文件，结构最完整）
- MD 摘要：同目录 `<slug>-scouting-report.md`（结构较简，同步改数字）

## 步骤
1. `python -X utf8 D:\baseball\scripts\_inspect_player.py <slug>` 查看现有卡片/对比行/带数字的段落/页脚。
2. 生成 spec JSON 到 `D:\baseball\scripts\_specs\<slug>.json`：
   ```json
   {"cards": {"出赛": "154", "打击率": ".233", ...},
    "row2026": ["154", ".233", ".330", ".385", ".715", "17", "70", "78", "105"]}
   ```
   - cards 的 key 必须和 HTML 里的 stat-label 完全一致（中文标签：出赛/打击率/上垒率/长打率/OPS/全垒打/打点/盗垒；投手可能是 出赛/防御率/WHIP/胜-败/三振/救援 等，以 inspect 输出为准）。
   - row2026 是对比表里 2026 行的单元格值（按顺序；投手行可能是 G/GS/W-L/ERA/IP/SO/BB 等列数不同，以 inspect 为准；不需要改的格子给 null）。
3. 跑 `python -X utf8 D:\baseball\scripts\apply-data-update.py <slug> D:\baseball\scripts\_specs\<slug>.json` 完成机械数字替换（页脚日期会自动改成 2026-10-17）。
4. **文字酌情更新**（用 python 读原文做精确子串替换，或 edit 工具）：
   - 所有引用旧数据（如"91场"、".296"、"仅7轰"、"保送率12.6%"）的句子都要改成最终数据。
   - 结论随数据变化修正：例如季中时写"下半季有望反弹"，赛季结束要写成实际结果；季中写"状态出色"但全年下滑的要如实下调。
   - 保留原文的文风、emoji、排版结构；只改该改的，不重写全文。
   - 若该球员在 ps-postseason-final.json 的 25 人名单里，在 `<h2>🔮 未来展望</h2>` 所在 section 之前插入一个同款 `<div class="section">`，标题 `<h2>🏆 2026 季后赛表现</h2>`：
     - 首行：`<p style="margin-bottom: 15px;">道奇 2026 季后赛战绩：NLDS 3-1 晋级、NLCS 0-4 止步。</p>`
     - 打者表格列：G|PA|AVG|OBP|SLG|OPS|HR|RBI|BB|SO；投手表格列：G|GS|W-L|ERA|WHIP|IP|SO|BB（二刀流两者都给）。
     - 表格用 class="comparison-table"，OPS 格用 class="highlight"。
     - 表下 2-3 条 `<ul>` 点评，必须具体（谁打得好/差、几轰几打点、ERA 如何、样本小需注明），不许写"表现良好"这类空话。
5. MD 同步：把 2026 数据表数字换成最终值；若在季后赛 25 人名单，加一段 `## 🏆 2026 季后赛` 表格+一句点评；页脚/头部日期改 2026-10-17。
6. 重建图表：`python -X utf8 D:\baseball\scripts\update-player-charts.py <slug>`（会自动按最终数据重画封面/赛季对比/评分雷达，文件名对齐 HTML 引用；stderr 的字体警告可忽略，退出码 1 属正常）。
7. 自检：
   - HTML 里 grep 旧日期 `2026-07` 和旧出赛数（mid-season 数字）应为 0 残留；
   - `🏆 2026 季后赛表现` 章节存在（若在 25 人名单）；
   - HTML/MD 无乱码 `?`（中文字符被替换成的问号），无未替换的旧数据。

## 铁律
- ❌ 不动 `D:\baseball\report.bak-20261017\`
- ❌ 不改变报告结构/章节顺序/CSS/图表文件名
- ❌ 不写模板话；点评必须带具体数字
- ✅ 投手 WHIP/ERA 等率值以 final-stats.json 为准；季后赛率值以 ps-postseason-final.json 为准
- ✅ 综合评分（20-80）原则上保留原版；只有当最终数据与评级明显矛盾时才微调一格，并在点评里体现
