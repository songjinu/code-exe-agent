"""TypeScript 파일 및 디렉토리 구조 생성"""
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from generator.categorizer import CategoryInfo
from generator.mcp_client import MCPTool


class FileGenerator:
    """파일 생성기"""
    
    def __init__(self, output_dir: str = "output/servers"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Jinja2 환경 설정
        self.env = Environment(
            loader=FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # 커스텀 필터 추가
        self.env.filters['ts_type'] = self._python_to_ts_type
    
    def _python_to_ts_type(self, python_type: str) -> str:
        """Python 타입을 TypeScript 타입으로 변환"""
        type_mapping = {
            'string': 'string',
            'integer': 'number',
            'number': 'number',
            'boolean': 'boolean',
            'array': 'any[]',
            'object': 'Record<string, any>'
        }
        return type_mapping.get(python_type, 'any')
    
    def generate_server_structure(
        self,
        server_name: str,
        categories: Dict[str, CategoryInfo]
    ):
        """서버의 전체 디렉토리 구조 생성"""
        server_dir = self.output_dir / server_name
        server_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📁 {server_name} 디렉토리 구조 생성 중...")
        
        # 각 카테고리별로 디렉토리 생성
        for category_name, category_info in categories.items():
            self._generate_category_dir(
                server_dir,
                server_name,
                category_name,
                category_info
            )
        
        # 서버 루트 README 생성
        self._generate_server_readme(server_dir, server_name, categories)
        
        # metadata.json 생성
        self._generate_server_metadata(server_dir, server_name, categories)
        
        print(f"  ✅ {server_name} 완료")
    
    def _generate_category_dir(
        self,
        server_dir: Path,
        server_name: str,
        category_name: str,
        category_info: CategoryInfo
    ):
        """카테고리 디렉토리 생성"""
        category_dir = server_dir / category_name
        category_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"  📂 {category_name}/")
        
        # 각 도구를 TypeScript 파일로 생성
        for tool in category_info.tools:
            self._generate_tool_file(
                category_dir,
                server_name,
                category_name,
                tool
            )
        
        # 카테고리 README 생성
        self._generate_category_readme(
            category_dir,
            category_info
        )
        
        # 카테고리 metadata.json 생성
        self._generate_category_metadata(
            category_dir,
            category_info
        )
    
    def _generate_tool_file(
        self,
        category_dir: Path,
        server_name: str,
        category_name: str,
        tool: MCPTool
    ):
        """개별 도구 TypeScript 파일 생성"""
        template = self.env.get_template('tool_wrapper.ts.j2')
        
        simple_name = tool.get_simple_name()
        file_path = category_dir / f"{simple_name}.ts"
        
        # 예시 사용법 생성
        example_usage = self._generate_example_usage(
            simple_name,
            tool
        )
        
        content = template.render(
            tool=tool,
            server_name=server_name,
            category_name=category_name,
            function_name=simple_name,
            input_schema=tool.input_schema,
            example_usage=example_usage
        )
        
        file_path.write_text(content)
        print(f"    ✓ {simple_name}.ts")
    
    def _generate_example_usage(self, function_name: str, tool: MCPTool) -> str:
        """사용 예시 코드 생성"""
        # 간단한 예시 생성
        if 'create' in function_name:
            return f"const result = await {function_name}({{ name: 'Example' }});"
        elif 'update' in function_name:
            return f"const result = await {function_name}({{ id: '123', data: {{...}} }});"
        elif 'read' in function_name or 'get' in function_name:
            return f"const result = await {function_name}({{ id: '123' }});"
        elif 'delete' in function_name:
            return f"await {function_name}({{ id: '123' }});"
        else:
            return f"const result = await {function_name}({{...}});"
    
    def _generate_category_readme(
        self,
        category_dir: Path,
        category_info: CategoryInfo
    ):
        """카테고리 README 생성"""
        template = self.env.get_template('category_readme.md.j2')
        
        content = template.render(
            category=category_info,
            generation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        readme_path = category_dir / "README.md"
        readme_path.write_text(content)
    
    def _generate_category_metadata(
        self,
        category_dir: Path,
        category_info: CategoryInfo
    ):
        """카테고리 메타데이터 생성"""
        metadata = {
            "category": category_info.name,
            "description": category_info.description,
            "keywords": category_info.keywords,
            "tool_count": len(category_info.tools),
            "tools": [
                {
                    "name": tool.get_simple_name(),
                    "full_name": tool.name,
                    "description": tool.description
                }
                for tool in category_info.tools
            ],
            "generated_at": datetime.now().isoformat()
        }
        
        metadata_path = category_dir / "metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
    
    def _generate_server_readme(
        self,
        server_dir: Path,
        server_name: str,
        categories: Dict[str, CategoryInfo]
    ):
        """서버 루트 README 생성"""
        total_tools = sum(len(cat.tools) for cat in categories.values())
        
        content = f"""# {server_name}

MCP 서버의 도구들을 카테고리별로 구조화했습니다.

## 통계

- **총 카테고리**: {len(categories)}
- **총 도구**: {total_tools}
- **생성일**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 카테고리

"""
        
        for category_name, category_info in sorted(categories.items()):
            content += f"### {category_name}\n\n"
            content += f"{category_info.description}\n\n"
            content += f"**도구 개수**: {len(category_info.tools)}\n\n"
            content += f"**키워드**: {', '.join(category_info.keywords)}\n\n"
            
            # 도구 목록
            for tool in category_info.tools:
                content += f"- `{tool.get_simple_name()}`: {tool.description}\n"
            
            content += "\n"
        
        content += """## 사용법

```typescript
// 도구 import
import { create } from './accounts/create';
import { update } from './accounts/update';

// 사용
const account = await create({ name: 'Example Corp' });
await update({ id: account.id, data: { status: 'active' } });
```

## 디렉토리 구조

```
"""
        
        # 트리 구조 생성
        for category_name, category_info in sorted(categories.items()):
            content += f"{category_name}/\n"
            for tool in category_info.tools:
                content += f"├── {tool.get_simple_name()}.ts\n"
            content += "├── README.md\n"
            content += "└── metadata.json\n\n"
        
        content += "```\n"
        
        readme_path = server_dir / "README.md"
        readme_path.write_text(content)
    
    def _generate_server_metadata(
        self,
        server_dir: Path,
        server_name: str,
        categories: Dict[str, CategoryInfo]
    ):
        """서버 메타데이터 생성"""
        metadata = {
            "server_name": server_name,
            "generated_at": datetime.now().isoformat(),
            "total_categories": len(categories),
            "total_tools": sum(len(cat.tools) for cat in categories.values()),
            "categories": {
                cat_name: {
                    "description": cat_info.description,
                    "tool_count": len(cat_info.tools),
                    "keywords": cat_info.keywords
                }
                for cat_name, cat_info in categories.items()
            }
        }
        
        metadata_path = server_dir / "metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))


def main():
    """테스트"""
    import asyncio
    from generator.mcp_client import MCPClient
    from generator.categorizer import ToolCategorizer
    
    async def test():
        # MCP 도구 가져오기
        client = MCPClient()
        all_tools = await client.get_all_tools()
        
        # 분류 및 파일 생성
        categorizer = ToolCategorizer()
        generator = FileGenerator()
        
        for server_name, tools in all_tools.items():
            categories = categorizer.categorize_tools(tools)
            generator.generate_server_structure(server_name, categories)
        
        print("\n✅ 모든 파일 생성 완료!")
        print(f"📂 생성 위치: {generator.output_dir.absolute()}")
    
    asyncio.run(test())


if __name__ == "__main__":
    main()
