#Requires -Version 5.1
param(
    [int]$Port = 8080,
    [string]$BaseDir = "D:\baseball"
)

$ErrorActionPreference = "Continue"

Set-Location $BaseDir

# Prefer the Python installation that has statsapi installed
if (Test-Path "C:\Python314\python.exe") {
    $python = "C:\Python314\python.exe"
} else {
    $python = (Get-Command python).Source
}

& $python portal\update-portal.py
& $python portal\fetch-dashboard-data.py

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
