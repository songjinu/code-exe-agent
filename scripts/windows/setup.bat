@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════╗
echo ║  CodeEx Agent Setup                        ║
echo ║  Windows Installer                         ║
echo ╚════════════════════════════════════════════╝
echo.

REM Python 설치 확인
echo [1/5] Python 설치 확인 중...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않습니다.
    echo.
    echo Python 3.8 이상을 설치해주세요:
    echo https://www.python.org/downloads/
    echo.
    echo 설치 시 "Add Python to PATH" 옵션을 꼭 체크하세요!
    pause
    exit /b 1
)
python --version
echo ✅ Python 확인 완료
echo.

REM 가상 환경 생성
echo [2/5] 가상 환경 생성 중...
if exist venv (
    echo ⚠️  기존 가상 환경이 있습니다. 삭제하고 다시 생성하시겠습니까? (Y/N)
    set /p recreate="선택: "
    if /i "%recreate%"=="Y" (
        rmdir /s /q venv
        python -m venv venv
        echo ✅ 가상 환경 재생성 완료
    ) else (
        echo ✅ 기존 가상 환경 사용
    )
) else (
    python -m venv venv
    echo ✅ 가상 환경 생성 완료
)
echo.

REM 가상 환경 활성화
echo [3/5] 가상 환경 활성화 중...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 가상 환경 활성화 실패
    echo.
    echo PowerShell에서 실행 정책 오류가 발생한 경우:
    echo 1. PowerShell을 관리자 권한으로 실행
    echo 2. Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    echo 3. 다시 setup.bat 실행
    pause
    exit /b 1
)
echo ✅ 가상 환경 활성화 완료
echo.

REM pip 업그레이드
echo [4/5] pip 업그레이드 중...
python -m pip install --upgrade pip -q
echo ✅ pip 업그레이드 완료
echo.

REM 의존성 설치
echo [5/5] 패키지 설치 중...
echo 이 작업은 몇 분 정도 걸릴 수 있습니다...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo ❌ 패키지 설치 실패
    echo.
    echo 수동으로 설치해보세요:
    echo pip install jinja2 click rich
    pause
    exit /b 1
)
echo ✅ 패키지 설치 완료
echo.

REM 테스트 실행
echo ╔════════════════════════════════════════════╗
echo ║  설치 완료!                                ║
echo ╚════════════════════════════════════════════╝
echo.
echo 테스트 실행 중...
python main.py list-servers >nul 2>&1
if errorlevel 1 (
    echo.
    echo Mock 데이터를 생성합니다...
    python main.py generate
)
echo.

echo ✅ 모든 설치가 완료되었습니다!
echo.
echo 다음 단계:
echo   1. scripts\windows\run.bat 실행 - 메뉴 방식 사용
echo   2. scripts\windows\quick-generate.bat - 빠른 생성
echo   3. config\mcp_servers.json 수정 - 실제 MCP 서버 연결
echo   4. output\servers\ 폴더 확인 - 생성된 파일 보기
echo.
echo 문서:
echo   docs\windows\START_HERE.md - 시작 가이드
echo   docs\windows\quickstart.md - 빠른 시작
echo.
pause
