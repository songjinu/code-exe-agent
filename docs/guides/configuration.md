# ⚙️ 설정 가이드

## MCP 서버 설정

### 설정 파일 위치
`config\mcp_servers.json`

### Mock 모드와 실제 모드

#### Mock 모드 (테스트용)
```json
{
  "mock_mode": true,
  "mock_servers": {
    "salesforce": {
      "tools": [
        {"name": "salesforce__account__create", "description": "Create account"}
      ]
    }
  }
}
```

#### 실제 모드
```json
{
  "mock_mode": false,
  "servers": [
    {
      "name": "filesystem",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", "."],
      "env": {}
    }
  ]
}
```

### 환경 변수 사용

`.env.example` 파일을 `.env`로 복사:
```
GITHUB_TOKEN=your_token_here
GOOGLE_API_KEY=your_api_key
```

설정 파일에서 참조:
```json
{
  "name": "github",
  "env": {
    "GITHUB_TOKEN": "${GITHUB_TOKEN}"
  }
}
```

## 카테고리 분류 규칙

### 설정 파일 위치
`config\categories.json`

### 새로운 카테고리 추가

```json
{
  "category_rules": {
    "patterns": [
      {
        "pattern": "__(email|mail)__",
        "category": "emails",
        "description": "이메일 관리",
        "keywords": ["email", "mail", "이메일"]
      }
    ]
  }
}
```

### 작동 방식

1. **패턴 매칭**: 도구 이름에서 정규표현식 패턴 찾기
2. **키워드 검색**: 설명에서 키워드 찾기
3. **기본 카테고리**: 매칭 안 되면 "general"

### 예시

도구 이름: `gdrive__email__send`
- `__(email|mail)__` 패턴 매칭
- → `emails` 카테고리로 분류

## 출력 디렉토리 설정

### 기본 위치
`output\servers\`

### 변경 방법
```cmd
python main.py generate --output custom\path
```

### 구조
```
output\servers\
└── [server-name]\
    └── [category]\
        ├── [tool].ts
        ├── README.md
        └── metadata.json
```

## 템플릿 커스터마이징

### 위치
`src\templates\`

### 도구 래퍼 템플릿
`src\templates\tool_wrapper.ts.j2`

수정하여 생성되는 TypeScript 코드 형식 변경 가능

### README 템플릿
`src\templates\category_readme.md.j2`

수정하여 카테고리 README 형식 변경 가능

## 고급 설정

### Python 경로 설정
스크립트에서 다른 Python 사용:
```cmd
set PYTHON_PATH=C:\Python39\python.exe
%PYTHON_PATH% main.py generate
```

### 가상 환경 위치 변경
기본: `venv\`
변경 시: `setup.bat` 수정 필요

## 자주 묻는 질문

**Q: 여러 MCP 서버를 동시에 연결할 수 있나요?**
A: 네, `servers` 배열에 여러 서버 추가 가능합니다.

**Q: 카테고리 이름을 한글로 할 수 있나요?**
A: 디렉토리명은 영문 권장, `description`에 한글 사용하세요.

**Q: 생성된 파일을 수정해도 되나요?**
A: 네, 하지만 재생성 시 덮어써집니다. 백업하세요.

더 많은 정보: [Anthropic MCP 문서](https://modelcontextprotocol.io)
