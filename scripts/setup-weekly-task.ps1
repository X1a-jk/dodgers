# Dodgers Weekly Report + Portal Data Update - Setup Script
# Run this script once to create the weekly scheduled task
# Requires: PowerShell with admin privileges

$taskName = "DodgersWeeklyReport"
$taskDescription = "Dodgers Weekly Report + Portal Dashboard Data Refresh - Every Monday at 12:00 Beijing Time"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Task '$taskName' already exists. Removing old task..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Wrap all portal data refresh steps in one offline-capable launcher.
$wrapper = "D:\baseball\scripts\run-weekly-and-portal-update.ps1"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$wrapper`""

# Create the trigger (Every Monday at 12:00)
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "12:00"

# Create settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

# Register the task
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description $taskDescription -RunLevel Highest | Out-Null

Write-Host "Task '$taskName' created successfully."
Write-Host "Schedule: Every Monday at 12:00"
Write-Host "Log file: D:\baseball\logs\weekly-trigger.log"
Write-Host "Flow: Generate weekly report -> Refresh portal dashboard -> Update file index"
