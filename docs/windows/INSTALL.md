# 📦 Windows 설치 가이드

이 가이드는 CodeEx Agent를 원하는 위치에 설치하는 방법입니다.

## 🎯 권장 설치 위치

`D:\jinu\work\codeExAgent`

(물론 다른 위치에도 설치 가능합니다)

## 📥 설치 단계

### 1단계: 프로젝트 다운로드

다운로드한 `codeExAgent` 폴더를 확인하세요.

### 2단계: 원하는 위치로 이동

#### 방법 A: 탐색기 사용

1. `codeExAgent` 폴더를 복사
2. `D:\jinu\work\` 폴더를 엽니다
3. 붙여넣기

최종 경로: `D:\jinu\work\codeExAgent\`

#### 방법 B: 명령줄 사용

```cmd
REM D:\jinu\work 폴더가 없으면 생성
mkdir D:\jinu\work

REM codeExAgent 폴더 이동 (다운로드 폴더에서)
move "%USERPROFILE%\Downloads\codeExAgent" D:\jinu\work\
```

### 3단계: 설치 확인

```cmd
cd D:\jinu\work\codeExAgent
dir
```

다음 파일/폴더가 보여야 합니다:
- `main.py`
- `requirements.txt`
- `config\`
- `src\`
- `scripts\`
- `docs\`

### 4단계: Python 확인

```cmd
python --version
```

Python 3.8 이상이 필요합니다.

### 5단계: 자동 설치 실행

```cmd
cd D:\jinu\work\codeExAgent
scripts\windows\setup.bat
```

또는 PowerShell:

```powershell
cd D:\jinu\work\codeExAgent
.\scripts\windows\setup.ps1
```

## ✅ 설치 확인

설치가 완료되면:

```cmd
scripts\windows\quick-generate.bat
```

`output\servers` 폴더에 파일이 생성되면 성공! 🎉

## 🔧 다른 위치에 설치

예: `C:\Projects\codeExAgent`

```cmd
mkdir C:\Projects
cd C:\Projects
REM codeExAgent 폴더를 여기에 복사/이동
cd codeExAgent
scripts\windows\setup.bat
```

**중요:** 
- ❌ 한글 경로는 피하세요: `C:\Users\사용자\프로젝트`
- ✅ 영문 경로 사용: `C:\Users\Username\Projects`

## 📝 환경 변수 설정 (선택사항)

자주 사용한다면 PATH에 추가:

1. `Windows 키 + R` → `sysdm.cpl`
2. "고급" 탭 → "환경 변수"
3. 사용자 변수 "Path"에 추가:
   ```
   D:\jinu\work\codeExAgent\scripts\windows
   ```

4. 명령 프롬프트 재시작 후:
   ```cmd
   REM 어디서든 실행 가능
   quick-generate.bat
   ```

## 🚀 빠른 시작 바로가기

### 바탕화면 바로가기 만들기

1. `scripts\windows\quick-generate.bat` 우클릭
2. "바로가기 만들기"
3. 바탕화면으로 이동
4. 이름 변경: "CodeEx Agent 생성"

이제 더블클릭만으로 실행! 🎯

### 시작 폴더에 추가

1. `Windows 키 + R` → `shell:startup`
2. 바로가기 복사

## 📂 디렉토리 구조 확인

```
D:\jinu\work\codeExAgent\
├── main.py              ✓
├── requirements.txt     ✓
├── README.md           ✓
├── config\             ✓
│   ├── mcp_servers.json
│   └── categories.json
├── src\                ✓
│   ├── generator\
│   └── templates\
├── scripts\            ✓
│   └── windows\
│       ├── setup.bat
│       ├── run.bat
│       └── quick-generate.bat
├── docs\               ✓
│   ├── windows\
│   ├── examples\
│   └── guides\
└── output\             (생성 후)
    └── servers\
```

## 🆘 문제 해결

### "경로를 찾을 수 없습니다" 오류

```cmd
REM 현재 위치 확인
cd

REM 올바른 경로로 이동
cd /d D:\jinu\work\codeExAgent
```

### 권한 오류

1. 폴더 우클릭 → 속성
2. 보안 탭
3. 사용자 권한 확인

### Python 경로 문제

```cmd
REM Python 위치 확인
where python

REM 없으면 py 사용
where py
py --version
```

## ✨ 설치 완료!

다음 단계:
1. ✅ [docs/windows/START_HERE.md](../windows/START_HERE.md) 읽기
2. ✅ 첫 번째 생성 실행
3. ✅ [docs/examples/usage.md](../examples/usage.md)에서 AI와 사용법 확인

**설치 위치:** `D:\jinu\work\codeExAgent`

**문서:** [docs/windows/START_HERE.md](../windows/START_HERE.md)
