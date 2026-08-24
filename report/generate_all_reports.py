import subprocess
import json
import os
import sys
import time
from datetime import datetime

# 活跃球员列表
active_players = [
    # 投手
    {"name": "Jack Dreyer", "position": "P", "number": "86", "type": "pitcher"},
    {"name": "Edgardo Henriquez", "position": "P", "number": "60", "type": "pitcher"},
    {"name": "Kyle Hurt", "position": "P", "number": "63", "type": "pitcher"},
    {"name": "Will Klein", "position": "P", "number": "61", "type": "pitcher"},
    {"name": "Eric Lauer", "position": "P", "number": "33", "type": "pitcher"},
    {"name": "Evan Phillips", "position": "P", "number": "59", "type": "pitcher"},
    {"name": "Tanner Scott", "position": "P", "number": "66", "type": "pitcher"},
    {"name": "Emmet Sheehan", "position": "P", "number": "80", "type": "pitcher"},
    {"name": "Brock Stewart", "position": "P", "number": "41", "type": "pitcher"},
    {"name": "Alex Vesia", "position": "P", "number": "51", "type": "pitcher"},
    {"name": "Justin Wrobleski", "position": "P", "number": "70", "type": "pitcher"},
    {"name": "Yoshinobu Yamamoto", "position": "P", "number": "18", "type": "pitcher"},
    # 双向
    {"name": "Shohei Ohtani", "position": "DH/P", "number": "17", "type": "two-way"},
    # 捕手
    {"name": "Eliezer Alfonzo", "position": "C", "number": "64", "type": "batter"},
    {"name": "Dalton Rushing", "position": "C", "number": "68", "type": "batter"},
    # 内野手
    {"name": "Mookie Betts", "position": "IF/OF", "number": "50", "type": "batter"},
    {"name": "Alex Freeland", "position": "IF", "number": "76", "type": "batter"},
    {"name": "Freddie Freeman", "position": "1B", "number": "5", "type": "batter"},
    {"name": "Max Muncy", "position": "3B", "number": "13", "type": "batter"},
    {"name": "Miguel Rojas", "position": "SS", "number": "72", "type": "batter"},
    # 外野手
    {"name": "Alex Call", "position": "OF", "number": "12", "type": "batter"},
    {"name": "Tommy Edman", "position": "OF/IF", "number": "25", "type": "batter"},
    {"name": "Teoscar Hernandez", "position": "OF", "number": "37", "type": "batter"},
    {"name": "Andy Pages", "position": "OF", "number": "44", "type": "batter"},
    {"name": "Kyle Tucker", "position": "OF", "number": "23", "type": "batter"}
]

def generate_report(player, stats_text):
    """生成球员报告"""
    player_slug = player['name'].lower().replace(' ', '-')
    output_dir = f"D:\\baseball\\report\\{player_slug}"
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成Markdown报告
    md_content = f"""# {player['name']} 球探报告

> **Los Angeles Dodgers #{player['number']} | {player['position']}**
> 
> 报告生成时间：2026-07-09

---

## 📋 基本信息

| 项目 | 内容 |
|------|------|
| **姓名** | {player['name']} |
| **背号** | #{player['number']} |
| **位置** | {player['position']} |
| **球队** | Los Angeles Dodgers |
| **类型** | {player['type']} |

---

## 📊 统计数据

```
{stats_text}
```

---

## 📝 备注

此报告为批量生成版本。详细分析版本将在后续补充。

数据来源：MLB Stats API
"""
    
    # 保存Markdown文件
    md_path = os.path.join(output_dir, f"{player_slug}-scouting-report.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return output_dir

def main():
    print("=" * 60)
    print("Dodgers Active Players Scouting Report Generator")
    print("=" * 60)
    print(f"\nTotal players: {len(active_players)}\n")
    
    success_count = 0
    failed_players = []
    
    for i, player in enumerate(active_players, 1):
        print(f"[{i:2d}/{len(active_players)}] {player['name']:<25} ... ", end="", flush=True)
        
        try:
            # 获取统计数据
            result = subprocess.run(
                ['python', r'C:\Users\Junkai XIA\.openclaw\workspace\skills\baseball\scripts\baseball.py', 
                 'stats', player['name']],
                capture_output=True, text=True, timeout=30
            )
            
            stats_text = result.stdout if result.returncode == 0 else "Stats not available"
            
            # 生成报告
            output_dir = generate_report(player, stats_text)
            
            print(f"OK")
            success_count += 1
            
            # 避免请求过快
            time.sleep(0.5)
            
        except Exception as e:
            print(f"FAIL: {str(e)[:50]}")
            failed_players.append(player['name'])
    
    print("\n" + "=" * 60)
    print(f"Completed: {success_count}/{len(active_players)}")
    if failed_players:
        print(f"Failed ({len(failed_players)}): {', '.join(failed_players)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
