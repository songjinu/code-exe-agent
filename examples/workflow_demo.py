"""워크플로우 데모 - 전체 시스템 테스트"""
import sys
import os
from pathlib import Path

# 프로젝트 루트 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from src.workflow import CodeExecutionWorkflow

console = Console()


def demo_basic():
    """기본 데모"""
    console.print("\n[bold cyan]===== Demo 1: Basic Usage =====[/bold cyan]\n")

    workflow = CodeExecutionWorkflow('output/servers')

    # 예제 질문
    queries = [
        "Create a new Salesforce account named 'Demo Corporation'",
        "Search for documents in Google Drive containing 'report'",
        "Update a Google spreadsheet cell A1 with value 'Hello World'",
    ]

    for i, query in enumerate(queries, 1):
        console.print(f"\n[bold yellow]Example {i}:[/bold yellow] {query}")
        console.print("[dim]" + "=" * 60 + "[/dim]")

        result = workflow.run(query, execute=True, verbose=True)

        if result["success"]:
            console.print("[green]✓ Success![/green]")
        else:
            console.print(f"[red]✗ Failed: {result.get('error')}[/red]")

        console.print("\n")


def demo_code_only():
    """코드만 생성 (실행하지 않음)"""
    console.print("\n[bold cyan]===== Demo 2: Code Generation Only =====[/bold cyan]\n")

    workflow = CodeExecutionWorkflow('output/servers')

    query = "Create 3 Salesforce accounts and then generate a report"
    console.print(f"[bold yellow]Query:[/bold yellow] {query}\n")

    result = workflow.run(query, execute=False, verbose=True)

    if result["generated_code"]:
        console.print("\n[green]✓ Code generated successfully![/green]")
        console.print(f"\n[dim]Description: {result['generated_code']['description']}[/dim]")


def demo_with_context():
    """컨텍스트를 포함한 코드 생성"""
    console.print("\n[bold cyan]===== Demo 3: Code Generation with Context =====[/bold cyan]\n")

    workflow = CodeExecutionWorkflow('output/servers')

    query = "Create a new account"
    context = """
    The account should have:
    - Name: Tech Solutions Inc
    - Industry: Technology
    - Annual Revenue: $5M
    - Number of Employees: 50
    """

    console.print(f"[bold yellow]Query:[/bold yellow] {query}")
    console.print(f"[bold yellow]Context:[/bold yellow] {context}\n")

    result = workflow.code_generator.generate_code(query, context=context)

    console.print("[green]✓ Generated code:[/green]")
    console.print(result.code)
    console.print(f"\n[dim]Explanation: {result.explanation}[/dim]")


def demo_error_handling():
    """에러 핸들링 테스트"""
    console.print("\n[bold cyan]===== Demo 4: Error Handling =====[/bold cyan]\n")

    workflow = CodeExecutionWorkflow('output/servers')

    # 존재하지 않는 도구 사용
    query = "Use a non-existent tool to do something impossible"

    console.print(f"[bold yellow]Query:[/bold yellow] {query}\n")

    result = workflow.run(query, execute=True, verbose=True)

    if not result["success"]:
        console.print("\n[yellow]⚠ Error was handled gracefully[/yellow]")


def main():
    """메인 데모 실행"""
    console.print("""
[bold cyan]╔═══════════════════════════════════════════════════════════════╗
║  Code Execution Workflow - Complete Demo                     ║
║  MCP Tools → AI Code Generation → Safe Execution             ║
╚═══════════════════════════════════════════════════════════════╝[/bold cyan]
""")

    # API 키 확인
    if not os.getenv('ANTHROPIC_API_KEY'):
        console.print("[red]Error: ANTHROPIC_API_KEY가 설정되지 않았습니다[/red]")
        console.print("[yellow]데모를 실행하려면 .env 파일에 API 키를 설정하세요[/yellow]")
        return

    # MCP 구조 확인
    if not Path('output/servers').exists():
        console.print("[red]Error: MCP 구조를 찾을 수 없습니다[/red]")
        console.print("[yellow]먼저 'python main.py generate'를 실행하세요[/yellow]")
        return

    try:
        # 데모 실행
        demo_basic()

        input("\n[dim]Press Enter to continue to next demo...[/dim]")
        demo_code_only()

        input("\n[dim]Press Enter to continue to next demo...[/dim]")
        demo_with_context()

        input("\n[dim]Press Enter to continue to next demo...[/dim]")
        demo_error_handling()

        console.print("\n[bold green]✓ All demos completed![/bold green]")

    except KeyboardInterrupt:
        console.print("\n\n[dim]Demo interrupted[/dim]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
