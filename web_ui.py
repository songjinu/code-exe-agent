#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""웹 UI 서버 - 사용자 질문 입력 및 결과 표시"""
import sys
import os
from pathlib import Path

# Windows UTF-8 설정
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# 프로젝트 루트 추가
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import uvicorn
from dotenv import load_dotenv

from src.workflow import CodeExecutionWorkflow

# .env 파일 로드
load_dotenv()

app = FastAPI(title="CodeEx Agent - AI Code Execution")

# 워크플로우 인스턴스
workflow = None


class QueryRequest(BaseModel):
    """질문 요청 모델"""
    query: str
    execute: bool = True


class QueryResponse(BaseModel):
    """질문 응답 모델"""
    success: bool
    query: str
    generated_code: Optional[dict] = None
    execution_result: Optional[dict] = None
    error: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """서버 시작 시 워크플로우 초기화"""
    global workflow

    # API 키 확인
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  WARNING: ANTHROPIC_API_KEY가 설정되지 않았습니다")
        print("    .env 파일에 API 키를 설정하세요")

    # MCP 구조 확인
    output_dir = Path("output/servers")
    if not output_dir.exists():
        print("⚠️  WARNING: MCP 구조를 찾을 수 없습니다")
        print("    먼저 'python main.py generate'를 실행하세요")
    else:
        try:
            workflow = CodeExecutionWorkflow('output/servers')
            print("✅ CodeEx Agent 워크플로우가 준비되었습니다")
        except Exception as e:
            print(f"❌ 워크플로우 초기화 실패: {e}")


@app.get("/", response_class=HTMLResponse)
async def root():
    """메인 페이지"""
    return """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeEx Agent - AI Code Execution</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }

        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .main-card {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .input-section {
            padding: 40px;
            background: linear-gradient(to right, #f8f9fa, #e9ecef);
            border-bottom: 1px solid #dee2e6;
        }

        .input-group {
            display: flex;
            gap: 10px;
            align-items: stretch;
        }

        #queryInput {
            flex: 1;
            padding: 15px 20px;
            font-size: 16px;
            border: 2px solid #dee2e6;
            border-radius: 10px;
            transition: all 0.3s;
        }

        #queryInput:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        #submitBtn {
            padding: 15px 40px;
            font-size: 16px;
            font-weight: bold;
            color: white;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }

        #submitBtn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        #submitBtn:active {
            transform: translateY(0);
        }

        #submitBtn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        .results-section {
            padding: 40px;
            display: none;
        }

        .results-section.show {
            display: block;
        }

        .result-card {
            margin-bottom: 20px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            overflow: hidden;
        }

        .result-card-header {
            padding: 15px 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .result-card-body {
            padding: 20px;
        }

        .code-block {
            background: #282c34;
            color: #abb2bf;
            padding: 20px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.5;
        }

        .output-block {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            border-left: 4px solid #667eea;
            font-family: monospace;
            white-space: pre-wrap;
        }

        .error-block {
            background: #fff5f5;
            padding: 20px;
            border-radius: 5px;
            border-left: 4px solid #e53e3e;
            color: #c53030;
        }

        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }

        .badge-success {
            background: #d4edda;
            color: #155724;
        }

        .badge-error {
            background: #f8d7da;
            color: #721c24;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 40px;
        }

        .loading.show {
            display: block;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .examples {
            margin-top: 20px;
            padding: 20px;
            background: white;
            border-radius: 10px;
        }

        .examples h3 {
            margin-bottom: 10px;
            color: #495057;
        }

        .example-chip {
            display: inline-block;
            padding: 8px 16px;
            margin: 5px;
            background: #e9ecef;
            border-radius: 20px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .example-chip:hover {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
        }

        .tool-info {
            font-size: 12px;
            color: #6c757d;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 CodeEx Agent</h1>
            <p>AI가 자동으로 코드를 생성하고 실행합니다</p>
        </div>

        <div class="main-card">
            <div class="input-section">
                <div class="input-group">
                    <input
                        type="text"
                        id="queryInput"
                        placeholder="무엇을 도와드릴까요? (예: Create a Salesforce account named 'ACME Corp')"
                        onkeypress="if(event.key==='Enter') submitQuery()"
                    >
                    <button id="submitBtn" onclick="submitQuery()">
                        실행 🎯
                    </button>
                </div>

                <div class="examples">
                    <h3>💡 예제 질문</h3>
                    <span class="example-chip" onclick="setQuery(this.textContent)">
                        Create a Salesforce account named 'ACME Corp'
                    </span>
                    <span class="example-chip" onclick="setQuery(this.textContent)">
                        Search for documents in Google Drive
                    </span>
                    <span class="example-chip" onclick="setQuery(this.textContent)">
                        Update spreadsheet cell A1 with 'Hello World'
                    </span>
                    <span class="example-chip" onclick="setQuery(this.textContent)">
                        Create account and opportunity
                    </span>
                </div>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>AI가 코드를 생성하고 실행 중입니다...</p>
            </div>

            <div class="results-section" id="results">
                <!-- 결과가 여기에 표시됩니다 -->
            </div>
        </div>
    </div>

    <script>
        function setQuery(text) {
            document.getElementById('queryInput').value = text;
        }

        async function submitQuery() {
            const query = document.getElementById('queryInput').value.trim();
            if (!query) {
                alert('질문을 입력해주세요');
                return;
            }

            // UI 업데이트
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('loading').classList.add('show');
            document.getElementById('results').classList.remove('show');

            try {
                const response = await fetch('/api/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query, execute: true })
                });

                const data = await response.json();
                displayResults(data);

            } catch (error) {
                displayError('네트워크 오류: ' + error.message);
            } finally {
                document.getElementById('submitBtn').disabled = false;
                document.getElementById('loading').classList.remove('show');
            }
        }

        function displayResults(data) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';

            if (data.error) {
                resultsDiv.innerHTML = `
                    <div class="result-card">
                        <div class="result-card-header">
                            <span class="badge badge-error">ERROR</span>
                            오류 발생
                        </div>
                        <div class="result-card-body">
                            <div class="error-block">${escapeHtml(data.error)}</div>
                        </div>
                    </div>
                `;
            } else {
                // 생성된 코드
                if (data.generated_code) {
                    const code = data.generated_code;
                    resultsDiv.innerHTML += `
                        <div class="result-card">
                            <div class="result-card-header">
                                <span class="badge badge-success">GENERATED</span>
                                생성된 코드
                            </div>
                            <div class="result-card-body">
                                <p><strong>설명:</strong> ${escapeHtml(code.description)}</p>
                                <div class="tool-info">
                                    <strong>사용된 도구:</strong>
                                    ${code.required_tools.map(t => `${t.server}/${t.category}/${t.tool}`).join(', ') || '없음'}
                                </div>
                                <br>
                                <div class="code-block">${escapeHtml(code.code)}</div>
                                ${code.explanation ? `<p style="margin-top: 15px; color: #6c757d;"><strong>설명:</strong><br>${escapeHtml(code.explanation)}</p>` : ''}
                            </div>
                        </div>
                    `;
                }

                // 실행 결과
                if (data.execution_result) {
                    const exec = data.execution_result;
                    const status = exec.success ? 'SUCCESS' : 'ERROR';
                    const badgeClass = exec.success ? 'badge-success' : 'badge-error';

                    resultsDiv.innerHTML += `
                        <div class="result-card">
                            <div class="result-card-header">
                                <span class="badge ${badgeClass}">${status}</span>
                                실행 결과
                            </div>
                            <div class="result-card-body">
                                ${exec.success ?
                                    `<div class="output-block">${escapeHtml(exec.output || '출력 없음')}</div>
                                     ${exec.return_value ? `<p style="margin-top: 10px;"><strong>반환값:</strong> ${JSON.stringify(exec.return_value)}</p>` : ''}` :
                                    `<div class="error-block">
                                        <strong>오류:</strong> ${escapeHtml(exec.error)}<br><br>
                                        ${exec.traceback ? `<pre>${escapeHtml(exec.traceback)}</pre>` : ''}
                                     </div>`
                                }
                            </div>
                        </div>
                    `;
                }
            }

            resultsDiv.classList.add('show');
        }

        function displayError(message) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = `
                <div class="result-card">
                    <div class="result-card-header">
                        <span class="badge badge-error">ERROR</span>
                        오류
                    </div>
                    <div class="result-card-body">
                        <div class="error-block">${escapeHtml(message)}</div>
                    </div>
                </div>
            `;
            resultsDiv.classList.add('show');
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>
"""


@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """사용자 질문 처리"""
    if not workflow:
        raise HTTPException(
            status_code=503,
            detail="워크플로우가 초기화되지 않았습니다. MCP 구조를 먼저 생성하세요."
        )

    if not os.getenv('ANTHROPIC_API_KEY'):
        raise HTTPException(
            status_code=500,
            detail="ANTHROPIC_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요."
        )

    try:
        # 워크플로우 실행
        result = workflow.run(
            request.query,
            execute=request.execute,
            verbose=False  # 웹 UI에서는 verbose 끔
        )

        return QueryResponse(
            success=result.get("success", False),
            query=result["query"],
            generated_code=result.get("generated_code"),
            execution_result=result.get("execution_result"),
            error=result.get("error")
        )

    except Exception as e:
        return QueryResponse(
            success=False,
            query=request.query,
            error=str(e)
        )


@app.get("/api/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "ok",
        "workflow_ready": workflow is not None,
        "api_key_set": bool(os.getenv('ANTHROPIC_API_KEY')),
        "mcp_structure": Path("output/servers").exists()
    }


def main():
    """서버 실행"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  CodeEx Agent - Web UI                                        ║
║  AI-Powered Code Generation & Execution                       ║
╚═══════════════════════════════════════════════════════════════╝
""")

    print("🚀 서버를 시작합니다...")
    print("📍 URL: http://localhost:8000")
    print("🛑 종료: Ctrl+C\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
