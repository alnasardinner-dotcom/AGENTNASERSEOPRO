@echo off
title AGENT NASER SEO PRO SaaS Web Platform
cd /d "%~dp0"
echo ========================================================================
echo                 STARTING AGENT NASER SEO PRO SAAS WEB PLATFORM
echo ========================================================================
echo.
echo Launching Web Server...
echo Opening Web Application in your default browser at http://localhost:8501
echo.
python -m streamlit run web_app.py --server.port 8501
echo.
echo ========================================================================
echo Web Server Stopped. Press any key to exit.
echo ========================================================================
pause
