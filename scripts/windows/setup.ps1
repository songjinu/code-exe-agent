# MCP to Code Structure Generator - PowerShell Setup Script
# UTF-8 인코딩
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "╔════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  MCP to Code Structure Generator Setup    ║" -ForegroundColor Cyan
Write-Host "║  PowerShell Installer                      ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 관리자 권한 확인
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  관리자 권한으로 실행하지 않았습니다." -ForegroundColor Yellow
    Write-Host "일부 기능이 제한될 수 있습니다." -ForegroundColor Yellow
    Write-Host ""
}

# Python 설치 확인
Write-Host "[1/5] Python 설치 확인 중..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python이 설치되어 있지 않습니다." -ForegroundColor Red
    Write-Host ""
    Write-Host "Python 3.8 이상을 설치해주세요:" -ForegroundColor Yellow
    Write-Host "https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "설치 시 'Add Python to PATH' 옵션을 꼭 체크하세요!" -ForegroundColor Yellow
    Read-Host "계속하려면 Enter를 누르세요"
    exit 1
}
Write-Host ""

# 가상 환경 생성
Write-Host "[2/5] 가상 환경 생성 중..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠️  기존 가상 환경이 있습니다." -ForegroundColor Yellow
    $recreate = Read-Host "삭제하고 다시 생성하시겠습니까? (Y/N)"
    if ($recreate -eq "Y" -or $recreate -eq "y") {
        Remove-Item -Recurse -Force venv
        python -m venv venv
        Write-Host "✅ 가상 환경 재생성 완료" -ForegroundColor Green
    } else {
        Write-Host "✅ 기존 가상 환경 사용" -ForegroundColor Green
    }
} else {
    python -m venv venv
    Write-Host "✅ 가상 환경 생성 완료" -ForegroundColor Green
}
Write-Host ""

# 가상 환경 활성화
Write-Host "[3/5] 가상 환경 활성화 중..." -ForegroundColor Yellow
try {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✅ 가상 환경 활성화 완료" -ForegroundColor Green
} catch {
    Write-Host "❌ 가상 환경 활성화 실패" -ForegroundColor Red
    Write-Host ""
    Write-Host "PowerShell 실행 정책 오류가 발생했을 수 있습니다." -ForegroundColor Yellow
    Write-Host "다음 명령어를 실행해보세요:" -ForegroundColor Yellow
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "계속하려면 Enter를 누르세요"
    exit 1
}
Write-Host ""

# pip 업그레이드
Write-Host "[4/5] pip 업그레이드 중..." -ForegroundColor Yellow
python -m pip install --upgrade pip -q
Write-Host "✅ pip 업그레이드 완료" -ForegroundColor Green
Write-Host ""

# 의존성 설치
Write-Host "[5/5] 패키지 설치 중..." -ForegroundColor Yellow
Write-Host "이 작업은 몇 분 정도 걸릴 수 있습니다..." -ForegroundColor Gray
pip install -r requirements.txt -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 패키지 설치 실패" -ForegroundColor Red
    Write-Host ""
    Write-Host "수동으로 설치해보세요:" -ForegroundColor Yellow
    Write-Host "pip install jinja2 click rich" -ForegroundColor Cyan
    Read-Host "계속하려면 Enter를 누르세요"
    exit 1
}
Write-Host "✅ 패키지 설치 완료" -ForegroundColor Green
Write-Host ""

# 테스트 실행
Write-Host "╔════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  설치 완료!                                ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "테스트 실행 중..." -ForegroundColor Yellow
python main.py list-servers 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Mock 데이터를 생성합니다..." -ForegroundColor Yellow
    python main.py generate
}
Write-Host ""

Write-Host "✅ 모든 설치가 완료되었습니다!" -ForegroundColor Green
Write-Host ""
Write-Host "다음 단계:" -ForegroundColor Cyan
Write-Host "  1. .\run.ps1 실행 - 디렉토리 구조 생성" -ForegroundColor White
Write-Host "  2. config\mcp_servers.json 수정 - 실제 MCP 서버 연결" -ForegroundColor White
Write-Host "  3. output\servers\ 폴더 확인 - 생성된 파일 보기" -ForegroundColor White
Write-Host ""
Write-Host "도움말:" -ForegroundColor Cyan
Write-Host "  python main.py --help" -ForegroundColor White
Write-Host ""

Read-Host "계속하려면 Enter를 누르세요"
