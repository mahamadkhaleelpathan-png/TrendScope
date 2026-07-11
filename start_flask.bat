@echo off
cd /d "%~dp0"
start /B "" ".venv\Scripts\python.exe" app.py > flask_out.log 2>&1
