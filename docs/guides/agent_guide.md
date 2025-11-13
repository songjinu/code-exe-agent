# 🤖 MCP Agent 사용 가이드

생성된 MCP 구조를 실제로 실행할 수 있는 Python Agent입니다.

## 🎯 주요 기능

- ✅ **구조 탐색** - 생성된 서버/카테고리/도구 탐색
- ✅ **도구 검색** - 키워드로 도구 찾기
- ✅ **도구 실행** - 실제 MCP 서버 호출
- ✅ **CLI 도구** - 대화형 명령줄 인터페이스
- ✅ **Python API** - 프로그래밍 방식 사용

## 🚀 빠른 시작

### 1. 구조 생성 (먼저 해야 함)

```cmd
python main.py generate
```

이 명령으로 `output/servers/` 디렉토리가 생성됩니다.

### 2. Agent 사용

#### Python 코드로 사용

```python
from src.agent import MCPAgent

# Agent 초기화
agent = MCPAgent('output/servers')

# 서버 목록
servers = agent.list_servers()
print(servers)  # ['salesforce', 'google-drive']

# 카테고리 목록
categories = agent.list_categories('salesforce')
for cat in categories:
    print(f"{cat.name}: {cat.description}")

# 도구 목록
tools = agent.list_tools('salesforce', 'accounts')
for tool in tools:
    print(f"{tool.name}: {tool.description}")

# 도구 실행
result = agent.execute('salesforce', 'accounts', 'create', {
    'name': 'New Account'
})
print(result)
```

#### CLI로 사용

```cmd
# 서버 목록
python agent_cli.py servers

# 카테고리 목록
python agent_cli.py categories salesforce

# 도구 목록
python agent_cli.py tools salesforce accounts

# 도구 정보
python agent_cli.py info salesforce accounts create

# 도구 검색
python agent_cli.py search "create"

# 트리 구조
python agent_cli.py tree

# 도구 실행
python agent_cli.py run salesforce accounts create --params "{\"name\":\"Test\"}"

# 대화형 모드
python agent_cli.py interactive
```

## 📖 상세 사용법

### Python API

#### 1. 기본 탐색

```python
from src.agent import MCPAgent

agent = MCPAgent('output/servers')

# 서버 목록
servers = agent.list_servers()
# → ['salesforce', 'google-drive']

# 특정 서버 정보
info = agent.get_server_info('salesforce')
# → {'total_categories': 6, 'total_tools': 16, ...}

# 카테고리 목록
categories = agent.list_categories('salesforce')
# → [CategoryInfo(...), CategoryInfo(...), ...]

# 도구 목록
tools = agent.list_tools('salesforce', 'accounts')
# → [ToolInfo(...), ToolInfo(...), ...]

# 특정 도구 정보
tool = agent.get_tool_info('salesforce', 'accounts', 'create')
# → ToolInfo(name='create', description=..., input_schema=...)
```

#### 2. 도구 검색

```python
# 키워드로 검색
results = agent.search_tools('create')

for tool in results:
    print(f"{tool.server}/{tool.category}/{tool.name}")
    print(f"  {tool.description}")
```

#### 3. 도구 실행

```python
# Mock 모드 (테스트용)
result = agent.execute('salesforce', 'accounts', 'create', {
    'name': 'Test Account',
    'type': 'Customer'
})

# 실제 MCP 서버 연결
# config/mcp_servers.json에서 mock_mode: false로 설정
result = agent.execute('salesforce', 'accounts', 'create', {
    'name': 'Real Account'
})
```

#### 4. 트리 구조

```python
# 전체 트리
agent.print_tree()

# 특정 서버만
agent.print_tree('salesforce')

# 문자열로 반환
tree_str = agent.get_tree('salesforce')
```

### CLI 명령어

#### 서버 관련

```cmd
# 서버 목록
python agent_cli.py servers

# 출력 예시:
# 📂 salesforce
#    카테고리: 6개
#    도구: 16개
#    생성: 2025-01-01T00:00:00
```

#### 카테고리 관련

```cmd
# 카테고리 목록
python agent_cli.py categories salesforce

# 출력 예시 (테이블 형식):
# ┌────────────┬─────────────────┬─────────┬──────────────┐
# │ 카테고리    │ 설명             │ 도구 수  │ 키워드        │
# ├────────────┼─────────────────┼─────────┼──────────────┤
# │ accounts   │ 계정 관리        │ 4       │ account, ... │
# └────────────┴─────────────────┴─────────┴──────────────┘
```

#### 도구 관련

```cmd
# 도구 목록
python agent_cli.py tools salesforce accounts

# 도구 상세 정보
python agent_cli.py info salesforce accounts create

# 출력 예시:
# 설명: Create a new account
# 
# 키워드: create, account, new
# 
# 입력 스키마:
# {
#   "type": "object",
#   "properties": {
#     "name": {"type": "string"},
#     "type": {"type": "string"}
#   },
#   "required": ["name"]
# }
```

#### 검색

```cmd
# 키워드 검색
python agent_cli.py search "create"

# 출력 예시 (테이블):
# ┌───────────┬────────────┬────────┬──────────────────┐
# │ 서버      │ 카테고리    │ 도구    │ 설명              │
# ├───────────┼────────────┼────────┼──────────────────┤
# │ salesforce│ accounts   │ create │ Create account   │
# │ salesforce│ opportunity│ create │ Create opportunity│
# └───────────┴────────────┴────────┴──────────────────┘
```

#### 트리

```cmd
# 전체 트리
python agent_cli.py tree

# 특정 서버만
python agent_cli.py tree --server salesforce

# 출력 예시:
# 📂 salesforce/
#   ├── 📂 accounts/ (4 tools)
#   │   ├── 📄 create.ts
#   │   ├── 📄 update.ts
#   │   └── 📄 delete.ts
#   └── 📂 opportunities/ (3 tools)
#       ├── 📄 create.ts
#       └── 📄 close.ts
```

#### 실행

```cmd
# 기본 실행 (Mock 모드)
python agent_cli.py run salesforce accounts create

# 파라미터 전달
python agent_cli.py run salesforce accounts create --params "{\"name\":\"Test Account\"}"

# 출력 예시:
# ✅ 실행 완료
# {
#   "status": "success",
#   "result": {
#     "id": "001...",
#     "name": "Test Account"
#   }
# }
```

#### 대화형 모드

```cmd
python agent_cli.py interactive

# 사용 예시:
mcp > servers
📂 salesforce
📂 google-drive

mcp > use salesforce
✓ 서버: salesforce

mcp > salesforce > categories
📂 accounts (4 tools)
📂 opportunities (3 tools)

mcp > salesforce > use accounts
✓ 카테고리: accounts

mcp > salesforce > accounts > tools
📄 create
📄 update
📄 delete

mcp > salesforce > accounts > run create {"name":"Test"}
✓ 실행 완료
{...}

mcp > salesforce > accounts > back
mcp > salesforce > exit
```

## 🎨 실전 예시

### 예시 1: AI 통합

```python
from src.agent import MCPAgent

class AIAssistant:
    def __init__(self):
        self.agent = MCPAgent('output/servers')
    
    def handle_user_request(self, request: str):
        """사용자 요청 처리"""
        
        # 1. 키워드 추출
        if "계정" in request and "생성" in request:
            # 2. 관련 도구 검색
            tools = self.agent.search_tools("account create")
            
            if tools:
                tool = tools[0]
                
                # 3. 파라미터 준비
                params = self.extract_params(request)
                
                # 4. 실행
                result = self.agent.execute(
                    tool.server,
                    tool.category,
                    tool.name,
                    params
                )
                
                return f"계정이 생성되었습니다: {result}"
        
        return "요청을 이해하지 못했습니다."
```

### 예시 2: 워크플로우 자동화

```python
from src.agent import MCPAgent

def create_account_and_opportunity(account_name: str, opp_name: str):
    """계정과 영업 기회를 순차적으로 생성"""
    agent = MCPAgent('output/servers')
    
    # 1. 계정 생성
    account = agent.execute('salesforce', 'accounts', 'create', {
        'name': account_name
    })
    account_id = account['result']['id']
    
    # 2. 영업 기회 생성
    opportunity = agent.execute('salesforce', 'opportunities', 'create', {
        'name': opp_name,
        'account_id': account_id
    })
    
    return {
        'account': account,
        'opportunity': opportunity
    }
```

### 예시 3: 배치 처리

```python
from src.agent import MCPAgent

def batch_create_accounts(names: list):
    """여러 계정 일괄 생성"""
    agent = MCPAgent('output/servers')
    results = []
    
    for name in names:
        try:
            result = agent.execute('salesforce', 'accounts', 'create', {
                'name': name
            })
            results.append({'name': name, 'status': 'success', 'result': result})
        except Exception as e:
            results.append({'name': name, 'status': 'error', 'error': str(e)})
    
    return results

# 사용
names = ['Company A', 'Company B', 'Company C']
results = batch_create_accounts(names)
```

## 🔧 설정

### Mock 모드 vs 실제 모드

**Mock 모드 (테스트용):**
```json
// config/mcp_servers.json
{
  "mock_mode": true
}
```

**실제 모드:**
```json
{
  "mock_mode": false,
  "servers": [
    {
      "name": "salesforce",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-salesforce"],
      "env": {
        "SALESFORCE_TOKEN": "${SALESFORCE_TOKEN}"
      }
    }
  ]
}
```

### 환경 변수

`.env` 파일 생성:
```
SALESFORCE_TOKEN=your_token
GOOGLE_API_KEY=your_key
```

## 📚 추가 자료

- **예시 코드**: [examples/agent_usage.py](../examples/agent_usage.py)
- **API 문서**: Agent 클래스 docstring 참조
- **설정 가이드**: [configuration.md](configuration.md)

## 💡 팁

1. **먼저 탐색하기**: 도구 실행 전에 `search`로 찾기
2. **스키마 확인**: `info` 명령으로 필수 파라미터 확인
3. **Mock 모드**: 테스트는 Mock 모드로
4. **대화형 모드**: 탐색에는 `interactive` 사용

## 🐛 문제 해결

**Q: "출력 디렉토리를 찾을 수 없습니다"**
A: 먼저 `python main.py generate` 실행

**Q: "Mock 모드에서만 작동합니다"**
A: `config/mcp_servers.json`에서 `mock_mode: false` 설정

**Q: "서버 연결 실패"**
A: MCP 서버 설정 및 환경 변수 확인

더 많은 정보: [troubleshooting.md](../windows/troubleshooting.md)
