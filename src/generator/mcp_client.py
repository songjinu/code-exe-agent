"""MCP 서버 연결 및 도구 정보 가져오기"""
import json
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class MCPTool:
    """MCP 도구 정보"""
    name: str
    description: str
    server_name: str
    input_schema: Optional[Dict[str, Any]] = None
    
    def get_simple_name(self) -> str:
        """도구 이름에서 마지막 부분 추출"""
        parts = self.name.split('__')
        return parts[-1] if len(parts) > 1 else self.name
    
    def get_category_hint(self) -> Optional[str]:
        """도구 이름에서 카테고리 힌트 추출"""
        parts = self.name.split('__')
        if len(parts) >= 3:
            return parts[1]
        return None


class MCPClient:
    """MCP 서버 연결 및 도구 조회"""
    
    def __init__(self, config_path: str = "config/mcp_servers.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """설정 파일 로드"""
        with open(self.config_path) as f:
            return json.load(f)
    
    async def get_all_tools(self) -> Dict[str, List[MCPTool]]:
        """모든 MCP 서버의 도구 가져오기"""
        all_tools = {}
        
        # Mock 모드인 경우
        if self.config.get("mock_mode", False):
            print("Mock 모드로 실행 중...")
            mock_servers = self.config.get("mock_servers", {})

            for server_name, server_data in mock_servers.items():
                tools = []
                for tool_data in server_data.get("tools", []):
                    tools.append(MCPTool(
                        name=tool_data["name"],
                        description=tool_data["description"],
                        server_name=server_name
                    ))
                all_tools[server_name] = tools
                print(f"  OK {server_name}: {len(tools)}개 도구")

        else:
            # 실제 MCP 서버 연결 (TODO: 실제 MCP SDK 사용)
            print("실제 MCP 서버에 연결 중...")
            for server in self.config.get("servers", []):
                try:
                    tools = await self._connect_and_list_tools(server)
                    all_tools[server["name"]] = tools
                    print(f"  OK {server['name']}: {len(tools)}개 도구")
                except Exception as e:
                    print(f"  X {server['name']}: 연결 실패 - {e}")
        
        return all_tools
    
    async def _connect_and_list_tools(self, server_config: Dict) -> List[MCPTool]:
        """실제 MCP 서버 연결 및 도구 목록 가져오기"""
        # TODO: 실제 MCP SDK를 사용한 구현
        # from mcp import ClientSession, StdioServerParameters
        # from mcp.client.stdio import stdio_client
        
        # server_params = StdioServerParameters(
        #     command=server_config["command"],
        #     args=server_config["args"],
        #     env=server_config.get("env")
        # )
        
        # async with stdio_client(server_params) as (read, write):
        #     async with ClientSession(read, write) as session:
        #         await session.initialize()
        #         tools_result = await session.list_tools()
        #         return [
        #             MCPTool(
        #                 name=tool.name,
        #                 description=tool.description,
        #                 server_name=server_config["name"],
        #                 input_schema=tool.inputSchema
        #             )
        #             for tool in tools_result.tools
        #         ]
        
        # 임시로 빈 리스트 반환
        return []


async def main():
    """테스트"""
    client = MCPClient()
    tools = await client.get_all_tools()
    
    print(f"\n총 {len(tools)}개 서버")
    for server_name, server_tools in tools.items():
        print(f"\n{server_name}:")
        for tool in server_tools[:3]:  # 처음 3개만
            print(f"  - {tool.name}: {tool.description}")


if __name__ == "__main__":
    asyncio.run(main())
