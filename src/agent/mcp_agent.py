"""MCP Agent - 생성된 구조를 탐색하고 실행하는 Agent"""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ToolInfo:
    """도구 정보"""
    name: str
    server: str
    category: str
    description: str
    input_schema: Optional[Dict[str, Any]] = None
    keywords: List[str] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []


@dataclass
class CategoryInfo:
    """카테고리 정보"""
    name: str
    server: str
    description: str
    tool_count: int
    keywords: List[str]
    tools: List[ToolInfo] = None
    
    def __post_init__(self):
        if self.tools is None:
            self.tools = []


class MCPAgent:
    """
    생성된 MCP 디렉토리 구조를 탐색하고 실행하는 Agent
    
    Usage:
        agent = MCPAgent('output/servers')
        
        # 탐색
        servers = agent.list_servers()
        categories = agent.list_categories('salesforce')
        tools = agent.list_tools('salesforce', 'accounts')
        
        # 실행
        result = agent.execute('salesforce', 'accounts', 'create', {
            'name': 'New Corp'
        })
    """
    
    def __init__(self, output_dir: str = "output/servers"):
        """
        Args:
            output_dir: 생성된 서버 디렉토리 경로
        """
        self.output_dir = Path(output_dir)
        if not self.output_dir.exists():
            raise ValueError(f"출력 디렉토리를 찾을 수 없습니다: {output_dir}")
    
    def list_servers(self) -> List[str]:
        """사용 가능한 서버 목록 반환"""
        servers = []
        for item in self.output_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                servers.append(item.name)
        return sorted(servers)
    
    def list_categories(self, server: str) -> List[CategoryInfo]:
        """서버의 카테고리 목록 반환"""
        server_path = self.output_dir / server
        if not server_path.exists():
            raise ValueError(f"서버를 찾을 수 없습니다: {server}")
        
        # 메타데이터 읽기
        metadata_file = server_path / "metadata.json"
        if not metadata_file.exists():
            raise ValueError(f"메타데이터를 찾을 수 없습니다: {server}")
        
        metadata = json.loads(metadata_file.read_text(encoding='utf-8'))
        
        categories = []
        for cat_name, cat_info in metadata['categories'].items():
            category = CategoryInfo(
                name=cat_name,
                server=server,
                description=cat_info['description'],
                tool_count=cat_info['tool_count'],
                keywords=cat_info['keywords']
            )
            categories.append(category)
        
        return categories
    
    def list_tools(self, server: str, category: str) -> List[ToolInfo]:
        """카테고리의 도구 목록 반환"""
        category_path = self.output_dir / server / category
        if not category_path.exists():
            raise ValueError(f"카테고리를 찾을 수 없습니다: {server}/{category}")
        
        # 카테고리 메타데이터 읽기
        metadata_file = category_path / "metadata.json"
        if not metadata_file.exists():
            raise ValueError(f"메타데이터를 찾을 수 없습니다: {server}/{category}")
        
        metadata = json.loads(metadata_file.read_text(encoding='utf-8'))
        
        tools = []
        for tool_info in metadata['tools']:
            tool = ToolInfo(
                name=tool_info['name'],
                server=server,
                category=category,
                description=tool_info['description'],
                input_schema=tool_info.get('input_schema'),
                keywords=tool_info.get('keywords', [])
            )
            tools.append(tool)
        
        return tools
    
    def get_tool_info(self, server: str, category: str, tool_name: str) -> Optional[ToolInfo]:
        """특정 도구의 상세 정보 반환"""
        tools = self.list_tools(server, category)
        for tool in tools:
            if tool.name == tool_name:
                return tool
        return None
    
    def get_server_info(self, server: str) -> Dict[str, Any]:
        """서버의 전체 정보 반환"""
        metadata_file = self.output_dir / server / "metadata.json"
        if not metadata_file.exists():
            raise ValueError(f"서버 메타데이터를 찾을 수 없습니다: {server}")
        
        return json.loads(metadata_file.read_text(encoding='utf-8'))
    
    def search_tools(self, query: str) -> List[ToolInfo]:
        """키워드로 도구 검색"""
        query_lower = query.lower()
        results = []
        
        for server in self.list_servers():
            for category in self.list_categories(server):
                for tool in self.list_tools(server, category.name):
                    # 이름, 설명, 키워드에서 검색
                    if (query_lower in tool.name.lower() or
                        query_lower in tool.description.lower() or
                        any(query_lower in kw.lower() for kw in tool.keywords)):
                        results.append(tool)
        
        return results
    
    def execute(self, server: str, category: str, tool_name: str, 
                params: Dict[str, Any]) -> Dict[str, Any]:
        """
        도구 실행
        
        Args:
            server: 서버 이름
            category: 카테고리 이름
            tool_name: 도구 이름
            params: 도구 파라미터
            
        Returns:
            실행 결과
        """
        from .tool_executor import ToolExecutor
        
        executor = ToolExecutor()
        return executor.execute(server, category, tool_name, params)
    
    def get_tree(self, server: Optional[str] = None) -> str:
        """디렉토리 트리 구조를 문자열로 반환"""
        lines = []
        
        if server:
            servers = [server]
        else:
            servers = self.list_servers()
        
        for srv in servers:
            lines.append(f"📂 {srv}/")
            categories = self.list_categories(srv)
            
            for i, cat in enumerate(categories):
                is_last_cat = (i == len(categories) - 1)
                prefix = "└── " if is_last_cat else "├── "
                lines.append(f"  {prefix}📂 {cat.name}/ ({cat.tool_count} tools)")
                
                tools = self.list_tools(srv, cat.name)
                for j, tool in enumerate(tools[:3]):  # 처음 3개만
                    is_last_tool = (j == len(tools) - 1) or (j == 2)
                    tool_prefix = "    └── " if is_last_cat else "    │   "
                    if is_last_tool:
                        tool_prefix = tool_prefix.replace("│", " ")
                    lines.append(f"{tool_prefix}📄 {tool.name}.ts")
                
                if len(tools) > 3:
                    tool_prefix = "    └── " if is_last_cat else "    │   "
                    lines.append(f"{tool_prefix}... {len(tools) - 3}개 더")
        
        return "\n".join(lines)
    
    def print_tree(self, server: Optional[str] = None):
        """디렉토리 트리 구조 출력"""
        print(self.get_tree(server))
