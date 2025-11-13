#!/usr/bin/env python3
"""
MCP Agent CLI - 대화형 명령줄 도구

생성된 MCP 구조를 탐색하고 실행할 수 있는 CLI 도구입니다.
"""
import sys
import json
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src'))

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich import box

from agent.mcp_agent import MCPAgent

console = Console()


@click.group()
def cli():
    """MCP Agent CLI - 생성된 MCP 구조 탐색 및 실행"""
    pass


@cli.command()
@click.option('--output', default='output/servers', help='서버 디렉토리 경로')
def servers(output):
    """사용 가능한 서버 목록 표시"""
    try:
        agent = MCPAgent(output)
        server_list = agent.list_servers()
        
        if not server_list:
            console.print("[yellow]⚠️  사용 가능한 서버가 없습니다.[/yellow]")
            return
        
        console.print(Panel.fit(
            f"[bold cyan]사용 가능한 서버[/bold cyan] ({len(server_list)}개)",
            border_style="cyan"
        ))
        
        for server in server_list:
            info = agent.get_server_info(server)
            console.print(f"\n[bold yellow]📂 {server}[/bold yellow]")
            console.print(f"   카테고리: {info['total_categories']}개")
            console.print(f"   도구: {info['total_tools']}개")
            console.print(f"   생성: {info['generated_at']}")
        
    except Exception as e:
        console.print(f"[red]❌ 오류: {e}[/red]")


@cli.command()
@click.argument('server')
@click.option('--output', default='output/servers', help='서버 디렉토리 경로')
def categories(server, output):
    """서버의 카테고리 목록 표시"""
    try:
        agent = MCPAgent(output)
        cat_list = agent.list_categories(server)
        
        if not cat_list:
            console.print(f"[yellow]⚠️  {server}에 카테고리가 없습니다.[/yellow]")
            return
        
        console.print(Panel.fit(
            f"[bold cyan]{server}[/bold cyan] 카테고리 ({len(cat_list)}개)",
            border_style="cyan"
        ))
        
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("카테고리", style="yellow")
        table.add_column("설명", style="white")
        table.add_column("도구 수", justify="right", style="cyan")
        table.add_column("키워드", style="dim")
        
        for cat in cat_list:
            table.add_row(
                cat.name,
                cat.description,
                str(cat.tool_count),
                ", ".join(cat.keywords[:3]) + ("..." if len(cat.keywords) > 3 else "")
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]❌ 오류: {e}[/red]")


@cli.command()
@click.argument('server')
@click.argument('category')
@click.option('--output', default='output/servers', help='서버 디렉토리 경로')
def tools(server, category, output):
    """카테고리의 도구 목록 표시"""
    try:
        agent = MCPAgent(output)
        tool_list = agent.list_tools(server, category)
        
        if not tool_list:
            console.print(f"[yellow]⚠️  {server}/{category}에 도구가 없습니다.[/yellow]")
            return
        
        console.print(Panel.fit(
            f"[bold cyan]{server}/{category}[/bold cyan] 도구 ({len(tool_list)}개)",
            border_style="cyan"
        ))
        
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("도구", style="yellow")
        table.add_column("설명", style="white", no_wrap=False)
        
        for tool in tool_list:
            table.add_row(tool.name, tool.description)
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]❌ 오류: {e}[/red]")


@cli.command()
@click.argument('server')
@click.argument('category')
@click.argument('tool')
@click.option('--output', default='output/servers', help='서버 디렉토리 경로')
def info(server, category, tool, output):
    """도구의 상세 정보 표시"""
    try:
        agent = MCPAgent(output)
        tool_info = agent.get_tool_info(server, category, tool)
        
        if not tool_info:
            console.print(f"[red]❌ 도구를 찾을 수 없습니다: {server}/{category}/{tool}[/red]")
            return
        
        console.print(Panel.fit(
            f"[bold cyan]{server}/{category}/{tool}[/bold cyan]",
            border_style="cyan"
        ))
        
        console.print(f"\n[bold]설명:[/bold]")
        console.print(f"  {tool_info.description}")
        
        if tool_info.keywords:
            console.print(f"\n[bold]키워드:[/bold]")
            console.print(f"  {', '.join(tool_info.keywords)}")
        
        if tool_info.input_schema:
            console.print(f"\n[bold]입력 스키마:[/bold]")
            schema_json = json.dumps(tool_info.input_schema, indent=2, ensure_ascii=False)
            syntax = Syntax(schema_json, "json", theme="monokai", line_numbers=True)
            console.print(syntax)
        
    except Exception as e:
        console.print(f"[red]❌ 오류: {e}[/red]")


@cli.command()
@click.argument('query')
@click.option('--output', default='output/servers', help='서버 디렉토리 경로')
def search(query, output):
    """키워드로 도구 검색"""
    try:
        agent = MCPAgent(output)
        results = agent.search_tools(query)
        
        if not results:
            console.print(f"[yellow]⚠️  '{query}'에 대한 검색 결과가 없습니다.[/yellow]")
            return
        
        console.print(Panel.fit(
            f"[bold cyan]'{query}'[/bold cyan] 검색 결과 ({len(results)}개)",
            border_style="cyan"
        ))
        
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("서버", style="cyan")
        table.add_column("카테고리", style="yellow")
        table.add_column("도구", style="green")
        table.add_column("설명", style="white", no_wrap=False)
        
        for tool in results:
            table.add_row(
                tool.server,
                tool.category,
                tool.name,
                tool.description[:50] + "..." if len(tool.description) > 50 else tool.description
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]❌ 오류: {e}[/red]")


@cli.command()
@click.argument('server')
@click.argument('category')
@click.argument('tool')
@click.option('--params', help='JSON 형식의 파라미터')
@click.option('--output', default='output/servers', help='서버 디렉토리 경로')
def run(server, category, tool, params, output):
    """도구 실행"""
    try:
        agent = MCPAgent(output)
        
        # 파라미터 파싱
        if params:
            try:
                params_dict = json.loads(params)
            except json.JSONDecodeError:
                console.print("[red]❌ 잘못된 JSON 형식입니다.[/red]")
                return
        else:
            params_dict = {}
        
        console.print(f"[cyan]실행 중: {server}/{category}/{tool}[/cyan]")
        console.print(f"[dim]파라미터: {params_dict}[/dim]\n")
        
        # 실행
        result = agent.execute(server, category, tool, params_dict)
        
        # 결과 출력
        console.print(Panel.fit(
            "[bold green]✅ 실행 완료[/bold green]",
            border_style="green"
        ))
        
        result_json = json.dumps(result, indent=2, ensure_ascii=False)
        syntax = Syntax(result_json, "json", theme="monokai", line_numbers=True)
        console.print(syntax)
        
    except Exception as e:
        console.print(f"[red]❌ 오류: {e}[/red]")


@cli.command()
@click.option('--server', help='특정 서버만 표시')
@click.option('--output', default='output/servers', help='서버 디렉토리 경로')
def tree(server, output):
    """디렉토리 트리 구조 표시"""
    try:
        agent = MCPAgent(output)
        
        console.print(Panel.fit(
            "[bold cyan]MCP 서버 구조[/bold cyan]",
            border_style="cyan"
        ))
        
        console.print()
        agent.print_tree(server)
        
    except Exception as e:
        console.print(f"[red]❌ 오류: {e}[/red]")


@cli.command()
@click.option('--output', default='output/servers', help='서버 디렉토리 경로')
def interactive(output):
    """대화형 모드 (REPL)"""
    console.print(Panel.fit(
        "[bold cyan]MCP Agent 대화형 모드[/bold cyan]\n"
        "명령어: servers, use <server>, categories, use <category>, tools, run <tool>, exit",
        border_style="cyan"
    ))
    
    try:
        agent = MCPAgent(output)
        current_server = None
        current_category = None
        
        while True:
            # 프롬프트 구성
            prompt_parts = ["mcp"]
            if current_server:
                prompt_parts.append(current_server)
            if current_category:
                prompt_parts.append(current_category)
            prompt = " > ".join(prompt_parts) + " > "
            
            try:
                cmd = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                console.print("\n[yellow]종료합니다.[/yellow]")
                break
            
            if not cmd:
                continue
            
            parts = cmd.split()
            command = parts[0]
            args = parts[1:]
            
            try:
                if command == "exit" or command == "quit":
                    break
                
                elif command == "servers":
                    for srv in agent.list_servers():
                        console.print(f"📂 {srv}")
                
                elif command == "use":
                    if not args:
                        console.print("[red]사용법: use <server|category>[/red]")
                        continue
                    
                    target = args[0]
                    
                    if not current_server:
                        # 서버 선택
                        if target in agent.list_servers():
                            current_server = target
                            console.print(f"[green]✓[/green] 서버: {current_server}")
                        else:
                            console.print(f"[red]서버를 찾을 수 없습니다: {target}[/red]")
                    else:
                        # 카테고리 선택
                        categories = agent.list_categories(current_server)
                        cat_names = [c.name for c in categories]
                        if target in cat_names:
                            current_category = target
                            console.print(f"[green]✓[/green] 카테고리: {current_category}")
                        else:
                            console.print(f"[red]카테고리를 찾을 수 없습니다: {target}[/red]")
                
                elif command == "categories":
                    if not current_server:
                        console.print("[red]먼저 서버를 선택하세요: use <server>[/red]")
                        continue
                    
                    for cat in agent.list_categories(current_server):
                        console.print(f"📂 {cat.name} ({cat.tool_count} tools)")
                
                elif command == "tools":
                    if not current_server or not current_category:
                        console.print("[red]먼저 서버와 카테고리를 선택하세요[/red]")
                        continue
                    
                    for tool in agent.list_tools(current_server, current_category):
                        console.print(f"📄 {tool.name}")
                
                elif command == "run":
                    if not current_server or not current_category:
                        console.print("[red]먼저 서버와 카테고리를 선택하세요[/red]")
                        continue
                    
                    if not args:
                        console.print("[red]사용법: run <tool> [params_json][/red]")
                        continue
                    
                    tool_name = args[0]
                    params = json.loads(args[1]) if len(args) > 1 else {}
                    
                    result = agent.execute(current_server, current_category, tool_name, params)
                    console.print("[green]✓[/green] 실행 완료")
                    console.print(json.dumps(result, indent=2, ensure_ascii=False))
                
                elif command == "back":
                    if current_category:
                        current_category = None
                    elif current_server:
                        current_server = None
                    console.print("[green]✓[/green] 뒤로")
                
                elif command == "help":
                    console.print("""
사용 가능한 명령어:
  servers              - 서버 목록
  use <name>          - 서버 또는 카테고리 선택
  categories          - 현재 서버의 카테고리
  tools               - 현재 카테고리의 도구
  run <tool> [params] - 도구 실행
  back                - 이전 단계로
  exit, quit          - 종료
  help                - 도움말
                    """)
                
                else:
                    console.print(f"[red]알 수 없는 명령어: {command}[/red]")
                    console.print("[dim]'help' 입력으로 도움말 확인[/dim]")
            
            except Exception as e:
                console.print(f"[red]오류: {e}[/red]")
    
    except Exception as e:
        console.print(f"[red]❌ 오류: {e}[/red]")


if __name__ == "__main__":
    cli()
