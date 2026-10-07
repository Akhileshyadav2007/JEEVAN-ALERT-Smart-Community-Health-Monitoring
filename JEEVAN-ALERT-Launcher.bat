@echo off
title JEEVAN-ALERT
cd /d "%~dp0"

echo Starting JEEVAN-ALERT...
start "" cmd /c "python -m streamlit run app.py --server.port 8503"

timeout /t 5 /nobreak >nul
start "" "http://localhost:8503"

exit
