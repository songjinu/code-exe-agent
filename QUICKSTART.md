# 🚀 Quick Start Guide - Code Execution with MCP

MCP 서버의 tools를 기반으로 AI가 자동으로 코드를 생성하고 실행하는 시스템입니다.

## 📋 사전 요구사항

- Python 3.10+
- uv (Python 패키지 관리자)
- Anthropic API Key

## 🔧 설치

### 1. 저장소 클론 또는 다운로드

```bash
cd d:\jinu\work\code_exe_agent
```

### 2. uv 가상환경 생성 및 의존성 설치

```bash
uv venv
uv sync
```

### 3. 환경 변수 설정

```bash
# .env 파일 생성
copy .env.example .env

# .env 파일을 열고 API 키 설정
# ANTHROPIC_API_KEY=your-actual-api-key-here
```

## 📂 1단계: MCP 파일 구조 생성

MCP 서버의 tools 정보를 기반으로 계층적 파일 구조를 생성합니다.

```bash
# 가상환경 활성화
.venv\Scripts\activate

# MCP 구조 생성
python main.py generate
```

생성된 구조 예시:
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

## 🤖 2단계: AI 코드 생성 및 실행

### 대화형 모드 (추천)

```bash
python workflow_cli.py interactive
```

대화형 모드에서 할 수 있는 것:
- 자연어로 질문하면 AI가 코드를 생성하고 실행
- `!servers` - 사용 가능한 서버 목록
- `!search <keyword>` - 도구 검색
- `!tree` - 디렉토리 구조 보기
- `help` - 도움말
- `exit` - 종료

### 단일 질문 모드

```bash
# 코드 생성 및 실행
python workflow_cli.py ask "Create a Salesforce account named 'ACME Corp'"

# 코드만 생성 (실행하지 않음)
python workflow_cli.py ask "Search documents in Google Drive" --no-execute

# 간략한 출력
python workflow_cli.py ask "Update spreadsheet cell" --quiet
```

### Python API 사용

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
┌─────────────────────┐
│  1. 사용자 질문      │
│  "Create account"   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  2. MCP 구조 탐색    │
│  관련 도구 검색      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  3. Claude API      │
│  코드 자동 생성      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  4. 코드 실행        │
│  안전한 Sandbox     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  5. 결과 반환        │
└─────────────────────┘
```

## 📖 예제

### 예제 1: Salesforce 계정 생성

```bash
python workflow_cli.py ask "Create a Salesforce account with name 'ACME' and industry 'Technology'"
```

생성되는 코드:
```python
# Salesforce 계정 생성
result = agent.execute(
    'salesforce',
    'accounts',
    'create',
    {
        'name': 'ACME',
        'industry': 'Technology'
    }
)
print(f"Account created: {result}")
```

### 예제 2: Google Drive 문서 검색

```bash
python workflow_cli.py ask "Search for all documents in Google Drive that contain 'report'"
```

### 예제 3: 복합 작업

```bash
python workflow_cli.py ask "Create a Salesforce account named 'NewCo', then create an opportunity for that account"
```

## 🛠️ CLI 명령어

### 서버 관리

```bash
# 서버 목록
python workflow_cli.py servers

# 도구 검색
python workflow_cli.py search "create"

# 구조 확인
python workflow_cli.py tree
python workflow_cli.py tree salesforce
```

### 코드 실행

```bash
# 대화형 모드
python workflow_cli.py interactive

# 단일 질문
python workflow_cli.py ask "your question here"

# 코드만 생성
python workflow_cli.py ask "your question" --no-execute
```

## 🧪 데모 실행

전체 시스템 테스트를 위한 데모:

```bash
python examples/workflow_demo.py
```

데모 내용:
1. 기본 사용법
2. 코드만 생성
3. 컨텍스트를 포함한 생성
4. 에러 핸들링

## 🔍 문제 해결

### API 키 에러
```
Error: ANTHROPIC_API_KEY가 설정되지 않았습니다
```
→ `.env` 파일에 `ANTHROPIC_API_KEY=your-key` 추가

### MCP 구조 없음
```
Error: MCP 구조를 찾을 수 없습니다
```
→ `python main.py generate` 먼저 실행

### Mock 모드
현재 설정이 mock 모드인 경우:
- `config/mcp_servers.json`에서 `"mock_mode": false`로 변경
- 실제 MCP 서버 설정 추가

## 📚 추가 문서

- [README.md](README.md) - 전체 프로젝트 개요
- [docs/guides/agent_guide.md](docs/guides/agent_guide.md) - Agent 사용법
- [docs/guides/configuration.md](docs/guides/configuration.md) - 설정 가이드

## 🎉 다음 단계

1. 실제 MCP 서버 연결
2. 커스텀 도구 추가
3. 더 복잡한 워크플로우 구성

---

**참고**: [Anthropic - Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
