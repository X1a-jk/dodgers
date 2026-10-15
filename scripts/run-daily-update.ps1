#Requires -Version 5.1
# Dodgers daily update: roster report + schedule/game hub data fetch.
# Called by the DodgersRosterCheck scheduled task every day at 12:00.
# All network access happens here; the portal only reads static files on startup.
param(
    [string]$BaseDir = "D:\baseball",
    [string]$Python = "C:\Python314\python.exe"
)

$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$logFile = "$BaseDir\logs\daily-trigger.log"

function Write-Log($msg) {
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - $msg"
    Add-Content -Path $logFile -Value $line -ErrorAction SilentlyContinue
    Write-Host $line
}

if (-not (Test-Path $Python)) {
    $py = (Get-Command python -ErrorAction SilentlyContinue).Source
    if ($py) { $Python = $py } else { throw "python.exe not found" }
}

Set-Location $BaseDir
$logDir = "$BaseDir\logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

Write-Log "===== Daily update started ====="

$scripts = @(
    @{ Path = "scripts\daily-report.py";          Name = "Daily roster report" },
    @{ Path = "scripts\fetch-schedule-hub.py";    Name = "Schedule & game hub fetch" },
    @{ Path = "scripts\fetch-depth-chart.py";     Name = "Depth chart fetch" },
    @{ Path = "scripts\fetch-injuries.py";        Name = "Injury timeline fetch" },
    @{ Path = "scripts\fetch-farm.py";           Name = "Farm system fetch" },
    @{ Path = "scripts\fetch-prospects.py";      Name = "Pipeline Top 30 prospects fetch" },
    @{ Path = "scripts\fetch-transactions.py";   Name = "Transactions / roster moves fetch" },
    @{ Path = "scripts\fetch-season-roster.py";  Name = "Season roster (yearly archive) fetch" },
    @{ Path = "scripts\fetch-opponent.py";      Name = "Opponent scout fetch" },
    @{ Path = "scripts\fetch-milestones.py";   Name = "Milestones fetch" },
    @{ Path = "scripts\fetch-playoff.py";      Name = "Postseason simulator fetch" },
    @{ Path = "scripts\fetch-postseason.py";    Name = "Postseason bracket tracker fetch" },
    @{ Path = "portal\fetch-dashboard-data.py";   Name = "Dashboard data fetch (standings etc.)" },
    @{ Path = "portal\update-portal.py";          Name = "Portal file index update" }
)

$anyError = $false
foreach ($s in $scripts) {
    $fullPath = Join-Path $BaseDir $s.Path
    Write-Log "[$($s.Name)] Starting: $fullPath"
    try {
        & $Python $fullPath
        if ($LASTEXITCODE -ne 0) {
            Write-Log "[$($s.Name)] Exit code: $LASTEXITCODE"
            $anyError = $true
        } else {
            Write-Log "[$($s.Name)] Done"
        }
    } catch {
        Write-Log "[$($s.Name)] Exception: $_"
        $anyError = $true
    }
}

if ($anyError) {
    Write-Log "===== Daily update finished with errors ====="
    exit 1
} else {
    Write-Log "===== Daily update finished ====="
    exit 0
}
