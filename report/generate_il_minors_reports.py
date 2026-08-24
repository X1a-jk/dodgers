import subprocess
import os
import time

# 剩余球员列表（IL + Minors）
remaining_players = [
    # IL球员
    {"name": "Will Smith", "position": "C", "number": "16", "status": "IL-10"},
    {"name": "Enrique Hernandez", "position": "IF", "number": "8", "status": "IL-10"},
    {"name": "Blake Treinen", "position": "P", "number": "49", "status": "IL-15"},
    {"name": "Ben Casparius", "position": "P", "number": "78", "status": "IL-60"},
    {"name": "Tyler Glasnow", "position": "P", "number": "31", "status": "IL-60"},
    {"name": "Brusdar Graterol", "position": "P", "number": "48", "status": "IL-60"},
    {"name": "Edwin Diaz", "position": "P", "number": "3", "status": "IL-60"},
    {"name": "Landon Knack", "position": "P", "number": "96", "status": "IL-60"},
    {"name": "Bobby Miller", "position": "P", "number": "28", "status": "IL-60"},
    {"name": "Blake Snell", "position": "P", "number": "7", "status": "IL-60"},
    {"name": "Gavin Stone", "position": "P", "number": "35", "status": "IL-60"},
    {"name": "Jake Cousins", "position": "P", "number": "—", "status": "IL-60"},
    # 小联盟球员
    {"name": "Charlie Barnes", "position": "P", "number": "57", "status": "Minors"},
    {"name": "Nick Frasso", "position": "P", "number": "—", "status": "Minors"},
    {"name": "Paul Gervase", "position": "P", "number": "65", "status": "Minors"},
    {"name": "Ronan Kopp", "position": "P", "number": "83", "status": "Minors"},
    {"name": "Chayce McDermott", "position": "P", "number": "62", "status": "Minors"},
    {"name": "Wyatt Mills", "position": "P", "number": "58", "status": "Minors"},
    {"name": "River Ryan", "position": "P", "number": "77", "status": "Minors"},
    {"name": "Hyeseong Kim", "position": "IF", "number": "6", "status": "Minors"},
    {"name": "Alek Thomas", "position": "OF", "number": "5", "status": "Minors"},
    {"name": "Ryan Ward", "position": "OF", "number": "67", "status": "Minors"}
]

def generate_report(player, stats_text):
    """生成球员报告"""
    player_slug = player['name'].lower().replace(' ', '-')
    output_dir = f"D:\\baseball\\report\\{player_slug}"
    os.makedirs(output_dir, exist_ok=True)
    
    status_note = ""
    if player['status'].startswith('IL'):
        status_note = f"\n> ⚠️ **伤病状态**: {player['status']}\n"
    elif player['status'] == 'Minors':
        status_note = f"\n> 📋 **小联盟**: 目前不在大联盟活跃名单\n"
    
    md_content = f"""# {player['name']} 球探报告

> **Los Angeles Dodgers #{player['number']} | {player['position']}**
{status_note}
> 报告生成时间：2026-07-09

---

## 📋 基本信息

| 项目 | 内容 |
|------|------|
| **姓名** | {player['name']} |
| **背号** | #{player['number']} |
| **位置** | {player['position']} |
| **状态** | {player['status']} |
| **球队** | Los Angeles Dodgers |

---

## 📊 统计数据

```
{stats_text}
```

---

## 📝 备注

此报告为批量生成版本。

数据来源：MLB Stats API
"""
    
    md_path = os.path.join(output_dir, f"{player_slug}-scouting-report.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return output_dir

def main():
    print("=" * 60)
    print("Dodgers IL + Minors Players Scouting Report Generator")
    print("=" * 60)
    print(f"\nTotal players: {len(remaining_players)}\n")
    
    success_count = 0
    failed_players = []
    
    for i, player in enumerate(remaining_players, 1):
        status_icon = "[IL]" if player['status'].startswith('IL') else "[MIN]"
        print(f"[{i:2d}/{len(remaining_players)}] {status_icon} {player['name']:<25} ({player['status']:<8}) ... ", end="", flush=True)
        
        try:
            result = subprocess.run(
                ['python', r'C:\Users\Junkai XIA\.openclaw\workspace\skills\baseball\scripts\baseball.py', 
                 'stats', player['name']],
                capture_output=True, text=True, timeout=30
            )
            
            stats_text = result.stdout if result.returncode == 0 else "Stats not available"
            output_dir = generate_report(player, stats_text)
            
            print("OK")
            success_count += 1
            time.sleep(0.5)
            
        except Exception as e:
            print(f"FAIL: {str(e)[:50]}")
            failed_players.append(player['name'])
    
    print("\n" + "=" * 60)
    print(f"Completed: {success_count}/{len(remaining_players)}")
    if failed_players:
        print(f"Failed ({len(failed_players)}): {', '.join(failed_players)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
