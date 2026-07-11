param(
    [switch]$RebuildApk = $false
)

$ErrorActionPreference = "Stop"
$base = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = "$base\.venv\Scripts\python.exe"
$cloudflared = "$env:TEMP\cloudflared.exe"
$startScript = "$base\start_both.py"

Write-Host "=== TrendScope Deployment ===" -ForegroundColor Cyan

# Kill any existing processes
Get-Process -Name "python", "cloudflared" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Start services
Write-Host "Starting Flask + Cloudflare Tunnel..." -ForegroundColor Yellow
$p = Start-Process -NoNewWindow -FilePath $python -ArgumentList $startScript -PassThru
Start-Sleep -Seconds 3

# Wait for tunnel URL
$url = $null
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 2
    $log = Get-Content "$env:TEMP\tunnel_url.log" -ErrorAction SilentlyContinue
    $match = $log | Select-String -Pattern "https://[a-z0-9-]+\.trycloudflare\.com"
    if ($match) {
        $url = $match.Matches[0].Value
        break
    }
    Write-Host "." -NoNewline
}

if (-not $url) {
    Write-Host "`nFailed to get tunnel URL. Check tunnel_url.log" -ForegroundColor Red
    exit 1
}

Write-Host "`n`n=== Public URL ===" -ForegroundColor Green
Write-Host $url -ForegroundColor Green

if ($RebuildApk) {
    Write-Host "`nRebuilding APK with new URL..." -ForegroundColor Yellow
    $androidDir = "$base\android\TrendScope"
    Set-Location $androidDir
    # Ensure JAVA_HOME is set before building
    if (-not $env:JAVA_HOME) { throw "JAVA_HOME environment variable is required for Android builds" }
    & "$androidDir\gradlew.bat" assembleDebug --no-daemon -x test
    if ($LASTEXITCODE -eq 0) {
        Write-Host "APK rebuilt successfully!" -ForegroundColor Green
        Write-Host "Location: $androidDir\app\build\outputs\apk\debug\app-debug.apk" -ForegroundColor Green
    }
}

Write-Host "`nPress Ctrl+C to stop services." -ForegroundColor Cyan
$p.WaitForExit()
