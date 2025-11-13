# 🎯 Windows 명령어 치트시트

## ⚡ 빠른 명령어

### 한 번만 실행 (처음)

```cmd
setup.bat
```

### 매번 실행

```cmd
quick-generate.bat
```

---

## 📦 배치 파일 (.bat)

### 기본 실행

```cmd
REM 설치
setup.bat

REM 메뉴 실행
run.bat

REM 빠른 생성
quick-generate.bat
```

### 수동 실행

```cmd
REM 가상 환경 활성화
venv\Scripts\activate.bat

REM 생성
python main.py generate

REM 비활성화
deactivate
```

---

## 💻 PowerShell 스크립트 (.ps1)

### 기본 실행

```powershell
# 설치
.\setup.ps1

# 메뉴 실행
.\run.ps1

# 진단
.\diagnose.ps1
```

### 수동 실행

```powershell
# 가상 환경 활성화
.\venv\Scripts\Activate.ps1

# 생성
python main.py generate

# 비활성화
deactivate
```

### 실행 정책 설정

```powershell
# 현재 세션만
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 현재 사용자 (영구)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🐍 Python 명령어

### 기본 작업

```powershell
# 전체 생성
python main.py generate

# 특정 서버만 생성
python main.py generate --server salesforce

# 서버 목록
python main.py list-servers

# 서버 상세 정보
python main.py show salesforce

# 도움말
python main.py --help
```

### 고급 옵션

```powershell
# 출력 디렉토리 지정
python main.py generate --output custom/path

# 설정 파일 지정
python main.py generate --config custom/config.json
```

---

## 📁 파일 & 폴더 작업

### 탐색기

```cmd
REM 출력 폴더 열기
explorer output\servers

REM 설정 폴더 열기
explorer config

REM 현재 폴더 열기
explorer .
```

### 파일 확인

```cmd
REM 파일 목록
dir

REM 하위 폴더 포함
dir /s

REM 트리 구조 (tree 명령어가 있다면)
tree /F output\servers
```

### 파일 편집

```cmd
REM 메모장으로 열기
notepad config\mcp_servers.json

REM VS Code로 열기 (설치되어 있다면)
code .
code config\mcp_servers.json
```

---

## 🔧 가상 환경

### 생성

```cmd
python -m venv venv
```

### 활성화

```cmd
REM CMD
venv\Scripts\activate.bat

REM PowerShell
.\venv\Scripts\Activate.ps1

REM Git Bash
source venv/Scripts/activate
```

### 비활성화

```cmd
deactivate
```

### 삭제 (다시 시작)

```cmd
rmdir /s /q venv
```

---

## 📦 패키지 관리

### 설치

```cmd
REM requirements.txt 사용
pip install -r requirements.txt

REM 개별 설치
pip install jinja2 click rich

REM 특정 버전
pip install jinja2==3.1.0
```

### 확인

```cmd
REM 설치된 패키지 목록
pip list

REM 특정 패키지 정보
pip show jinja2

REM 업데이트 가능한 패키지
pip list --outdated
```

### 업데이트

```cmd
REM pip 자체 업데이트
python -m pip install --upgrade pip

REM 특정 패키지 업데이트
pip install --upgrade jinja2
```

---

## 🐛 디버깅

### 오류 로그 저장

```cmd
python main.py generate > log.txt 2>&1
```

```powershell
python main.py generate 2>&1 | Tee-Object -FilePath log.txt
```

### 상세 출력

```cmd
REM Python 상세 모드
python -v main.py generate

REM pip 상세 모드
pip install -v jinja2
```

### 시스템 정보

```cmd
REM Python 정보
python --version
python -c "import sys; print(sys.executable)"

REM pip 정보
pip --version
pip list

REM 시스템 정보
systeminfo
```

```powershell
# PowerShell 정보
$PSVersionTable

# 환경 변수
Get-ChildItem Env:

# Python 경로
where.exe python
```

---

## 🌍 환경 변수

### 임시 설정 (CMD)

```cmd
set GITHUB_TOKEN=your_token
set GOOGLE_API_KEY=your_key
python main.py generate
```

### 임시 설정 (PowerShell)

```powershell
$env:GITHUB_TOKEN="your_token"
$env:GOOGLE_API_KEY="your_key"
python main.py generate
```

### 영구 설정

1. `Windows 키 + R` → `sysdm.cpl`
2. 고급 탭 → 환경 변수
3. 사용자 변수에 추가

또는 PowerShell:

```powershell
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "your_token", "User")
```

---

## 📂 경로 관련

### 현재 디렉토리

```cmd
REM CMD
cd
echo %CD%

REM PowerShell
pwd
Get-Location
```

### 디렉토리 이동

```cmd
REM 특정 폴더로
cd C:\Users\Username\Projects

REM 상위 폴더로
cd ..

REM 드라이브 변경
D:
```

### 경로 복사

```cmd
REM 현재 경로를 클립보드로
echo %CD% | clip

REM PowerShell
pwd | Set-Clipboard
```

---

## 🔍 찾기 & 검색

### 파일 찾기

```cmd
REM 이름으로 찾기
dir /s *.ts

REM 내용으로 찾기
findstr /s "create" *.ts
```

```powershell
# PowerShell (더 강력함)
Get-ChildItem -Recurse -Filter "*.ts"
Get-ChildItem -Recurse | Select-String "create"
```

### 프로세스 확인

```cmd
REM 실행 중인 Python 확인
tasklist | findstr python
```

```powershell
Get-Process python
```

---

## 🚀 생산성 팁

### 명령 프롬프트 빠르게 열기

1. 탐색기에서 폴더 주소창 클릭
2. `cmd` 입력 후 Enter

또는:

1. 폴더에서 `Shift + 우클릭`
2. "PowerShell 창 여기에 열기"

### 자주 쓰는 명령어 단축

`alias.bat` 만들기:

```cmd
@echo off
doskey g=python main.py generate
doskey ls=python main.py list-servers
doskey s=python main.py show $*
```

실행:
```cmd
alias.bat
g  REM generate 대신
```

### PowerShell 프로필

```powershell
# 프로필 열기
notepad $PROFILE

# 추가할 내용:
function g { python main.py generate }
function ls { python main.py list-servers }
```

---

## 💾 백업 & 복원

### 중요 파일 백업

```cmd
REM 설정 백업
xcopy /s /i config config_backup

REM 생성 결과 백업
xcopy /s /i output\servers output_backup
```

### 복원

```cmd
REM 설정 복원
xcopy /s /y config_backup config

REM 결과 복원
xcopy /s /y output_backup output\servers
```

---

## 🎓 도움말

### Python

```cmd
python --help
python main.py --help
python main.py generate --help
```

### pip

```cmd
pip --help
pip install --help
```

### Git (설치되어 있다면)

```cmd
git --help
git clone --help
```

---

## 🔗 유용한 단축키

### Windows

- `Windows + E` - 탐색기
- `Windows + R` - 실행
- `Windows + X` - 빠른 링크 메뉴
- `Alt + Tab` - 창 전환

### 명령 프롬프트

- `Tab` - 자동 완성
- `↑/↓` - 이전 명령어
- `Ctrl + C` - 중단
- `Ctrl + A` - 줄 시작으로
- `Ctrl + E` - 줄 끝으로

### VS Code

- `Ctrl + `` ` - 터미널 열기
- `Ctrl + Shift + P` - 명령 팔레트
- `Ctrl + K Ctrl + S` - 키보드 단축키

---

이 치트시트를 프린트하거나 북마크해두세요! 📌
