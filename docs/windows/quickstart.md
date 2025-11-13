# 🚀 Windows 빠른 시작 가이드

## 사전 요구사항

- Python 3.8 이상
- pip (Python 패키지 관리자)
- Git (선택사항)

### Python 설치 확인

```powershell
python --version
# 또는
python3 --version
```

## 설치 및 실행

### 1. 프로젝트 디렉토리로 이동

```powershell
cd mcp-to-code-structure
```

### 2. 가상 환경 생성 (권장)

```powershell
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
.\venv\Scripts\activate

# 활성화되면 프롬프트 앞에 (venv) 표시됨
```

### 3. 필수 패키지 설치

```powershell
# 가상 환경 내에서
pip install -r requirements.txt

# 또는 직접 설치
pip install jinja2 click rich
```

### 4. 실행

```powershell
# Mock 데이터로 테스트
python main.py generate

# 생성된 결과 확인
python main.py list-servers

# 특정 서버 상세 정보
python main.py show salesforce
```

## PowerShell 실행 정책 오류 해결

만약 가상 환경 활성화 시 오류가 발생하면:

```powershell
# 현재 PowerShell 세션에만 적용
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 그 다음 다시 활성화
.\venv\Scripts\activate
```

## 생성된 파일 확인

```powershell
# 디렉토리 구조 확인
tree /F output\servers

# 또는
dir output\servers /s
```

## 실제 MCP 서버 연결 (Windows)

### 1. MCP 서버 설정 수정

`config\mcp_servers.json` 파일 수정:

```json
{
  "mock_mode": false,
  "servers": [
    {
      "name": "filesystem",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\YourName\\Documents"],
      "env": {}
    },
    {
      "name": "google-drive",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-gdrive"],
      "env": {
        "GOOGLE_API_KEY": "your-api-key"
      }
    }
  ]
}
```

**주의사항:**
- Windows 경로는 백슬래시(`\`)를 이중으로 사용: `C:\\Users\\...`
- 또는 슬래시(`/`) 사용: `C:/Users/...`

### 2. Node.js 및 npx 설치

MCP 서버들은 주로 Node.js로 작성되므로:

1. [Node.js 공식 사이트](https://nodejs.org/)에서 다운로드
2. 설치 후 확인:
   ```powershell
   node --version
   npx --version
   ```

### 3. 생성 실행

```powershell
python main.py generate
```

## 환경 변수 설정 (Windows)

### 임시 설정 (현재 세션만)

```powershell
$env:GITHUB_TOKEN="your_token_here"
$env:GOOGLE_API_KEY="your_api_key_here"

python main.py generate
```

### 영구 설정

1. **시스템 설정 방법:**
   - `Windows 키 + R` → `sysdm.cpl` 입력
   - "고급" 탭 → "환경 변수" 클릭
   - 사용자 변수에 추가

2. **PowerShell 프로필 방법:**
   ```powershell
   # 프로필 파일 열기
   notepad $PROFILE
   
   # 다음 내용 추가:
   $env:GITHUB_TOKEN="your_token_here"
   $env:GOOGLE_API_KEY="your_api_key_here"
   ```

## 일반적인 Windows 문제 해결

### 문제 1: "python을 찾을 수 없습니다"

**해결:**
```powershell
# py 런처 사용
py --version
py main.py generate

# 또는 Python 경로를 PATH에 추가
```

### 문제 2: 한글 경로 문제

**해결:**
```powershell
# 영문 경로 사용 권장
# 나쁨: C:\Users\사용자\프로젝트
# 좋음: C:\Users\Username\Projects
```

### 문제 3: 파일 인코딩 오류

**해결:**
```powershell
# PowerShell에서 UTF-8 설정
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 또는 환경 변수 설정
$env:PYTHONIOENCODING="utf-8"
```

### 문제 4: "venv\Scripts\activate"가 작동하지 않음

**해결:**
```powershell
# 대신 activate.bat 사용
venv\Scripts\activate.bat

# 또는 PowerShell 스크립트
.\venv\Scripts\Activate.ps1
```

## Windows Terminal 사용 (권장)

Windows 11 또는 Windows 10에서 [Windows Terminal](https://aka.ms/terminal) 사용을 권장합니다:

```powershell
# Windows Terminal에서
cd mcp-to-code-structure
.\venv\Scripts\activate
python main.py generate
```

## 배치 파일로 간편 실행

### setup.bat 생성

```batch
@echo off
echo MCP to Code Structure Generator Setup
echo ========================================

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Setup complete!
echo.
echo To use the tool, run:
echo   venv\Scripts\activate.bat
echo   python main.py generate
pause
```

### run.bat 생성

```batch
@echo off
call venv\Scripts\activate.bat
python main.py generate
pause
```

사용법:
```powershell
# 처음 한 번만
setup.bat

# 실행할 때마다
run.bat
```

## VS Code에서 사용

1. VS Code로 프로젝트 폴더 열기
2. `Ctrl+Shift+P` → "Python: Select Interpreter"
3. `.\venv\Scripts\python.exe` 선택
4. 터미널 열기 (`Ctrl+``)
5. 자동으로 가상 환경 활성화됨

## Git Bash 사용 시

Git Bash를 사용하는 경우:

```bash
# Linux/Mac 스타일 명령어 사용 가능
cd mcp-to-code-structure
python -m venv venv
source venv/Scripts/activate  # Windows에서는 Scripts
pip install -r requirements.txt
python main.py generate
```

## 빠른 시작 체크리스트

- [ ] Python 3.8+ 설치 확인
- [ ] 프로젝트 다운로드/압축 해제
- [ ] 가상 환경 생성
- [ ] 가상 환경 활성화
- [ ] 의존성 패키지 설치
- [ ] `python main.py generate` 실행
- [ ] `output\servers` 폴더 확인

## 다음 단계

✅ Mock 데이터로 테스트 완료
✅ 생성된 구조 확인

이제:
1. 실제 MCP 서버 연결 설정
2. 카테고리 분류 규칙 커스터마이징
3. AI와 함께 사용해보기!

## 도움말

```powershell
# 모든 명령어 보기
python main.py --help

# 특정 명령어 도움말
python main.py generate --help
```

## 문의 및 버그 리포트

문제가 발생하면:
1. Python 버전 확인
2. 오류 메시지 전체 복사
3. 실행 환경 정보 (Windows 버전, PowerShell 버전)
