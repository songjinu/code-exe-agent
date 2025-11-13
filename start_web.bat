@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8

echo.
echo ========================================
echo  CodeEx Agent - Web UI
echo ========================================
echo.

.venv\Scripts\python.exe web_ui.py
