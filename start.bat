@echo off
cd /d "%~dp0"
start /B "" ".venv\Scripts\python.exe" app.py
timeout /t 5 /nobreak >nul
start /B "" "%TEMP%\cloudflared.exe" tunnel --url http://localhost:5000 > "%cd%\tun3.log" 2>&1
timeout /t 12 /nobreak >nul
echo Tunnel URL:
findstr "https://" tun3.log 2>nul
echo.
echo Verifying...
powershell -Command "& { try { $r = Invoke-WebRequest -Uri (Select-String -Path tun3.log -Pattern 'https://[a-zA-Z0-9-]+\.trycloudflare\.com' | Select-Object -First 1).Matches.Value -TimeoutSec 10; Write-Host ('Status: ' + $r.StatusCode + ' ' + $r.Content.Length + ' bytes') } catch { Write-Host ('Error: ' + $_.Exception.Message) } }"
echo.
echo Processes running. Press Ctrl+C to exit.
pause
