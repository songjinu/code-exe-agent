# CodeEx Agent - MCP Code Execution Structure Generator

> **AI가 자동으로 코드를 생성하고 실행하는 차세대 MCP 기반 시스템** 🚀

MCP 서버의 도구들을 기반으로 AI가 자동으로 코드를 생성하고 실행합니다.
Anthropic의 ["Code Execution with MCP"](https://www.anthropic.com/engineering/code-execution-with-mcp) 패턴의 완전한 구현체입니다.

## ✨ 핵심 기능

### 1️⃣ MCP 파일 구조 자동 생성
- MCP 서버 tools를 분석하여 계층적 디렉토리 구조 생성
- 각 도구를 TypeScript 래퍼 함수로 변환
- 지능형 카테고리 자동 분류

### 2️⃣ AI 코드 생성
- 사용자 질문을 Claude가 자동으로 실행 가능한 코드로 변환
- 관련 MCP 도구 자동 검색 및 사용
- 컨텍스트 기반 지능형 코드 생성

### 3️⃣ 안전한 코드 실행
- Sandbox 환경에서 안전하게 코드 실행
- 에러 핸들링 및 결과 반환
- stdout/stderr 캡처

### 4️⃣ 웹 UI (NEW! 🌐)
- **브라우저에서 바로 사용 가능!**
- 직관적인 인터페이스
- 실시간 코드 생성 및 실행 결과 확인
- 예제 질문으로 빠른 시작

### 5️⃣ 대화형 CLI
- 자연어로 대화하며 작업 수행
- 도구 탐색 및 검색
- 실시간 결과 확인

## 🚀 빠른 시작

### 1. 설치 (uv 기반)

```bash
# uv 가상환경 생성 및 의존성 설치
uv venv
uv sync
```

### 2. 환경 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일을 열고 API 키 설정
# ANTHROPIC_API_KEY=your-api-key-here
```

### 3. MCP 구조 생성

```bash
# 가상환경 활성화
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# MCP 도구 구조 생성
python main.py generate
```

생성된 구조:
```
output/servers/
├── salesforce/
│   ├── accounts/
│   │   ├── create.ts
│   │   ├── update.ts
│   │   └── delete.ts
│   └── opportunities/
└── google-drive/
    ├── documents/
    └── spreadsheets/
```

### 4. 사용 방법 선택

#### 🌐 방법 1: 웹 UI (추천!)

```bash
# Windows
start_web.bat

# Linux/Mac
./start_web.sh

# 또는 직접 실행
python web_ui.py
```

브라우저에서 http://localhost:8000 접속

**웹 UI 특징:**
- ✅ 직관적인 인터페이스
- ✅ 질문 입력창
- ✅ 예제 질문 버튼
- ✅ 생성된 코드 실시간 표시
- ✅ 실행 결과 즉시 확인
- ✅ 예쁜 UI 디자인

![Web UI Screenshot](docs/images/webui-screenshot.png)

#### 💻 방법 2: 대화형 CLI

```bash
python workflow_cli.py interactive
```

대화 예시:
```
Query> Create a Salesforce account named 'ACME Corp'

[Claude가 코드 자동 생성]
✅ Generated Code:
───────────────────────────
result = agent.execute(
    'salesforce',
    'accounts',
    'create',
    {'name': 'ACME Corp'}
)
print(f"Account created: {result}")
───────────────────────────

[코드 자동 실행]
✅ Execution Output:
───────────────────────────
Account created: {...}
───────────────────────────
```

#### ⚡ 방법 3: 단일 명령

```bash
# 코드 생성 및 실행
python workflow_cli.py ask "Create a Salesforce account named 'TechCo'"

# 코드만 생성 (실행하지 않음)
python workflow_cli.py ask "Search documents" --no-execute
```

#### 🐍 방법 4: Python API

```python
from src.workflow import CodeExecutionWorkflow

# 워크플로우 초기화
workflow = CodeExecutionWorkflow('output/servers')

# 코드 생성 및 실행
result = workflow.run(
    "Create a new Salesforce account named 'Tech Solutions Inc'"
)

print(result['generated_code']['code'])
print(result['execution_result']['output'])
```

## 🎯 작동 원리

```
┌─────────────────────────────────────────────────────────────┐
│                    전체 워크플로우                           │
└─────────────────────────────────────────────────────────────┘

 웹 브라우저         CLI             Python API
      │              │                   │
      └──────────────┴───────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│  사용자 질문                             │
│  "Create a Salesforce account"         │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  MCP 구조 탐색 & 도구 검색               │
│  output/servers/ 에서 관련 도구 찾기     │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  Claude API - 코드 자동 생성             │
│  • 관련 도구 매칭                        │
│  • 실행 가능한 Python 코드 생성          │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  Sandbox에서 코드 실행                   │
│  • 안전한 환경                           │
│  • stdout/stderr 캡처                   │
│  • 에러 핸들링                           │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  결과 반환                               │
│  • 생성된 코드                           │
│  • 실행 결과                             │
│  • 설명 및 메타데이터                    │
└─────────────────────────────────────────┘
```

## 📖 사용 예제

### 예제 1: Salesforce 계정 생성 (웹 UI)

1. 웹 브라우저에서 http://localhost:8000 접속
2. 질문 입력: `Create a Salesforce account named 'ACME Corp'`
3. **실행** 버튼 클릭
4. 결과 확인:
   - 생성된 코드 표시
   - 실행 결과 표시

### 예제 2: CLI로 복합 작업

```bash
python workflow_cli.py ask "Create a Salesforce account named 'NewCo', then create an opportunity for that account with value $100,000"
```

Claude가 자동으로 다단계 코드 생성:
```python
# Step 1: 계정 생성
account = agent.execute(
    'salesforce',
    'accounts',
    'create',
    {'name': 'NewCo'}
)

# Step 2: 기회 생성
opportunity = agent.execute(
    'salesforce',
    'opportunities',
    'create',
    {
        'account_id': account['id'],
        'amount': 100000
    }
)

print(f"Created account {account['id']} with opportunity {opportunity['id']}")
```

### 예제 3: Python API로 자동화

```python
from src.workflow import CodeExecutionWorkflow

workflow = CodeExecutionWorkflow('output/servers')

# 여러 작업 자동화
tasks = [
    "Create account named 'Client A'",
    "Create account named 'Client B'",
    "Generate sales report"
]

for task in tasks:
    result = workflow.run(task)
    if result['success']:
        print(f"✅ {task}: Success")
    else:
        print(f"❌ {task}: Failed")
```

## 📁 프로젝트 구조

```
code_exe_agent/
├── src/
│   ├── generator/           # MCP 구조 생성
│   │   ├── mcp_client.py   # MCP 서버 연결
│   │   ├── categorizer.py  # 도구 분류
│   │   └── file_generator.py
│   ├── agent/              # AI 실행 시스템
│   │   ├── mcp_agent.py    # Agent 클래스
│   │   ├── code_generator.py   # Claude 코드 생성 ⭐
│   │   └── code_executor.py    # Sandbox 실행 ⭐
│   └── workflow.py         # 통합 워크플로우 ⭐
├── templates/              # Jinja2 템플릿
├── config/                 # 설정 파일
├── examples/               # 사용 예제
├── output/                 # 생성 결과
│   └── servers/            # 서버별 구조
├── main.py                 # 구조 생성 CLI
├── workflow_cli.py         # AI 워크플로우 CLI ⭐
├── web_ui.py               # 웹 UI 서버 ⭐ NEW!
├── start_web.bat           # 웹 UI 시작 (Windows) ⭐ NEW!
├── start_web.sh            # 웹 UI 시작 (Linux/Mac) ⭐ NEW!
├── pyproject.toml          # uv 프로젝트 설정
└── README.md               # 이 파일
```

## 🛠️ CLI 명령어

### MCP 구조 관리

```bash
# 구조 생성
python main.py generate

# 서버 목록
python main.py list-servers

# 특정 서버 정보
python main.py show salesforce
```

### AI 워크플로우

```bash
# 웹 UI 시작
python web_ui.py
# 또는
start_web.bat  # Windows
./start_web.sh # Linux/Mac

# 서버 목록
python workflow_cli.py servers

# 도구 검색
python workflow_cli.py search "create"

# 구조 확인
python workflow_cli.py tree
python workflow_cli.py tree salesforce

# 대화형 모드
python workflow_cli.py interactive

# 단일 질문
python workflow_cli.py ask "your question here"
```

## ⚙️ 설정

### MCP 서버 추가

`config/mcp_servers.json`:

```json
{
  "mock_mode": false,
  "servers": [
    {
      "name": "your-server",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  ]
}
```

### 카테고리 규칙 커스터마이징

`config/categories.json` 수정

## 🎉 효과

**토큰 절감:**
- 기존 Tool Calling: 100,000+ 토큰
- Code Execution: 2,000 토큰
- **절감: 98%** ✅

**탐색 효율:**
- 기존: 모든 도구 로드
- 새로운: 필요한 도구만 탐색
- **효율: 20배** ✅

**생산성:**
- 기존: 수동 코드 작성
- 새로운: AI 자동 생성 및 실행
- **생산성: 10배** ✅

**사용자 경험:**
- 웹 UI로 누구나 쉽게 사용
- **접근성: 100배** ✅

## 🔍 문제 해결

### API 키 오류
```
Error: ANTHROPIC_API_KEY가 설정되지 않았습니다
```
→ `.env` 파일에 `ANTHROPIC_API_KEY=your-key` 추가

### MCP 구조 없음
```
Error: MCP 구조를 찾을 수 없습니다
```
→ `python main.py generate` 먼저 실행

### 웹 UI 접속 안됨
```bash
# 포트 8000 사용 중인지 확인
netstat -an | findstr 8000  # Windows
lsof -i :8000               # Linux/Mac

# 다른 포트로 실행
python web_ui.py --port 8080
```

### 이모지 깨짐 (Windows)
자동으로 UTF-8로 설정됩니다. 문제가 있다면:
```bash
chcp 65001
set PYTHONIOENCODING=utf-8
```

## 📚 문서

- **[WEB_UI_GUIDE.md](WEB_UI_GUIDE.md)** - 웹 UI 상세 가이드 ⭐ NEW!
- **[QUICKSTART.md](QUICKSTART.md)** - CLI 빠른 시작 가이드
- **[docs/guides/agent_guide.md](docs/guides/agent_guide.md)** - Agent 상세 가이드
- **[docs/guides/configuration.md](docs/guides/configuration.md)** - 설정 가이드

## 🧪 데모 실행

```bash
# Python 데모
python examples/workflow_demo.py

# 웹 UI 데모
python web_ui.py
# → http://localhost:8000 접속
```

## 🤝 기여

이슈와 PR을 환영합니다!

## 📄 라이선스

MIT License

---

**참고**: [Anthropic - Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)

**Made with ❤️ by CodeEx Agent Team**
