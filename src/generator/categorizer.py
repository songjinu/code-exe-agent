"""MCP 도구를 카테고리별로 분류"""
import json
import re
from typing import List, Dict, Any
from pathlib import Path
from dataclasses import dataclass, field
from generator.mcp_client import MCPTool


@dataclass
class CategoryInfo:
    """카테고리 정보"""
    name: str
    description: str
    keywords: List[str]
    tools: List[MCPTool] = field(default_factory=list)


class ToolCategorizer:
    """도구 분류기"""
    
    def __init__(self, config_path: str = "config/categories.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.patterns = self.config["category_rules"]["patterns"]
        self.default_category = self.config["category_rules"]["default_category"]
    
    def _load_config(self) -> Dict[str, Any]:
        """설정 파일 로드"""
        with open(self.config_path, encoding='utf-8') as f:
            return json.load(f)
    
    def categorize_tools(self, tools: List[MCPTool]) -> Dict[str, CategoryInfo]:
        """도구들을 카테고리별로 분류"""
        categories: Dict[str, CategoryInfo] = {}
        
        for tool in tools:
            category_name = self._determine_category(tool)
            
            # 카테고리가 없으면 생성
            if category_name not in categories:
                category_config = self._get_category_config(category_name)
                categories[category_name] = CategoryInfo(
                    name=category_name,
                    description=category_config["description"],
                    keywords=category_config["keywords"]
                )
            
            # 도구 추가
            categories[category_name].tools.append(tool)
        
        return categories
    
    def _determine_category(self, tool: MCPTool) -> str:
        """도구의 카테고리 결정"""
        tool_name_lower = tool.name.lower()
        
        # 1. 패턴 매칭으로 카테고리 찾기
        for pattern_config in self.patterns:
            pattern = pattern_config["pattern"]
            if re.search(pattern, tool_name_lower):
                return pattern_config["category"]
        
        # 2. 도구 이름에서 카테고리 힌트 추출
        category_hint = tool.get_category_hint()
        if category_hint:
            # 힌트를 복수형으로 변환
            if not category_hint.endswith('s'):
                category_hint += 's'
            return category_hint
        
        # 3. 설명에서 키워드 찾기
        description_lower = tool.description.lower()
        for pattern_config in self.patterns:
            for keyword in pattern_config["keywords"]:
                if keyword in description_lower:
                    return pattern_config["category"]
        
        # 4. 기본 카테고리
        return self.default_category
    
    def _get_category_config(self, category_name: str) -> Dict[str, Any]:
        """카테고리 설정 가져오기"""
        for pattern_config in self.patterns:
            if pattern_config["category"] == category_name:
                return pattern_config
        
        # 기본 설정
        return {
            "description": category_name.replace('_', ' ').title(),
            "keywords": [category_name]
        }
    
    def print_summary(self, categories: Dict[str, CategoryInfo]):
        """분류 결과 요약 출력"""
        print(f"\n📊 분류 결과:")
        for category_name, category_info in sorted(categories.items()):
            print(f"  {category_name}: {len(category_info.tools)}개 도구")
            for tool in category_info.tools:
                print(f"    - {tool.get_simple_name()}")


def main():
    """테스트"""
    import asyncio
    from generator.mcp_client import MCPClient
    
    async def test():
        # MCP 도구 가져오기
        client = MCPClient()
        all_tools = await client.get_all_tools()
        
        # 각 서버별로 분류
        categorizer = ToolCategorizer()
        
        for server_name, tools in all_tools.items():
            print(f"\n{'='*50}")
            print(f"서버: {server_name}")
            print(f"{'='*50}")
            
            categories = categorizer.categorize_tools(tools)
            categorizer.print_summary(categories)
    
    asyncio.run(test())


if __name__ == "__main__":
    main()
