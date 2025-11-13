"""전체 워크플로우 통합"""
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from src.agent.mcp_agent import MCPAgent
from src.agent.code_generator import CodeGenerator
from src.agent.code_executor import CodeExecutor


console = Console()


class CodeExecutionWorkflow:
    """
    MCP 기반 코드 실행 워크플로우

    Usage:
        workflow = CodeExecutionWorkflow()
        result = workflow.run("Create a Salesforce account named 'ACME Corp'")
    """

    def __init__(self, output_dir: str = "output/servers", api_key: Optional[str] = None):
        """
        Args:
            output_dir: 생성된 MCP 구조 디렉토리
            api_key: Anthropic API 키
        """
        self.output_dir = output_dir
        self.api_key = api_key

        # Agent 초기화
        self.mcp_agent = MCPAgent(output_dir)
        self.code_generator = CodeGenerator(self.mcp_agent, api_key)
        self.code_executor = CodeExecutor(self.mcp_agent)

    def run(self, user_query: str, execute: bool = True, verbose: bool = True) -> Dict[str, Any]:
        """
        전체 워크플로우 실행

        Args:
            user_query: 사용자 질문
            execute: 코드 실행 여부
            verbose: 상세 출력 여부

        Returns:
            결과 딕셔너리
        """
        result = {
            "query": user_query,
            "generated_code": None,
            "execution_result": None,
            "success": False
        }

        try:
            # 1. 코드 생성
            if verbose:
                console.print("\n[bold cyan]1️⃣  Generating code...[/bold cyan]")

            generated = self.code_generator.generate_code(user_query)
            result["generated_code"] = {
                "code": generated.code,
                "description": generated.description,
                "explanation": generated.explanation,
                "required_tools": generated.required_tools
            }

            if verbose:
                console.print(Panel(
                    Syntax(generated.code, "python", theme="monokai", line_numbers=True),
                    title="[bold green]Generated Code[/bold green]",
                    border_style="green"
                ))
                console.print(f"\n[dim]Description: {generated.description}[/dim]")
                console.print(f"[dim]Tools: {generated.required_tools}[/dim]")

            # 2. 코드 실행
            if execute:
                if verbose:
                    console.print("\n[bold cyan]2️⃣  Executing code...[/bold cyan]")

                exec_result = self.code_executor.execute(generated.code)
                result["execution_result"] = exec_result

                if exec_result["success"]:
                    result["success"] = True
                    if verbose:
                        console.print(Panel(
                            exec_result["output"] or "[dim]No output[/dim]",
                            title="[bold green]Execution Output[/bold green]",
                            border_style="green"
                        ))
                        if exec_result.get("return_value"):
                            console.print(f"\n[green]✓[/green] Return value: {exec_result['return_value']}")
                else:
                    if verbose:
                        console.print(Panel(
                            f"[red]{exec_result['error']}[/red]\n\n{exec_result.get('traceback', '')}",
                            title="[bold red]Execution Error[/bold red]",
                            border_style="red"
                        ))
            else:
                result["success"] = True

        except Exception as e:
            result["error"] = str(e)
            if verbose:
                console.print(f"\n[bold red]Error:[/bold red] {e}")

        return result

    def interactive_mode(self):
        """대화형 모드"""
        console.print(Panel.fit(
            "[bold cyan]Code Execution Workflow - Interactive Mode[/bold cyan]\n"
            "Type 'exit' or 'quit' to exit\n"
            "Type 'help' for commands",
            border_style="cyan"
        ))

        while True:
            try:
                query = console.input("\n[bold yellow]Query>[/bold yellow] ").strip()

                if not query:
                    continue

                if query.lower() in ['exit', 'quit', 'q']:
                    console.print("\n[dim]Goodbye![/dim]")
                    break

                if query.lower() == 'help':
                    self._show_help()
                    continue

                if query.startswith('!'):
                    self._handle_command(query[1:])
                    continue

                # 일반 질문 처리
                self.run(query, execute=True, verbose=True)

            except KeyboardInterrupt:
                console.print("\n\n[dim]Use 'exit' to quit[/dim]")
            except Exception as e:
                console.print(f"\n[red]Error: {e}[/red]")

    def _show_help(self):
        """도움말 표시"""
        help_text = """
[bold]Commands:[/bold]
  help                 - Show this help
  exit, quit, q        - Exit interactive mode
  !servers             - List available servers
  !search <keyword>    - Search tools by keyword
  !tree [server]       - Show directory tree

[bold]Examples:[/bold]
  Create a Salesforce account named 'ACME Corp'
  Search for all documents in Google Drive
  Update spreadsheet cell A1 with value 'Hello'
"""
        console.print(Panel(help_text, title="Help", border_style="blue"))

    def _handle_command(self, command: str):
        """명령어 처리"""
        parts = command.split()
        cmd = parts[0].lower()

        if cmd == 'servers':
            servers = self.mcp_agent.list_servers()
            console.print(f"\n[bold]Available Servers:[/bold] {', '.join(servers)}")

        elif cmd == 'search' and len(parts) > 1:
            keyword = parts[1]
            tools = self.mcp_agent.search_tools(keyword)
            console.print(f"\n[bold]Search results for '{keyword}':[/bold]")
            for tool in tools[:10]:
                console.print(f"  • {tool.server}/{tool.category}/{tool.name}")
                console.print(f"    {tool.description}")

        elif cmd == 'tree':
            server = parts[1] if len(parts) > 1 else None
            console.print("\n" + self.mcp_agent.get_tree(server))

        else:
            console.print(f"[red]Unknown command: {cmd}[/red]")


if __name__ == "__main__":
    import sys

    # API 키 확인
    import os
    if not os.getenv('ANTHROPIC_API_KEY'):
        console.print("[red]Error: ANTHROPIC_API_KEY not set[/red]")
        sys.exit(1)

    workflow = CodeExecutionWorkflow()
    workflow.interactive_mode()
