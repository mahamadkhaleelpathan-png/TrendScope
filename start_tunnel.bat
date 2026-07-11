@echo off
cd /d "PROJECT_ROOT"
echo %date% %time% Starting tunnel... >> tunnel_url.log
"%TEMP%\cloudflared.exe" tunnel --url http://localhost:5000 >> tunnel_url.log 2>&1
