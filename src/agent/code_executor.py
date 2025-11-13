"""안전한 코드 실행 환경"""
import sys
import io
import traceback
from typing import Dict, Any, Optional
from contextlib import redirect_stdout, redirect_stderr


class CodeExecutor:
    """
    생성된 코드를 안전하게 실행하는 Sandbox

    Usage:
        executor = CodeExecutor(mcp_agent)
        result = executor.execute(generated_code)
        print(result['output'])
    """

    def __init__(self, mcp_agent):
        """
        Args:
            mcp_agent: MCPAgent 인스턴스 (코드 실행 시 제공)
        """
        self.mcp_agent = mcp_agent

    def execute(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """
        코드 실행

        Args:
            code: 실행할 Python 코드
            timeout: 타임아웃 (초)

        Returns:
            실행 결과 딕셔너리
        """
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        result = {
            "success": False,
            "output": "",
            "error": None,
            "return_value": None
        }

        try:
            # 실행 환경 구성
            exec_globals = {
                "__builtins__": __builtins__,
                "agent": self.mcp_agent,
                "print": print,  # print는 capture됨
            }

            exec_locals = {}

            # stdout/stderr 캡처
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                # 코드 실행
                exec(code, exec_globals, exec_locals)

                # return_value 추출 (있으면)
                if 'result' in exec_locals:
                    result['return_value'] = exec_locals['result']

            result['success'] = True
            result['output'] = stdout_capture.getvalue()

            # stderr에 출력이 있으면 warning으로 추가
            stderr_output = stderr_capture.getvalue()
            if stderr_output:
                result['warnings'] = stderr_output

        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            result['traceback'] = traceback.format_exc()
            result['output'] = stdout_capture.getvalue()

        return result

    def execute_safe(self, code: str) -> Dict[str, Any]:
        """
        더 안전한 실행 (제한된 builtins)

        Args:
            code: 실행할 Python 코드

        Returns:
            실행 결과
        """
        # 안전한 builtins만 허용
        safe_builtins = {
            'print': print,
            'len': len,
            'range': range,
            'enumerate': enumerate,
            'zip': zip,
            'map': map,
            'filter': filter,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'set': set,
            'True': True,
            'False': False,
            'None': None,
        }

        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        result = {
            "success": False,
            "output": "",
            "error": None,
            "return_value": None
        }

        try:
            exec_globals = {
                "__builtins__": safe_builtins,
                "agent": self.mcp_agent,
            }

            exec_locals = {}

            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, exec_globals, exec_locals)

                if 'result' in exec_locals:
                    result['return_value'] = exec_locals['result']

            result['success'] = True
            result['output'] = stdout_capture.getvalue()

        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            result['traceback'] = traceback.format_exc()
            result['output'] = stdout_capture.getvalue()

        return result


# Sandbox with subprocess (더 강력한 격리)
class SubprocessExecutor:
    """
    별도 프로세스에서 코드 실행 (더 안전)

    TODO: 향후 구현
    - Docker 컨테이너 실행
    - Resource limits (CPU, Memory)
    - Network isolation
    """

    def __init__(self, mcp_agent):
        self.mcp_agent = mcp_agent

    def execute(self, code: str, timeout: int = 30):
        """별도 프로세스에서 실행"""
        raise NotImplementedError("SubprocessExecutor는 아직 구현되지 않았습니다")
