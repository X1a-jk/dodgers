@echo off
echo ==========================================
echo  Dodgers Weekly Report - Task Setup
echo ==========================================
echo.
echo This will create a Windows scheduled task
echo that triggers every Monday at 12:00.
echo.
echo Please run as Administrator if prompted.
echo.
pause

powershell.exe -ExecutionPolicy Bypass -File "%~dp0setup-weekly-task.ps1"

echo.
echo Setup complete! Press any key to exit.
pause