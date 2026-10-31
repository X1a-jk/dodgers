import matplotlib.pyplot as plt
import numpy as np
import os

# 统一风格参数（参考 Yamamoto 封面）
BG_COLOR = '#1a1a2e'
TITLE_COLOR = 'white'
SUBTITLE_COLOR = '#4fc3f7'
REPORT_COLOR = '#ff9800'
STAT_VALUE_COLOR = '#4fc3f7'
STAT_LABEL_COLOR = '#90a4ae'
FOOTER_COLOR = '#90a4ae'
FOOTER_INFO_COLOR = '#666'

# ============================================================
# BLAKE SNELL COVER - Yamamoto 风格
# ============================================================
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

# 大标题
ax.text(0.5, 0.85, 'Blake Snell', fontsize=32, fontweight='bold', ha='center', 
        color=TITLE_COLOR, transform=ax.transAxes)

# 副标题
ax.text(0.5, 0.75, 'Los Angeles Dodgers #7 | LHP', fontsize=18, ha='center', 
        color=SUBTITLE_COLOR, transform=ax.transAxes)

# 报告类型
ax.text(0.5, 0.65, 'SCOUTING REPORT 2026', fontsize=22, fontweight='bold', ha='center', 
        color=REPORT_COLOR, transform=ax.transAxes)

# 8个关键数据卡片（2行4列）
stats_data = [
    ('ERA', '3.24'), ('W-L', '72-55'), ('K', '1,261'), ('IP', '1,069'),
    ('WHIP', '1.23'), ('K/9', '10.6'), ('CY YOUNG', '2×'), ('Age', '33')
]

y_pos = 0.45
for i, (label, value) in enumerate(stats_data):
    x_pos = 0.15 + (i % 4) * 0.23
    if i >= 4:
        y_pos = 0.25
    ax.text(x_pos, y_pos, value, fontsize=26, fontweight='bold', ha='center',
            color=STAT_VALUE_COLOR, transform=ax.transAxes)
    ax.text(x_pos, y_pos - 0.08, label, fontsize=12, ha='center',
            color=STAT_LABEL_COLOR, transform=ax.transAxes)

# 底部荣誉
ax.text(0.5, 0.08, '2018 AL Cy Young | 2023 NL Cy Young | 2025 Dodgers Debut', fontsize=14, ha='center',
        color=FOOTER_COLOR, transform=ax.transAxes, style='italic')
ax.text(0.5, 0.02, 'Generated: 2026-07-11 | Data: MLB.com, MLB Stats API', 
        fontsize=10, ha='center', color=FOOTER_INFO_COLOR, transform=ax.transAxes)

plt.savefig(r'D:\baseball\report\blake-snell\snell_report_cover.png', 
            dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()

# ============================================================
# WILL SMITH COVER - Yamamoto 风格
# ============================================================
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

ax.text(0.5, 0.85, 'Will Smith', fontsize=32, fontweight='bold', ha='center', 
        color=TITLE_COLOR, transform=ax.transAxes)
ax.text(0.5, 0.75, 'Los Angeles Dodgers #16 | Catcher', fontsize=18, ha='center', 
        color=SUBTITLE_COLOR, transform=ax.transAxes)
ax.text(0.5, 0.65, 'SCOUTING REPORT 2026', fontsize=22, fontweight='bold', ha='center', 
        color=REPORT_COLOR, transform=ax.transAxes)

stats_data = [
    ('AVG', '.263'), ('HR', '86+'), ('RBI', '300+'), ('OPS', '.800'),
    ('OBP', '.350'), ('SLG', '.450'), ('ALL-STAR', '2×'), ('Age', '31')
]

y_pos = 0.45
for i, (label, value) in enumerate(stats_data):
    x_pos = 0.15 + (i % 4) * 0.23
    if i >= 4:
        y_pos = 0.25
    ax.text(x_pos, y_pos, value, fontsize=26, fontweight='bold', ha='center',
            color=STAT_VALUE_COLOR, transform=ax.transAxes)
    ax.text(x_pos, y_pos - 0.08, label, fontsize=12, ha='center',
            color=STAT_LABEL_COLOR, transform=ax.transAxes)

ax.text(0.5, 0.08, '2020 World Series Champion | 2023-2024 All-Star', fontsize=14, ha='center',
        color=FOOTER_COLOR, transform=ax.transAxes, style='italic')
ax.text(0.5, 0.02, 'Generated: 2026-07-11 | Data: MLB.com, MLB Stats API', 
        fontsize=10, ha='center', color=FOOTER_INFO_COLOR, transform=ax.transAxes)

plt.savefig(r'D:\baseball\report\will-smith\smith_report_cover.png', 
            dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
plt.close()

print("Cover images regenerated in Yamamoto style!")
