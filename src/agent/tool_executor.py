"""Tool Executor - 실제 MCP 서버를 호출하여 도구 실행"""
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
import os


class ToolExecutor:
    """
    생성된 도구를 실제 MCP 서버에 연결하여 실행
    """
    
    def __init__(self, config_path: str = "config/mcp_servers.json"):
        """
        Args:
            config_path: MCP 서버 설정 파일 경로
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._processes = {}  # 실행 중인 서버 프로세스
    
    def _load_config(self) -> Dict[str, Any]:
        """설정 파일 로드"""
        if not self.config_path.exists():
            raise ValueError(f"설정 파일을 찾을 수 없습니다: {self.config_path}")
        
        with open(self.config_path, encoding='utf-8') as f:
            return json.load(f)
    
    def _get_server_config(self, server_name: str) -> Optional[Dict[str, Any]]:
        """서버 설정 가져오기"""
        if self.config.get("mock_mode", False):
            return None  # Mock 모드
        
        for server in self.config.get("servers", []):
            if server["name"] == server_name:
                return server
        
        return None
    
    async def _start_server(self, server_name: str) -> subprocess.Popen:
        """MCP 서버 프로세스 시작"""
        if server_name in self._processes:
            return self._processes[server_name]
        
        server_config = self._get_server_config(server_name)
        if not server_config:
            raise ValueError(f"서버 설정을 찾을 수 없습니다: {server_name}")
        
        # 환경 변수 준비
        env = os.environ.copy()
        if "env" in server_config:
            for key, value in server_config["env"].items():
                # ${VAR} 형식의 환경 변수 치환
                if value.startswith("${") and value.endswith("}"):
                    var_name = value[2:-1]
                    value = os.environ.get(var_name, "")
                env[key] = value
        
        # 프로세스 시작
        cmd = [server_config["command"]] + server_config.get("args", [])
        
        process = subprocess.Popen(
            cmd,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        self._processes[server_name] = process
        
        # 서버 시작 대기 (간단히)
        await asyncio.sleep(1)
        
        return process
    
    async def _call_mcp_tool(self, server_name: str, tool_name: str, 
                            params: Dict[str, Any]) -> Dict[str, Any]:
        """
        MCP 서버의 도구 호출
        
        Args:
            server_name: 서버 이름
            tool_name: 도구 이름 (예: salesforce__account__create)
            params: 도구 파라미터
            
        Returns:
            실행 결과
        """
        # 서버 시작
        process = await self._start_server(server_name)
        
        # MCP 프로토콜에 따라 요청 구성
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": params
            }
        }
        
        # 요청 전송
        request_json = json.dumps(request) + "\n"
        process.stdin.write(request_json.encode())
        process.stdin.flush()
        
        # 응답 읽기
        response_line = process.stdout.readline().decode()
        response = json.loads(response_line)
        
        if "error" in response:
            raise Exception(f"MCP 오류: {response['error']}")
        
        return response.get("result", {})
    
    def execute(self, server: str, category: str, tool_name: str, 
                params: Dict[str, Any]) -> Dict[str, Any]:
        """
        도구 실행 (동기 인터페이스)
        
        Args:
            server: 서버 이름
            category: 카테고리 이름
            tool_name: 도구 이름 (간단한 이름)
            params: 도구 파라미터
            
        Returns:
            실행 결과
        """
        # Mock 모드 확인
        if self.config.get("mock_mode", False):
            return self._mock_execute(server, category, tool_name, params)
        
        # 전체 도구 이름 구성
        full_tool_name = f"{server}__{category}__{tool_name}"
        
        # 비동기 실행
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 이미 실행 중인 이벤트 루프가 있으면 새로운 루프 사용
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                result = new_loop.run_until_complete(
                    self._call_mcp_tool(server, full_tool_name, params)
                )
            finally:
                new_loop.close()
                asyncio.set_event_loop(loop)
        else:
            result = loop.run_until_complete(
                self._call_mcp_tool(server, full_tool_name, params)
            )
        
        return result
    
    def _mock_execute(self, server: str, category: str, tool_name: str,
                     params: Dict[str, Any]) -> Dict[str, Any]:
        """Mock 모드 실행 (테스트용)"""
        return {
            "status": "success",
            "message": f"Mock execution of {server}.{category}.{tool_name}",
            "params": params,
            "result": {
                "id": "mock_123",
                "created_at": "2025-01-01T00:00:00Z"
            }
        }
    
    def close_all(self):
        """모든 서버 프로세스 종료"""
        for name, process in self._processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()
        
        self._processes.clear()
    
    def __del__(self):
        """소멸자 - 프로세스 정리"""
        self.close_all()
