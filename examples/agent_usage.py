"""
MCP Agent 사용 예시

생성된 MCP 구조를 Python 코드에서 사용하는 방법을 보여줍니다.
"""
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from agent.mcp_agent import MCPAgent


def example_1_list_servers():
    """예시 1: 서버 목록 조회"""
    print("=" * 60)
    print("예시 1: 서버 목록 조회")
    print("=" * 60)
    
    agent = MCPAgent('output/servers')
    servers = agent.list_servers()
    
    print(f"\n사용 가능한 서버: {len(servers)}개")
    for server in servers:
        print(f"  - {server}")


def example_2_explore_structure():
    """예시 2: 구조 탐색"""
    print("\n" + "=" * 60)
    print("예시 2: 구조 탐색")
    print("=" * 60)
    
    agent = MCPAgent('output/servers')
    
    # 서버 선택
    servers = agent.list_servers()
    if not servers:
        print("사용 가능한 서버가 없습니다.")
        return
    
    server = servers[0]
    print(f"\n서버: {server}")
    
    # 카테고리 목록
    categories = agent.list_categories(server)
    print(f"카테고리: {len(categories)}개")
    for cat in categories[:3]:  # 처음 3개만
        print(f"  📂 {cat.name}")
        print(f"     설명: {cat.description}")
        print(f"     도구: {cat.tool_count}개")
        print(f"     키워드: {', '.join(cat.keywords[:5])}")


def example_3_search_tools():
    """예시 3: 도구 검색"""
    print("\n" + "=" * 60)
    print("예시 3: 도구 검색")
    print("=" * 60)
    
    agent = MCPAgent('output/servers')
    
    # 'create'가 포함된 도구 검색
    query = "create"
    results = agent.search_tools(query)
    
    print(f"\n'{query}' 검색 결과: {len(results)}개")
    for tool in results[:5]:  # 처음 5개만
        print(f"  📄 {tool.server}/{tool.category}/{tool.name}")
        print(f"     {tool.description}")


def example_4_get_tool_info():
    """예시 4: 도구 상세 정보"""
    print("\n" + "=" * 60)
    print("예시 4: 도구 상세 정보")
    print("=" * 60)
    
    agent = MCPAgent('output/servers')
    
    # 첫 번째 서버의 첫 번째 카테고리의 첫 번째 도구
    servers = agent.list_servers()
    if not servers:
        print("사용 가능한 서버가 없습니다.")
        return
    
    server = servers[0]
    categories = agent.list_categories(server)
    if not categories:
        print("사용 가능한 카테고리가 없습니다.")
        return
    
    category = categories[0].name
    tools = agent.list_tools(server, category)
    if not tools:
        print("사용 가능한 도구가 없습니다.")
        return
    
    tool = tools[0]
    
    print(f"\n도구: {server}/{category}/{tool.name}")
    print(f"설명: {tool.description}")
    
    if tool.input_schema:
        print("\n입력 스키마:")
        import json
        print(json.dumps(tool.input_schema, indent=2, ensure_ascii=False))


def example_5_execute_tool():
    """예시 5: 도구 실행 (Mock 모드)"""
    print("\n" + "=" * 60)
    print("예시 5: 도구 실행 (Mock 모드)")
    print("=" * 60)
    
    agent = MCPAgent('output/servers')
    
    # Mock 모드로 실행
    servers = agent.list_servers()
    if not servers:
        print("사용 가능한 서버가 없습니다.")
        return
    
    server = servers[0]
    categories = agent.list_categories(server)
    if not categories:
        return
    
    category = categories[0].name
    tools = agent.list_tools(server, category)
    if not tools:
        return
    
    tool_name = tools[0].name
    
    print(f"\n실행: {server}/{category}/{tool_name}")
    
    # 파라미터 예시
    params = {
        "name": "Test Account",
        "type": "Customer"
    }
    
    print(f"파라미터: {params}")
    
    try:
        result = agent.execute(server, category, tool_name, params)
        print("\n결과:")
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"오류: {e}")


def example_6_tree_structure():
    """예시 6: 트리 구조 출력"""
    print("\n" + "=" * 60)
    print("예시 6: 트리 구조")
    print("=" * 60)
    
    agent = MCPAgent('output/servers')
    
    print("\n전체 구조:")
    agent.print_tree()


def example_7_programmatic_workflow():
    """예시 7: 프로그래밍 방식 워크플로우"""
    print("\n" + "=" * 60)
    print("예시 7: 프로그래밍 방식 워크플로우")
    print("=" * 60)
    
    agent = MCPAgent('output/servers')
    
    # 시나리오: "create" 작업을 수행하는 도구 찾기
    create_tools = agent.search_tools("create")
    
    print(f"\n'create' 도구 발견: {len(create_tools)}개")
    
    # 각 도구의 정보 출력
    for tool in create_tools[:3]:
        print(f"\n도구: {tool.server}/{tool.category}/{tool.name}")
        
        # 스키마가 있으면 필수 필드 확인
        if tool.input_schema and "required" in tool.input_schema:
            print(f"  필수 파라미터: {', '.join(tool.input_schema['required'])}")


def example_8_ai_integration():
    """예시 8: AI 통합 시나리오"""
    print("\n" + "=" * 60)
    print("예시 8: AI 통합 시나리오")
    print("=" * 60)
    
    agent = MCPAgent('output/servers')
    
    print("\nAI가 사용할 수 있는 함수들:")
    print("""
    # 1. 탐색 함수
    def list_available_servers():
        return agent.list_servers()
    
    def list_server_categories(server: str):
        return [c.name for c in agent.list_categories(server)]
    
    def list_category_tools(server: str, category: str):
        return [t.name for t in agent.list_tools(server, category)]
    
    # 2. 검색 함수
    def search_tools_by_keyword(keyword: str):
        results = agent.search_tools(keyword)
        return [(t.server, t.category, t.name, t.description) 
                for t in results]
    
    # 3. 실행 함수
    def execute_tool(server: str, category: str, tool: str, params: dict):
        return agent.execute(server, category, tool, params)
    """)
    
    # 예시: AI가 "salesforce에서 계정 생성" 요청을 처리
    print("\nAI 시나리오: '계정 생성하기'")
    print("1. 'account' 키워드로 검색")
    
    account_tools = agent.search_tools("account")
    print(f"   → {len(account_tools)}개 도구 발견")
    
    if account_tools:
        tool = account_tools[0]
        print(f"\n2. 도구 선택: {tool.server}/{tool.category}/{tool.name}")
        print(f"   설명: {tool.description}")
        
        print("\n3. 파라미터 준비 및 실행")
        print("   params = {'name': 'AI Created Account'}")
        print(f"   result = execute_tool('{tool.server}', '{tool.category}', '{tool.name}', params)")


def main():
    """모든 예시 실행"""
    print("""
╔════════════════════════════════════════════════════════════╗
║                  MCP Agent 사용 예시                        ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    try:
        example_1_list_servers()
        example_2_explore_structure()
        example_3_search_tools()
        example_4_get_tool_info()
        example_5_execute_tool()
        example_6_tree_structure()
        example_7_programmatic_workflow()
        example_8_ai_integration()
        
        print("\n" + "=" * 60)
        print("모든 예시 실행 완료!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
