# Dodgers Daily Update - Setup Script
# Run this script once to create the daily scheduled task
# Requires: PowerShell with admin privileges

$taskName = "DodgersRosterCheck"
$taskDescription = "Dodgers Daily Roster Report + Schedule Hub Data Refresh - Every day at 12:00 Beijing Time"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Task '$taskName' already exists. Removing old task..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

$wrapper = "D:\baseball\scripts\run-daily-update.ps1"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$wrapper`""

# Create the trigger (Every day at 12:00)
$trigger = New-ScheduledTaskTrigger -Daily -At "12:00"

# Create settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

# Register the task
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description $taskDescription -RunLevel Highest | Out-Null

Write-Host "Task '$taskName' created successfully."
Write-Host "Schedule: Every day at 12:00"
Write-Host "Log file: D:\baseball\logs\daily-trigger.log"
Write-Host "Flow: Generate daily report -> Refresh schedule/game hub data"
