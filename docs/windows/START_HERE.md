# 🚀 여기서 시작하세요! (Windows)

이 문서는 Windows에서 CodeEx Agent를 5분 안에 시작하는 방법입니다.

## ⚡ 빠른 시작 (3단계)

### 1단계: Python 확인

명령 프롬프트(CMD)를 열고:
```cmd
python --version
```

**Python 3.8 이상이 필요합니다.**

없다면? → [Python 설치](https://www.python.org/downloads/)
- ⚠️ **"Add Python to PATH" 체크 필수!**

### 2단계: 자동 설치

프로젝트 폴더에서:
```cmd
scripts\windows\setup.bat
```

PowerShell을 사용한다면:
```powershell
.\scripts\windows\setup.ps1
```

### 3단계: 실행

```cmd
scripts\windows\quick-generate.bat
```

끝! 🎉

`output\servers` 폴더를 확인하세요!

---

## 📁 생성된 결과

```
output\servers\
├── salesforce\
│   ├── accounts\
│   │   ├── create.ts
│   │   ├── update.ts
│   │   └── delete.ts
│   ├── opportunities\
│   └── contacts\
└── google-drive\
    ├── documents\
    └── spreadsheets\
```

이것이 바로 AI가 Code Execution에 사용할 구조입니다!

---

## 🎯 다음 단계

### 초보자
1. ✅ [quickstart.md](quickstart.md) - 상세 가이드
2. 📖 [../examples/usage.md](../examples/usage.md) - AI와 함께 사용
3. 🔧 [troubleshooting.md](troubleshooting.md) - 문제 해결

### 경험자
1. 📝 [../guides/configuration.md](../guides/configuration.md) - 설정 방법
2. 🚀 [../examples/advanced.md](../examples/advanced.md) - 고급 사용

---

## 💡 주요 명령어

```cmd
REM 생성
python main.py generate

REM 서버 목록
python main.py list-servers

REM 특정 서버만
python main.py generate --server salesforce

REM 도움말
python main.py --help
```

---

## 🆘 문제가 있나요?

### 자동 진단
```powershell
.\scripts\windows\diagnose.ps1
```

### 일반적인 문제
- [troubleshooting.md](troubleshooting.md) 확인
- [cheatsheet.md](cheatsheet.md) 명령어 참조

---

## 📚 전체 문서

프로젝트 루트의 `docs/` 폴더:
```
docs\
├── windows\          # Windows 가이드
│   ├── START_HERE.md       (이 파일)
│   ├── quickstart.md
│   ├── cheatsheet.md
│   └── troubleshooting.md
├── examples\         # 사용 예시
│   ├── usage.md
│   └── advanced.md
└── guides\           # 상세 가이드
    ├── configuration.md
    └── customization.md
```

---

**프로젝트:** `D:\jinu\work\codeExAgent`

**다음:** [quickstart.md](quickstart.md) 읽기
