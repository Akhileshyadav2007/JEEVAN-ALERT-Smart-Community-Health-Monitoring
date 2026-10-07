@echo off
cd /d "%~dp0"

echo Starting JEEVAN-ALERT...
echo.

start "" http://localhost:8503

python -m streamlit run app.py --server.port 8503

pause