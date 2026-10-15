@echo off
echo ==========================================
echo  Dodgers Daily Update - Task Setup
echo ==========================================
echo.
echo This will create a Windows scheduled task
echo that triggers every day at 12:00.
echo.
echo Please run as Administrator if prompted.
echo.
pause

powershell.exe -ExecutionPolicy Bypass -File "%~dp0setup-daily-task.ps1"

echo.
echo Setup complete! Press any key to exit.
pause
