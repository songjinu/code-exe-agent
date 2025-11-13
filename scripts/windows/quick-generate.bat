@echo off
chcp 65001 >nul
REM CodeEx Agent - 빠른 생성

if not exist venv (
    echo ❌ 가상 환경이 없습니다.
    echo 먼저 scripts\windows\setup.bat을 실행해주세요.
    echo.
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════╗
echo ║  CodeEx Agent - 빠른 생성                  ║
echo ╚════════════════════════════════════════════╝
echo.

call venv\Scripts\activate.bat
python main.py generate

echo.
echo ✅ 생성 완료! output\servers 폴더를 확인하세요.
echo.

REM 자동으로 폴더 열기
if exist output\servers (
    explorer output\servers
)

pause
