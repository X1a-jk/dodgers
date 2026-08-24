# 道奇数据门户 (Dodgers Analytics Hub)

单页门户入口，整合三个模块：球员报告、每周战报、每日阵容。

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

## 功能说明

- **首页概览**：三个模块入口卡片，并展示最新周报/日报快捷列表
- **球员报告**：iframe 嵌入 `report/index.html`
- **每周战报**：左侧选择周报期数，右侧实时渲染 Markdown
- **每日阵容**：左侧选择日期，右侧实时渲染 40 人名单快照
