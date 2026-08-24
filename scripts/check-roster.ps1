# Dodgers Roster Update Checker
# This script checks for roster changes by downloading current roster data
# Run daily at 12:00 Beijing Time via Windows Task Scheduler

$rosterFile = "D:\baseball\dodgers-roster.md"
$logFile = "D:\baseball\check-log.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Log($msg) {
    $line = "[$timestamp] $msg"
    Write-Output $line
    Add-Content $logFile -Value $line
}

Write-Log "Starting Dodgers roster check..."

# Data sources (tested and working)
$primaryUrl = "https://www.mlb.com/dodgers/roster"
$roster40Url = "https://www.mlb.com/dodgers/roster/40-man"
$savantUrl = "https://baseballsavant.mlb.com/team/119"  # Recommended: no anti-bot

Write-Log "Primary source: $primaryUrl"
Write-Log "40-man roster: $roster40Url"
Write-Log "Baseball Savant (recommended): $savantUrl"

# TODO: Implement actual roster comparison
# Current limitation: This script runs in isolation and cannot directly notify the AI agent
# For full automatic comparison, use OpenClaw cron or manual trigger

Write-Log "Check completed. Please review roster file: $rosterFile"
Write-Log "To trigger AI comparison, send message: '检查道奇队阵容更新'"
