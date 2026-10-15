#Requires -Version 5.1
param(
    [int]$Port = 8080
)

$ErrorActionPreference = "Continue"

$BaseDir = "D:\baseball"
Set-Location $BaseDir

# Prefer the Python installation that has statsapi installed
if (Test-Path "C:\Python314\python.exe") {
    $python = "C:\Python314\python.exe"
} else {
    $python = (Get-Command python).Source
}

# 刷新门户文件索引（每日阵容/周报列表），失败不阻塞启动
try {
    & $python "portal\update-portal.py" | Out-Null
    Write-Host "[INFO] Portal file index refreshed."
} catch {
    Write-Host "[WARN] update-portal.py failed: $_" -ForegroundColor Yellow
}

# Portal data is now fetched ahead of time by the DodgersWeeklyReport scheduled task
# and saved as static JSON. The portal only reads this static data on startup,
# so a bad network will no longer result in all-zero dashboard values.
$dashboardData = Join-Path $BaseDir "portal\dashboard-data.json"
if (-not (Test-Path $dashboardData)) {
    Write-Host "[WARN] Dashboard static data not found: $dashboardData" -ForegroundColor Yellow
    Write-Host "[INFO] Please run the DodgersWeeklyReport scheduled task first, or execute:"
    Write-Host "       python D:\baseball\portal\fetch-dashboard-data.py"
}

# Start server in background, wait for it, then open browser
Write-Host "[INFO] Starting portal server on port $Port ..."
$server = Start-Process -FilePath $python -ArgumentList "portal\server.py", "$Port" -WorkingDirectory $BaseDir -PassThru -WindowStyle Hidden

Start-Sleep -Seconds 2

# Verify server is responding before opening browser
$maxRetry = 10
$started = $false
for ($i = 0; $i -lt $maxRetry; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$Port" -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $started = $true
            break
        }
    } catch {
        Start-Sleep -Seconds 1
    }
}

if (!$started) {
    Write-Host "[ERR] Portal server failed to start. Check that port $Port is not in use." -ForegroundColor Red
    if ($server -and !$server.HasExited) {
        $server | Stop-Process -Force
    }
    exit 1
}

$url = "http://localhost:" + $Port
Write-Host "[INFO] Server ready. Opening browser: $url"
Start-Process $url

# Keep script alive while server runs
try {
    while ($server -and !$server.HasExited) {
        Start-Sleep -Seconds 1
    }
} finally {
    if ($server -and !$server.HasExited) {
        $server | Stop-Process -Force
    }
}
