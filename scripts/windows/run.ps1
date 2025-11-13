# MCP to Code Structure Generator - PowerShell Run Script
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 가상 환경 확인
if (-not (Test-Path "venv")) {
    Write-Host "❌ 가상 환경이 없습니다." -ForegroundColor Red
    Write-Host ""
    Write-Host "먼저 setup.ps1을 실행해주세요:" -ForegroundColor Yellow
    Write-Host "  .\setup.ps1" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "계속하려면 Enter를 누르세요"
    exit 1
}

# 가상 환경 활성화
try {
    & ".\venv\Scripts\Activate.ps1"
} catch {
    Write-Host "❌ 가상 환경 활성화 실패" -ForegroundColor Red
    Write-Host ""
    Write-Host "실행 정책 설정:" -ForegroundColor Yellow
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Cyan
    Read-Host "계속하려면 Enter를 누르세요"
    exit 1
}

# 메인 메뉴
function Show-Menu {
    Clear-Host
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  MCP to Code Structure Generator          ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. 전체 생성 (모든 서버)" -ForegroundColor White
    Write-Host "2. 특정 서버만 생성" -ForegroundColor White
    Write-Host "3. 서버 목록 보기" -ForegroundColor White
    Write-Host "4. 서버 상세 정보 보기" -ForegroundColor White
    Write-Host "5. 생성된 파일 탐색" -ForegroundColor White
    Write-Host "6. 설정 파일 열기" -ForegroundColor White
    Write-Host "7. 도움말" -ForegroundColor White
    Write-Host "0. 종료" -ForegroundColor White
    Write-Host ""
}

# 메인 루프
do {
    Show-Menu
    $choice = Read-Host "선택하세요 (0-7)"
    
    switch ($choice) {
        "1" {
            Write-Host ""
            Write-Host "전체 서버 생성 중..." -ForegroundColor Yellow
            python main.py generate
            Write-Host ""
            Read-Host "계속하려면 Enter를 누르세요"
        }
        "2" {
            Write-Host ""
            $server = Read-Host "서버 이름을 입력하세요"
            Write-Host ""
            Write-Host "$server 생성 중..." -ForegroundColor Yellow
            python main.py generate --server $server
            Write-Host ""
            Read-Host "계속하려면 Enter를 누르세요"
        }
        "3" {
            Write-Host ""
            python main.py list-servers
            Write-Host ""
            Read-Host "계속하려면 Enter를 누르세요"
        }
        "4" {
            Write-Host ""
            $server = Read-Host "서버 이름을 입력하세요"
            Write-Host ""
            python main.py show $server
            Write-Host ""
            Read-Host "계속하려면 Enter를 누르세요"
        }
        "5" {
            Write-Host ""
            if (Test-Path "output\servers") {
                Write-Host "생성된 파일 탐색기로 열기..." -ForegroundColor Green
                explorer output\servers
            } else {
                Write-Host "❌ output\servers 폴더가 없습니다." -ForegroundColor Red
                Write-Host "먼저 '1. 전체 생성'을 실행해주세요." -ForegroundColor Yellow
            }
            Write-Host ""
            Read-Host "계속하려면 Enter를 누르세요"
        }
        "6" {
            Write-Host ""
            Write-Host "1. MCP 서버 설정" -ForegroundColor White
            Write-Host "2. 카테고리 규칙" -ForegroundColor White
            Write-Host ""
            $configChoice = Read-Host "선택하세요 (1-2)"
            
            if ($configChoice -eq "1") {
                notepad config\mcp_servers.json
            } elseif ($configChoice -eq "2") {
                notepad config\categories.json
            }
        }
        "7" {
            Write-Host ""
            python main.py --help
            Write-Host ""
            Read-Host "계속하려면 Enter를 누르세요"
        }
        "0" {
            Write-Host ""
            Write-Host "프로그램을 종료합니다." -ForegroundColor Yellow
            Write-Host ""
            break
        }
        default {
            Write-Host ""
            Write-Host "잘못된 선택입니다." -ForegroundColor Red
            Start-Sleep -Seconds 1
        }
    }
} while ($choice -ne "0")
