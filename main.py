#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeEx Agent - MCP to Code Structure Generator

MCP 서버의 도구들을 분석하여 Code Execution에 최적화된
계층적 디렉토리 구조를 자동 생성합니다.
"""
import sys
import asyncio
import os
from pathlib import Path

# Windows에서 UTF-8 인코딩 강제 설정
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src'))

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.tree import Tree

from generator.mcp_client import MCPClient
from generator.categorizer import ToolCategorizer
from generator.file_generator import FileGenerator

console = Console()


@click.group()
def cli():
    """CodeEx Agent - MCP Code Execution Structure Generator"""
    pass


@cli.command()
@click.option('--config', default='config/mcp_servers.json', help='MCP 서버 설정 파일')
@click.option('--output', default='output/servers', help='출력 디렉토리')
@click.option('--server', help='특정 서버만 생성 (선택사항)')
def generate(config, output, server):
    """MCP 서버 기반 디렉토리 구조 생성"""
    asyncio.run(_generate(config, output, server))


async def _generate(config_path: str, output_dir: str, specific_server: str = None):
    """실제 생성 로직"""
    
    # 헤더 출력
    console.print(Panel.fit(
        "[bold cyan]CodeEx Agent[/bold cyan]\n"
        "MCP 서버 → 계층적 코드 구조 자동 생성",
        border_style="cyan"
    ))
    
    try:
        # 1. MCP 도구 가져오기
        console.print("\n[bold]1️⃣  MCP 서버 연결 및 도구 조회[/bold]")
        client = MCPClient(config_path)
        all_tools = await client.get_all_tools()

        if not all_tools:
            console.print("[red]❌ 도구를 찾을 수 없습니다.[/red]")
            return

        # 특정 서버만 처리
        if specific_server:
            if specific_server not in all_tools:
                console.print(f"[red]❌ 서버 '{specific_server}'를 찾을 수 없습니다.[/red]")
                return
            all_tools = {specific_server: all_tools[specific_server]}

        total_tools = sum(len(tools) for tools in all_tools.values())
        console.print(f"   ✅ {len(all_tools)}개 서버, 총 {total_tools}개 도구")

        # 2. 도구 분류
        console.print("\n[bold]2️⃣  도구 분류[/bold]")
        categorizer = ToolCategorizer()
        
        all_categories = {}
        for server_name, tools in all_tools.items():
            categories = categorizer.categorize_tools(tools)
            all_categories[server_name] = categories
            console.print(f"   {server_name}: {len(categories)}개 카테고리")
        
        # 3. 파일 생성
        console.print("\n[bold]3️⃣  파일 구조 생성[/bold]")
        generator = FileGenerator(output_dir)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            for server_name, categories in all_categories.items():
                task = progress.add_task(
                    f"[cyan]{server_name} 생성 중...",
                    total=None
                )
                
                generator.generate_server_structure(server_name, categories)
                progress.remove_task(task)
        
        # 4. 결과 트리 출력
        console.print("\n[bold]4️⃣  생성 결과[/bold]")
        _print_result_tree(Path(output_dir), all_categories)
        
        # 완료 메시지
        console.print(Panel.fit(
            f"[bold green]✅ 생성 완료![/bold green]\n\n"
            f"📂 위치: [cyan]{Path(output_dir).absolute()}[/cyan]\n"
            f"📊 통계:\n"
            f"   - 서버: {len(all_categories)}개\n"
            f"   - 총 카테고리: {sum(len(cats) for cats in all_categories.values())}개\n"
            f"   - 총 도구: {total_tools}개",
            border_style="green"
        ))
        
    except Exception as e:
        console.print(f"\n[bold red]❌ 오류 발생:[/bold red] {e}")
        raise


def _print_result_tree(output_dir: Path, all_categories: dict):
    """생성된 파일 구조를 트리로 출력"""
    tree = Tree(f"[bold cyan]📁 {output_dir.name}/[/bold cyan]")
    
    for server_name, categories in all_categories.items():
        server_branch = tree.add(f"[bold yellow]📂 {server_name}/[/bold yellow]")
        
        for category_name, category_info in list(categories.items())[:3]:
            category_branch = server_branch.add(
                f"[green]📂 {category_name}/[/green] "
                f"[dim]({len(category_info.tools)} tools)[/dim]"
            )
            
            for tool in category_info.tools[:2]:
                category_branch.add(f"[blue]📄 {tool.get_simple_name()}.ts[/blue]")
            
            if len(category_info.tools) > 2:
                category_branch.add(f"[dim]... {len(category_info.tools) - 2}개 더[/dim]")
        
        if len(categories) > 3:
            server_branch.add(f"[dim]... {len(categories) - 3}개 카테고리 더[/dim]")
    
    console.print(tree)


@cli.command()
@click.option('--output', default='output/servers', help='출력 디렉토리')
def list_servers(output):
    """생성된 서버 목록 확인"""
    output_path = Path(output)
    
    if not output_path.exists():
        console.print(f"[red]❌ 디렉토리를 찾을 수 없습니다: {output}[/red]")
        return
    
    console.print(Panel.fit(
        "[bold cyan]생성된 MCP 서버 목록[/bold cyan]",
        border_style="cyan"
    ))
    
    servers = [d for d in output_path.iterdir() if d.is_dir()]
    
    if not servers:
        console.print("[yellow]⚠️  생성된 서버가 없습니다.[/yellow]")
        return
    
    for server_dir in servers:
        metadata_file = server_dir / "metadata.json"
        if metadata_file.exists():
            import json
            metadata = json.loads(metadata_file.read_text())
            
            console.print(f"\n[bold yellow]{server_dir.name}[/bold yellow]")
            console.print(f"  카테고리: {metadata['total_categories']}개")
            console.print(f"  도구: {metadata['total_tools']}개")
            console.print(f"  생성일: {metadata['generated_at']}")


@cli.command()
@click.argument('server_name')
@click.option('--output', default='output/servers', help='출력 디렉토리')
def show(server_name, output):
    """특정 서버의 상세 정보 표시"""
    server_path = Path(output) / server_name
    metadata_file = server_path / "metadata.json"
    
    if not metadata_file.exists():
        console.print(f"[red]❌ 서버를 찾을 수 없습니다: {server_name}[/red]")
        return
    
    import json
    metadata = json.loads(metadata_file.read_text())
    
    console.print(Panel.fit(
        f"[bold cyan]{server_name}[/bold cyan]",
        border_style="cyan"
    ))
    
    console.print(f"\n[bold]통계[/bold]")
    console.print(f"  카테고리: {metadata['total_categories']}개")
    console.print(f"  도구: {metadata['total_tools']}개")
    
    console.print(f"\n[bold]카테고리[/bold]")
    for cat_name, cat_info in metadata['categories'].items():
        console.print(f"\n  [yellow]{cat_name}[/yellow]")
        console.print(f"    설명: {cat_info['description']}")
        console.print(f"    도구: {cat_info['tool_count']}개")
        console.print(f"    키워드: {', '.join(cat_info['keywords'])}")


if __name__ == "__main__":
    cli()
