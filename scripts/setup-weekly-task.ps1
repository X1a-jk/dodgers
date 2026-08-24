# Dodgers Weekly Report - Setup Script
# Run this script once to create the weekly scheduled task
# Requires: PowerShell with admin privileges

$taskName = "DodgersWeeklyReport"
$taskDescription = "Dodgers Weekly Report - Every Monday at 12:00 Beijing Time"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Task '$taskName' already exists. Removing old task..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create the action (trigger a log that the AI will detect)
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -Command `"Add-Content -Path 'D:\baseball\weekly-trigger.log' -Value \"`$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Weekly report check triggered'`""

# Create the trigger (Every Monday at 12:00)
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "12:00"

# Create settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

# Register the task
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description $taskDescription -RunLevel Highest

Write-Host "✅ Task '$taskName' created successfully!"
Write-Host "📅 Schedule: Every Monday at 12:00"
Write-Host "📝 Log file: D:\baseball\weekly-trigger.log"
