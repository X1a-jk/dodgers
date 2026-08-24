@echo off
echo [%date% %time%] 触发道奇队阵容检查... > D:\baseball\check-log.txt
powershell.exe -ExecutionPolicy Bypass -File "D:\baseball\check-roster.ps1" >> D:\baseball\check-log.txt 2>&1