"""Claude를 사용한 동적 코드 생성"""
import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from anthropic import Anthropic


@dataclass
class GeneratedCode:
    """생성된 코드 정보"""
    code: str
    language: str
    description: str
    required_tools: List[Dict[str, str]]
    explanation: str


class CodeGenerator:
    """
    사용자 질문을 받아 MCP 도구를 사용하는 코드를 자동 생성

    Usage:
        generator = CodeGenerator(mcp_agent)
        result = generator.generate_code(
            "Create a new Salesforce account named 'ACME Corp'"
        )
        print(result.code)
    """

    def __init__(self, mcp_agent, api_key: Optional[str] = None):
        """
        Args:
            mcp_agent: MCPAgent 인스턴스
            api_key: Anthropic API 키
        """
        self.mcp_agent = mcp_agent
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')

        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다")

        self.client = Anthropic(api_key=self.api_key)

    def generate_code(self, user_query: str, context: Optional[str] = None) -> GeneratedCode:
        """
        사용자 질문을 기반으로 실행 가능한 코드 생성

        Args:
            user_query: 사용자 질문
            context: 추가 컨텍스트

        Returns:
            GeneratedCode: 생성된 코드와 메타데이터
        """
        # 1. 관련 도구 검색
        relevant_tools = self._search_relevant_tools(user_query)

        # 2. 프롬프트 구성
        prompt = self._build_prompt(user_query, relevant_tools, context)

        # 3. Claude API 호출
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # 4. 응답 파싱
        result = self._parse_response(response.content[0].text)

        return result

    def _search_relevant_tools(self, query: str) -> List[Dict[str, Any]]:
        """질문과 관련된 도구 검색"""
        keywords = query.lower().split()

        relevant = []
        for keyword in keywords:
            tools = self.mcp_agent.search_tools(keyword)
            for tool in tools[:3]:
                tool_info = {
                    "server": tool.server,
                    "category": tool.category,
                    "tool": tool.name,
                    "description": tool.description,
                    "keywords": tool.keywords
                }
                if tool_info not in relevant:
                    relevant.append(tool_info)

        return relevant[:10]

    def _build_prompt(self, user_query: str, relevant_tools: List[Dict], context: Optional[str]) -> str:
        """Claude용 프롬프트 생성"""
        tools_description = self._format_tools_for_prompt(relevant_tools)

        prompt = f"""You are a code generation assistant that creates executable code using MCP tools.

User Request: {user_query}

Available MCP Tools:
{tools_description}

Available Servers Structure:
{self._get_servers_structure()}

Task: Generate Python code that accomplishes the user's request using the appropriate MCP tools.

Requirements:
1. Use the MCPAgent API to execute tools: agent.execute(server, category, tool, params)
2. Include proper error handling
3. Return results in a structured format
4. Add helpful comments
5. Keep code simple and focused

Response Format (JSON):
{{
    "code": "# Python code here\\n...",
    "language": "python",
    "description": "Brief description of what the code does",
    "required_tools": [
        {{"server": "...", "category": "...", "tool": "..."}}
    ],
    "explanation": "Step-by-step explanation"
}}

Generate the code now:"""

        if context:
            prompt += f"\n\nAdditional Context: {context}"

        return prompt

    def _format_tools_for_prompt(self, tools: List[Dict]) -> str:
        """도구 목록을 프롬프트용 텍스트로 포맷팅"""
        if not tools:
            return "No specific tools found. You can explore available tools using the agent."

        formatted = []
        for i, tool in enumerate(tools, 1):
            formatted.append(
                f"{i}. {tool['server']}/{tool['category']}/{tool['tool']}\n"
                f"   Description: {tool['description']}\n"
                f"   Keywords: {', '.join(tool.get('keywords', []))}"
            )

        return "\n\n".join(formatted)

    def _get_servers_structure(self) -> str:
        """사용 가능한 서버 구조 요약"""
        servers = self.mcp_agent.list_servers()
        structure = []

        for server in servers[:5]:
            categories = self.mcp_agent.list_categories(server)
            cat_summary = ", ".join([f"{c.name} ({c.tool_count} tools)"
                                     for c in categories[:3]])
            structure.append(f"- {server}: {cat_summary}")

        return "\n".join(structure)

    def _parse_response(self, response_text: str) -> GeneratedCode:
        """Claude 응답 파싱"""
        try:
            # JSON 블록 추출
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "{" in response_text:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                json_text = response_text[json_start:json_end]
            else:
                raise ValueError("No JSON found in response")

            data = json.loads(json_text)

            return GeneratedCode(
                code=data.get("code", ""),
                language=data.get("language", "python"),
                description=data.get("description", ""),
                required_tools=data.get("required_tools", []),
                explanation=data.get("explanation", "")
            )

        except Exception as e:
            return GeneratedCode(
                code=response_text,
                language="python",
                description="Generated code (parsing failed)",
                required_tools=[],
                explanation=f"Error parsing response: {e}"
            )
