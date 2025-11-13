# Windows 문제 해결 가이드

## 일반적인 문제들

### 1. "python을 찾을 수 없습니다" 오류

**증상:**
```
'python'은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는 배치 파일이 아닙니다.
```

**해결 방법:**

#### 방법 1: Python 설치 확인
```powershell
# Python이 설치되어 있는지 확인
where python
where py
```

#### 방법 2: py 런처 사용
```powershell
# python 대신 py 사용
py --version
py main.py generate
```

#### 방법 3: Python PATH 추가
1. Windows 키 + R → `sysdm.cpl` 입력
2. "고급" 탭 → "환경 변수" 클릭
3. 시스템 변수의 "Path" 선택 → "편집"
4. Python 경로 추가:
   - `C:\Users\[사용자명]\AppData\Local\Programs\Python\Python312`
   - `C:\Users\[사용자명]\AppData\Local\Programs\Python\Python312\Scripts`
5. OK 클릭
6. 명령 프롬프트 재시작

---

### 2. PowerShell 실행 정책 오류

**증상:**
```
이 시스템에서 스크립트를 실행할 수 없으므로 파일을 로드할 수 없습니다.
```

**해결 방법:**

#### 방법 1: 현재 세션만 허용 (안전)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
```

#### 방법 2: 현재 사용자에게 영구 허용
```powershell
# PowerShell을 관리자 권한으로 실행
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 방법 3: activate.bat 사용
```cmd
# CMD에서
venv\Scripts\activate.bat
```

#### 방법 4: 우회 실행
```powershell
PowerShell -ExecutionPolicy Bypass -File .\setup.ps1
```

---

### 3. 한글 경로 문제

**증상:**
- 파일 생성 실패
- 인코딩 오류
- 깨진 문자

**해결 방법:**

#### 방법 1: 영문 경로 사용 (권장)
```
❌ 나쁨: C:\Users\사용자\문서\프로젝트
✅ 좋음: C:\Users\Username\Documents\Projects
```

#### 방법 2: UTF-8 인코딩 설정
```powershell
# PowerShell에서
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING="utf-8"

# 또는 Python 코드 상단에
# -*- coding: utf-8 -*-
```

#### 방법 3: 시스템 로케일 변경
1. 제어판 → 지역 → 관리 탭
2. "시스템 로케일 변경"
3. "Beta: 세계 언어 지원을 위해 Unicode UTF-8 사용" 체크

---

### 4. 가상 환경 활성화 안 됨

**증상:**
```
프롬프트에 (venv)가 나타나지 않음
```

**해결 방법:**

#### PowerShell
```powershell
# 정확한 경로 확인
Get-ChildItem venv\Scripts

# 올바른 활성화 명령
.\venv\Scripts\Activate.ps1
```

#### CMD
```cmd
venv\Scripts\activate.bat
```

#### Git Bash
```bash
source venv/Scripts/activate  # Windows에서는 Scripts (s 소문자)
```

---

### 5. pip 설치 오류

**증상:**
```
ERROR: Could not install packages due to an OSError
```

**해결 방법:**

#### 방법 1: 관리자 권한으로 실행
```powershell
# PowerShell을 관리자 권한으로 실행
Start-Process powershell -Verb runAs
```

#### 방법 2: --user 플래그 사용
```powershell
pip install --user jinja2 click rich
```

#### 방법 3: pip 업그레이드
```powershell
python -m pip install --upgrade pip
```

#### 방법 4: 캐시 삭제
```powershell
pip cache purge
pip install -r requirements.txt
```

---

### 6. 모듈을 찾을 수 없음 오류

**증상:**
```
ModuleNotFoundError: No module named 'jinja2'
```

**해결 방법:**

#### 가상 환경 활성화 확인
```powershell
# 프롬프트에 (venv)가 있는지 확인
# 없으면:
.\venv\Scripts\Activate.ps1

# 설치된 패키지 확인
pip list
```

#### 올바른 Python 사용 확인
```powershell
# 어떤 Python이 실행되는지 확인
where python
# venv\Scripts\python.exe가 나와야 함
```

---

### 7. 파일 인코딩 오류

**증상:**
```
UnicodeDecodeError: 'cp949' codec can't decode byte
```

**해결 방법:**

#### 환경 변수 설정
```powershell
$env:PYTHONIOENCODING="utf-8"
python main.py generate
```

#### 영구 설정
```powershell
# PowerShell 프로필에 추가
notepad $PROFILE

# 다음 줄 추가:
$env:PYTHONIOENCODING="utf-8"
```

---

### 8. "no such file or directory" 오류

**증상:**
```
FileNotFoundError: [Errno 2] No such file or directory
```

**해결 방법:**

#### 현재 디렉토리 확인
```powershell
# 현재 위치 확인
pwd
# 또는
Get-Location

# 프로젝트 디렉토리로 이동
cd mcp-to-code-structure
```

#### 파일 존재 확인
```powershell
# 파일 목록 확인
dir
# 또는
ls

# 필요한 파일이 있는지 확인
Test-Path config\mcp_servers.json
```

---

### 9. npx 또는 Node.js 관련 오류

**증상:**
```
'npx'은(는) 내부 또는 외부 명령... 아닙니다.
```

**해결 방법:**

#### Node.js 설치
1. [nodejs.org](https://nodejs.org/) 방문
2. LTS 버전 다운로드 및 설치
3. 명령 프롬프트 재시작
4. 확인:
```powershell
node --version
npm --version
npx --version
```

---

### 10. 생성된 파일이 열리지 않음

**증상:**
- TypeScript 파일을 클릭해도 아무 일도 안 일어남

**해결 방법:**

#### VS Code 설치 (권장)
1. [code.visualstudio.com](https://code.visualstudio.com/) 방문
2. 다운로드 및 설치
3. 프로젝트 폴더 열기:
```powershell
code .
```

#### 기본 연결 프로그램 설정
1. .ts 파일 우클릭
2. "연결 프로그램" → "다른 앱 선택"
3. VS Code 또는 메모장 선택

---

## 진단 스크립트

문제를 자동으로 진단하려면:

```powershell
# 진단 스크립트 실행
.\diagnose.ps1
```

수동 진단:

```powershell
# Python 확인
python --version
py --version

# 가상 환경 확인
Test-Path venv

# 패키지 확인
pip list

# 경로 확인
$env:PATH -split ';'

# 실행 정책 확인
Get-ExecutionPolicy -List
```

---

## 추가 도움말

### Windows Terminal 권장 설정

```json
// settings.json
{
    "defaultProfile": "{...PowerShell GUID...}",
    "profiles": {
        "defaults": {
            "fontFace": "Cascadia Code",
            "fontSize": 10
        }
    }
}
```

### VS Code 권장 확장

- Python (Microsoft)
- Pylance
- PowerShell

### 유용한 PowerShell 명령어

```powershell
# 빠른 도움말
Get-Help [명령어]

# 명령어 찾기
Get-Command *python*

# 환경 변수 보기
Get-ChildItem Env:

# 프로세스 확인
Get-Process python
```

---

## 여전히 문제가 해결되지 않는다면?

1. **오류 메시지 전체 복사**
2. **실행 환경 정보 수집:**
   ```powershell
   # 시스템 정보
   systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
   
   # Python 정보
   python --version
   pip --version
   
   # PowerShell 정보
   $PSVersionTable
   ```

3. **로그 저장:**
   ```powershell
   python main.py generate 2>&1 | Tee-Object -FilePath error_log.txt
   ```

4. **프로젝트 README 확인**
