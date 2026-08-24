from pathlib import Path

TARGETS = ['ben-casparius','blake-treinen','bobby-miller','brock-stewart','brusdar-graterol','gavin-stone','jack-dreyer','jake-cousins','kyle-hurt','landon-knack','nick-frasso','paul-gervase','river-ryan','will-klein']

def check_file(slug):
    p = Path(slug) / f'{slug}-scouting-report.html'
    if not p.exists():
        return f'{slug}: MISSING FILE'
    text = p.read_text(encoding='utf-8')
    issues = []
    checks = [
        ('header', '<div class="header">'),
        ('player-card', '<div class="player-card">'),
        ('career highlights', '<h2>🏆 职业生涯亮点</h2>'),
        ('2026 stats', '<h2>📊 2026赛季投球数据</h2>'),
        ('season comparison', '<h2>📊 2025 vs 2026 赛季对比</h2>'),
        ('pitch arsenal', '<h2>⚾ 投球武器库</h2>'),
        ('analysis', '<h2>🔍 球探分析</h2>'),
        ('pros-cons', '<h2>✅ 优势 vs ❌ 劣势</h2>'),
        ('grades', '<h2>📊 综合评分</h2>'),
        ('future', '<h2>🔮 未来展望</h2>'),
        ('background', '<h2>📖 背景故事</h2>'),
        ('footer', '<div class="footer">'),
    ]
    for name, marker in checks:
        if marker not in text:
            issues.append(f'missing {name}')
    # check for raw markdown left in output
    if '### 优势' in text or '### 劣势' in text:
        issues.append('raw markdown headers in output')
    if text.count('<h2>') < 10:
        issues.append('too few h2 sections')
    return f'{slug}: {"OK" if not issues else ", ".join(issues)}'

for t in TARGETS:
    print(check_file(t))
