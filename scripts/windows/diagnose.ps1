# MCP to Code Structure Generator - 진단 스크립트
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "╔════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  시스템 진단 도구                          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$issues = 0
$warnings = 0

# 1. Python 확인
Write-Host "[1/8] Python 설치 확인..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        
        if ($major -eq 3 -and $minor -ge 8) {
            Write-Host "  ✅ $pythonVersion" -ForegroundColor Green
        } elseif ($major -eq 3) {
            Write-Host "  ⚠️  $pythonVersion (3.8 이상 권장)" -ForegroundColor Yellow
            $warnings++
        } else {
            Write-Host "  ❌ $pythonVersion (Python 3.8+ 필요)" -ForegroundColor Red
            $issues++
        }
    }
} catch {
    Write-Host "  ❌ Python이 설치되지 않았거나 PATH에 없습니다" -ForegroundColor Red
    Write-Host "     해결: https://www.python.org/downloads/" -ForegroundColor Gray
    $issues++
}

# 2. py 런처 확인
Write-Host "[2/8] py 런처 확인..." -ForegroundColor Yellow
try {
    $pyVersion = py --version 2>&1
    Write-Host "  ✅ $pyVersion" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  py 런처를 사용할 수 없습니다" -ForegroundColor Yellow
    $warnings++
}

# 3. pip 확인
Write-Host "[3/8] pip 확인..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "  ✅ pip 설치됨" -ForegroundColor Green
} catch {
    Write-Host "  ❌ pip을 찾을 수 없습니다" -ForegroundColor Red
    $issues++
}

# 4. 가상 환경 확인
Write-Host "[4/8] 가상 환경 확인..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ✅ 가상 환경 존재" -ForegroundColor Green
    
    if (Test-Path "venv\Scripts\python.exe") {
        Write-Host "  ✅ Python 실행 파일 존재" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Python 실행 파일이 없습니다" -ForegroundColor Red
        $issues++
    }
} else {
    Write-Host "  ⚠️  가상 환경이 없습니다" -ForegroundColor Yellow
    Write-Host "     해결: setup.bat 또는 setup.ps1 실행" -ForegroundColor Gray
    $warnings++
}

# 5. Node.js/npx 확인
Write-Host "[5/8] Node.js 확인..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  ✅ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  Node.js가 설치되지 않음 (MCP 서버 실행에 필요할 수 있음)" -ForegroundColor Yellow
    Write-Host "     설치: https://nodejs.org/" -ForegroundColor Gray
    $warnings++
}

try {
    $npxVersion = npx --version 2>&1
    Write-Host "  ✅ npx 사용 가능" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  npx를 사용할 수 없음" -ForegroundColor Yellow
    $warnings++
}

# 6. 필수 파일 확인
Write-Host "[6/8] 필수 파일 확인..." -ForegroundColor Yellow
$requiredFiles = @(
    "main.py",
    "requirements.txt",
    "config\mcp_servers.json",
    "config\categories.json"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file 없음" -ForegroundColor Red
        $issues++
    }
}

# 7. 패키지 확인 (가상 환경이 있는 경우)
Write-Host "[7/8] Python 패키지 확인..." -ForegroundColor Yellow
if (Test-Path "venv") {
    try {
        & ".\venv\Scripts\activate.ps1"
        $packages = pip list 2>&1
        
        $requiredPackages = @("jinja2", "click", "rich")
        foreach ($pkg in $requiredPackages) {
            if ($packages -match $pkg) {
                Write-Host "  ✅ $pkg 설치됨" -ForegroundColor Green
            } else {
                Write-Host "  ❌ $pkg 미설치" -ForegroundColor Red
                Write-Host "     해결: pip install $pkg" -ForegroundColor Gray
                $issues++
            }
        }
    } catch {
        Write-Host "  ⚠️  패키지 확인 실패" -ForegroundColor Yellow
        $warnings++
    }
} else {
    Write-Host "  ⚠️  가상 환경이 없어 건너뜀" -ForegroundColor Yellow
}

# 8. 실행 정책 확인
Write-Host "[8/8] PowerShell 실행 정책 확인..." -ForegroundColor Yellow
$policy = Get-ExecutionPolicy -Scope CurrentUser
if ($policy -eq "RemoteSigned" -or $policy -eq "Unrestricted") {
    Write-Host "  ✅ 실행 정책: $policy" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  실행 정책: $policy (RemoteSigned 권장)" -ForegroundColor Yellow
    Write-Host "     해결: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Gray
    $warnings++
}

# 결과 요약
Write-Host ""
Write-Host "╔════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  진단 결과                                 ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

if ($issues -eq 0 -and $warnings -eq 0) {
    Write-Host "✅ 모든 검사를 통과했습니다!" -ForegroundColor Green
    Write-Host ""
    Write-Host "다음 단계:" -ForegroundColor Cyan
    Write-Host "  .\run.ps1 또는 run.bat 실행" -ForegroundColor White
} elseif ($issues -eq 0) {
    Write-Host "⚠️  $warnings 개의 경고가 있습니다" -ForegroundColor Yellow
    Write-Host "프로그램은 작동하지만 일부 기능이 제한될 수 있습니다" -ForegroundColor Yellow
} else {
    Write-Host "❌ $issues 개의 문제가 발견되었습니다" -ForegroundColor Red
    if ($warnings -gt 0) {
        Write-Host "⚠️  $warnings 개의 경고도 있습니다" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "위의 오류를 먼저 해결해주세요." -ForegroundColor Yellow
    Write-Host "자세한 내용은 WINDOWS_TROUBLESHOOTING.md를 참조하세요." -ForegroundColor Gray
}

Write-Host ""
Write-Host "시스템 정보:" -ForegroundColor Cyan
Write-Host "  OS: $([System.Environment]::OSVersion.VersionString)" -ForegroundColor Gray
Write-Host "  PowerShell: $($PSVersionTable.PSVersion)" -ForegroundColor Gray
Write-Host "  .NET: $([System.Runtime.InteropServices.RuntimeInformation]::FrameworkDescription)" -ForegroundColor Gray
Write-Host ""

Read-Host "계속하려면 Enter를 누르세요"
