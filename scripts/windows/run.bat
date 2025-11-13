@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════╗
echo ║  CodeEx Agent                              ║
echo ╚════════════════════════════════════════════╝
echo.

REM 가상 환경 확인
if not exist venv (
    echo ❌ 가상 환경이 없습니다.
    echo.
    echo 먼저 scripts\windows\setup.bat을 실행해주세요:
    echo   scripts\windows\setup.bat
    echo.
    pause
    exit /b 1
)

REM 가상 환경 활성화
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 가상 환경 활성화 실패
    pause
    exit /b 1
)

REM 메뉴 표시
:menu
cls
echo.
echo ╔════════════════════════════════════════════╗
echo ║  CodeEx Agent                              ║
echo ╚════════════════════════════════════════════╝
echo.
echo 1. 전체 생성 (모든 서버)
echo 2. 특정 서버만 생성
echo 3. 서버 목록 보기
echo 4. 서버 상세 정보 보기
echo 5. 생성된 파일 탐색
echo 6. 설정 파일 열기
echo 7. 문서 보기
echo 8. 도움말
echo 0. 종료
echo.
set /p choice="선택하세요 (0-8): "

if "%choice%"=="1" goto generate_all
if "%choice%"=="2" goto generate_specific
if "%choice%"=="3" goto list_servers
if "%choice%"=="4" goto show_server
if "%choice%"=="5" goto explore_output
if "%choice%"=="6" goto open_config
if "%choice%"=="7" goto open_docs
if "%choice%"=="8" goto help
if "%choice%"=="0" goto end
goto menu

:generate_all
echo.
echo 전체 서버 생성 중...
python main.py generate
echo.
pause
goto menu

:generate_specific
echo.
set /p server="서버 이름을 입력하세요: "
echo.
echo %server% 생성 중...
python main.py generate --server %server%
echo.
pause
goto menu

:list_servers
echo.
python main.py list-servers
echo.
pause
goto menu

:show_server
echo.
set /p server="서버 이름을 입력하세요: "
echo.
python main.py show %server%
echo.
pause
goto menu

:explore_output
echo.
if exist output\servers (
    echo 생성된 파일 탐색기로 열기...
    explorer output\servers
) else (
    echo ❌ output\servers 폴더가 없습니다.
    echo 먼저 "1. 전체 생성"을 실행해주세요.
)
echo.
pause
goto menu

:open_config
echo.
echo 1. MCP 서버 설정
echo 2. 카테고리 규칙
echo.
set /p config_choice="선택하세요 (1-2): "
if "%config_choice%"=="1" (
    notepad config\mcp_servers.json
) else if "%config_choice%"=="2" (
    notepad config\categories.json
)
goto menu

:open_docs
echo.
echo 1. 시작 가이드
echo 2. 빠른 시작
echo 3. 명령어 치트시트
echo 4. 문제 해결
echo 5. 사용 예시
echo.
set /p doc_choice="선택하세요 (1-5): "
if "%doc_choice%"=="1" (
    notepad docs\windows\START_HERE.md
) else if "%doc_choice%"=="2" (
    notepad docs\windows\quickstart.md
) else if "%doc_choice%"=="3" (
    notepad docs\windows\cheatsheet.md
) else if "%doc_choice%"=="4" (
    notepad docs\windows\troubleshooting.md
) else if "%doc_choice%"=="5" (
    notepad docs\examples\usage.md
)
goto menu

:help
echo.
python main.py --help
echo.
pause
goto menu

:end
echo.
echo 프로그램을 종료합니다.
echo.
exit /b 0
