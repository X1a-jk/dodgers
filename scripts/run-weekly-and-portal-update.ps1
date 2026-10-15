#Requires -Version 5.1
# Dodgers weekly report + portal dashboard data refresh.
# Called by the DodgersWeeklyReport scheduled task every Monday at 12:00.
# All network access happens here; the portal only reads static files on startup.
param(
    [string]$BaseDir = "D:\baseball",
    [string]$Python = "C:\Python314\python.exe"
)

$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$logFile = "$BaseDir\logs\weekly-trigger.log"

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

Write-Log "===== Weekly data refresh started ====="

$scripts = @(
    @{ Path = "scripts\generate-weekly.py";     Name = "Weekly report" },
    @{ Path = "portal\fetch-dashboard-data.py"; Name = "Dashboard data fetch" },
    @{ Path = "portal\update-portal.py";       Name = "Portal file index update" }
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
    Write-Log "===== Weekly data refresh finished with errors ====="
    exit 1
} else {
    Write-Log "===== Weekly data refresh finished ====="
    exit 0
}
