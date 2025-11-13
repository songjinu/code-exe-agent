#!/usr/bin/env python3
"""워크플로우 CLI - 사용자 질문 → 코드 생성 → 실행"""
import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import click
from rich.console import Console
from dotenv import load_dotenv

from src.workflow import CodeExecutionWorkflow

# .env 파일 로드
load_dotenv()

console = Console()


@click.group()
def cli():
    """Code Execution Workflow - MCP 기반 AI 코드 생성 및 실행"""
    pass


@cli.command()
@click.argument('query', required=False)
@click.option('--output', default='output/servers', help='MCP 구조 디렉토리')
@click.option('--no-execute', is_flag=True, help='코드만 생성하고 실행하지 않음')
@click.option('--quiet', is_flag=True, help='간략한 출력')
def ask(query, output, no_execute, quiet):
    """사용자 질문을 받아 코드 생성 및 실행

    Examples:
        workflow_cli.py ask "Create a Salesforce account named 'ACME Corp'"
        workflow_cli.py ask "Search for documents in Google Drive"
    """
    # API 키 확인
    if not os.getenv('ANTHROPIC_API_KEY'):
        console.print("[red]Error: ANTHROPIC_API_KEY가 설정되지 않았습니다[/red]")
        console.print("[yellow]Tip: .env 파일에 ANTHROPIC_API_KEY=your-key 추가[/yellow]")
        sys.exit(1)

    # MCP 구조 확인
    if not Path(output).exists():
        console.print(f"[red]Error: MCP 구조를 찾을 수 없습니다: {output}[/red]")
        console.print("[yellow]Tip: 먼저 'python main.py generate'를 실행하세요[/yellow]")
        sys.exit(1)

    # 대화형 모드
    if not query:
        workflow = CodeExecutionWorkflow(output)
        workflow.interactive_mode()
        return

    # 단일 질문 처리
    try:
        workflow = CodeExecutionWorkflow(output)
        result = workflow.run(
            query,
            execute=not no_execute,
            verbose=not quiet
        )

        if quiet:
            if result["success"]:
                if result.get("execution_result"):
                    print(result["execution_result"]["output"])
            else:
                console.print(f"[red]Error: {result.get('error')}[/red]")
                sys.exit(1)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--output', default='output/servers', help='MCP 구조 디렉토리')
def interactive(output):
    """대화형 모드로 시작"""
    ask.invoke(click.Context(ask), query=None, output=output, no_execute=False, quiet=False)


@cli.command()
@click.option('--output', default='output/servers', help='MCP 구조 디렉토리')
def servers(output):
    """사용 가능한 서버 목록 표시"""
    from src.agent.mcp_agent import MCPAgent

    if not Path(output).exists():
        console.print(f"[red]Error: MCP 구조를 찾을 수 없습니다: {output}[/red]")
        sys.exit(1)

    agent = MCPAgent(output)
    servers = agent.list_servers()

    console.print("\n[bold cyan]Available Servers:[/bold cyan]")
    for server in servers:
        console.print(f"  • {server}")


@cli.command()
@click.argument('keyword')
@click.option('--output', default='output/servers', help='MCP 구조 디렉토리')
def search(keyword, output):
    """키워드로 도구 검색"""
    from src.agent.mcp_agent import MCPAgent

    if not Path(output).exists():
        console.print(f"[red]Error: MCP 구조를 찾을 수 없습니다: {output}[/red]")
        sys.exit(1)

    agent = MCPAgent(output)
    tools = agent.search_tools(keyword)

    console.print(f"\n[bold cyan]Search results for '{keyword}':[/bold cyan]")
    if not tools:
        console.print("[yellow]No tools found[/yellow]")
        return

    for tool in tools[:20]:
        console.print(f"\n[bold]{tool.server}/{tool.category}/{tool.name}[/bold]")
        console.print(f"  {tool.description}")
        if tool.keywords:
            console.print(f"  [dim]Keywords: {', '.join(tool.keywords)}[/dim]")


@cli.command()
@click.option('--output', default='output/servers', help='MCP 구조 디렉토리')
@click.argument('server', required=False)
def tree(output, server):
    """디렉토리 트리 구조 표시"""
    from src.agent.mcp_agent import MCPAgent

    if not Path(output).exists():
        console.print(f"[red]Error: MCP 구조를 찾을 수 없습니다: {output}[/red]")
        sys.exit(1)

    agent = MCPAgent(output)
    console.print(f"\n{agent.get_tree(server)}")


if __name__ == "__main__":
    cli()
