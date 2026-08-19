#!/usr/bin/env python3
"""
MontExam Local Server — 浏览器答题 + 本地 Python 执行

零依赖（纯标准库），可选 websockets 获得实时推送。

用法:
    python montest-serve.py [--port 8234] [--dir ./montest-submissions] [--html path.html]
    python montest-serve.py  # 自动查找同目录下的 HTML 文件

启动后浏览器访问 http://localhost:8234
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from datetime import datetime

# ===== 配置 =====
DEFAULT_PORT = 8234
SUBMISSIONS_DIR = "montest-submissions"
HAS_WEBSOCKETS = False

try:
    import websockets
    import asyncio
    HAS_WEBSOCKETS = True
except ImportError:
    pass


# ===== 代码执行引擎 =====
class CodeRunner:
    """在本地 Python 解释器中执行代码，返回结构化结果"""

    def __init__(self, python_exec=None, submissions_dir=SUBMISSIONS_DIR):
        self.python = python_exec or sys.executable
        self.submissions_dir = Path(submissions_dir)
        self.submissions_dir.mkdir(parents=True, exist_ok=True)

    def run(self, code, test_cases=None, question_id=0):
        """
        执行用户代码 + 测试用例。

        Args:
            code: 用户编写的 Python 代码
            test_cases: [{"c": "func(1)", "e": 2}, ...] 测试用例列表
            question_id: 题目编号

        Returns:
            {"passed": int, "total": int, "results": [...], "error": str|None}
        """
        # 保存 .py 文件供 PyCharm 调试
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"q{question_id}_{ts}.py"
        filepath = self.submissions_dir / filename

        script_code = code
        if test_cases:
            full_code = self._build_test_script(code, test_cases)
            filepath.write_text(full_code, encoding="utf-8")
            script_code = full_code
        else:
            filepath.write_text(code, encoding="utf-8")

        # 用 subprocess 执行（必须执行含测试代码的完整脚本）
        result = self._execute(script_code, test_cases)

        return {
            **result,
            "file": str(filepath.resolve()),
            "filename": filename,
        }

    def _build_test_script(self, code, test_cases):
        """将用户代码和测试用例拼接成可执行脚本"""
        lines = [code, "", "# ===== MontExam 自动测试 ====="]

        for i, tc in enumerate(test_cases, 1):
            call = tc.get("c", "")
            expected = repr(tc.get("e", ""))
            lines.append("")
            lines.append("try:")
            lines.append(f"    _result = eval('{call}')")
            lines.append(f"    _expected = {expected}")
            lines.append("    _match = str(_result) == str(_expected)")
            # 注意：内层 f-string 的花括号需要 {{}} 转义
            lines.append("    print('TEST ' + ('PASS' if _match else 'FAIL') + ' | call=' + str(" + repr(call) + ") + ' | expected=' + str(_expected) + ' | got=' + str(_result))")
            lines.append("except Exception as _e:")
            lines.append("    print('TEST ERROR | call=' + str(" + repr(call) + ") + ' | error=' + str(_e))")

        return "\n".join(lines)

    def _execute(self, code, test_cases=None, timeout=10):
        """在子进程中执行代码"""
        try:
            proc = subprocess.run(
                [self.python, "-c", code],
                capture_output=True,
                text=True,
                timeout=timeout,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )

            stdout = proc.stdout.strip()
            stderr = proc.stderr.strip()

            if proc.returncode != 0 and not stdout:
                return {
                    "passed": 0,
                    "total": len(test_cases) if test_cases else 0,
                    "results": [],
                    "error": stderr or f"Exit code {proc.returncode}",
                    "output": stdout,
                }

            # 解析测试结果
            if test_cases:
                return self._parse_test_results(stdout, stderr, len(test_cases))

            return {
                "passed": 0,
                "total": 0,
                "results": [],
                "error": None,
                "output": stdout,
            }

        except subprocess.TimeoutExpired:
            return {
                "passed": 0,
                "total": len(test_cases) if test_cases else 0,
                "results": [],
                "error": f"执行超时（{timeout}秒限制）",
                "output": "",
            }
        except Exception as e:
            return {
                "passed": 0,
                "total": 0,
                "results": [],
                "error": str(e),
                "output": "",
            }

    def _parse_test_results(self, stdout, stderr, total):
        """解析 TEST PASS/FAIL 行"""
        results = []
        passed = 0

        for line in stdout.split("\n"):
            if line.startswith("TEST "):
                parts = line.split(" | ")
                status = parts[0].replace("TEST ", "")
                info = {}
                for p in parts[1:]:
                    if "=" in p:
                        k, v = p.split("=", 1)
                        info[k.strip()] = v.strip()

                is_pass = status == "PASS"
                if is_pass:
                    passed += 1

                results.append({
                    "pass": is_pass,
                    "call": info.get("call", ""),
                    "expected": info.get("expected", ""),
                    "actual": info.get("got", ""),
                    "error": info.get("error", "") if status == "ERROR" else None,
                })

        # 如果没有解析到 TEST 行，用普通输出模式
        if not results and stdout:
            return {
                "passed": -1,  # -1 表示无测试用例，只有输出
                "total": 0,
                "results": [],
                "error": None,
                "output": stdout,
            }

        return {
            "passed": passed,
            "total": total,
            "results": results,
            "error": stderr if stderr else None,
            "output": stdout,
        }


# ===== HTTP 请求处理 =====
class MontExamHandler(SimpleHTTPRequestHandler):
    """处理 HTTP 请求：静态文件 + API"""

    runner = None
    html_path = None
    # 长轮询结果缓存
    _pending_results = {}

    def log_message(self, format, *args):
        # 彩色日志
        msg = format % args
        if "200" in str(msg):
            sys.stdout.write(f"\033[32m  ✓ {msg}\033[0m\n")
        elif "404" in str(msg) or "500" in str(msg):
            sys.stdout.write(f"\033[31m  ✗ {msg}\033[0m\n")

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/" or parsed.path == "/index.html":
            self._serve_html()
        elif parsed.path == "/api/status":
            self._json_response({"status": "ok", "python": sys.executable})
        elif parsed.path.startswith("/api/result/"):
            request_id = parsed.path.split("/")[-1]
            result = self._pending_results.pop(request_id, None)
            if result:
                self._json_response(result)
            else:
                self._json_response({"pending": True}, status=202)
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/run":
            self._handle_run()
        else:
            self.send_error(404)

    def _serve_html(self):
        """提供 HTML 文件"""
        if self.html_path and Path(self.html_path).exists():
            html = Path(self.html_path).read_text(encoding="utf-8")
        else:
            # 尝试查找同目录下的 HTML
            candidates = list(Path(".").glob("*.html"))
            if candidates:
                html = candidates[0].read_text(encoding="utf-8")
            else:
                html = "<h1>MontExam</h1><p>未找到 HTML 文件，请用 --html 参数指定</p>"

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _handle_run(self):
        """处理代码执行请求"""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._json_response({"error": "Invalid JSON"}, status=400)
            return

        code = data.get("code", "")
        test_cases = data.get("testCases", [])
        question_id = data.get("questionId", 0)

        if not code.strip():
            self._json_response({"error": "代码不能为空"}, status=400)
            return

        result = self.runner.run(code, test_cases, question_id)
        self._json_response(result)

    def _json_response(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        """CORS preflight"""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


# ===== WebSocket 服务器（可选） =====
async def ws_handler(websocket, runner):
    """处理 WebSocket 连接"""
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                if data.get("type") == "run":
                    code = data.get("code", "")
                    test_cases = data.get("testCases", [])
                    question_id = data.get("questionId", 0)

                    result = runner.run(code, test_cases, question_id)
                    result["type"] = "result"
                    await websocket.send(json.dumps(result, ensure_ascii=False))
            except json.JSONDecodeError:
                await websocket.send(json.dumps({"error": "Invalid JSON"}))
    except Exception as e:
        print(f"  WebSocket error: {e}")


def start_ws_server(runner, port):
    """启动 WebSocket 服务器"""
    if not HAS_WEBSOCKETS:
        return None

    async def _start():
        server = await websockets.serve(
            lambda ws: ws_handler(ws, runner),
            "localhost",
            port + 1
        )
        await server.wait_closed()

    loop = asyncio.new_event_loop()
    thread = threading.Thread(target=lambda: loop.run_until_complete(_start()), daemon=True)
    thread.start()
    return thread


# ===== 主入口 =====
def main():
    parser = argparse.ArgumentParser(description="MontExam Local Server")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"HTTP 端口 (default: {DEFAULT_PORT})")
    parser.add_argument("--dir", default=SUBMISSIONS_DIR, help=f"提交保存目录 (default: {SUBMISSIONS_DIR})")
    parser.add_argument("--html", default=None, help="HTML 文件路径")
    parser.add_argument("--python", default=None, help="Python 解释器路径")
    args = parser.parse_args()

    runner = CodeRunner(python_exec=args.python, submissions_dir=args.dir)
    MontExamHandler.runner = runner
    MontExamHandler.html_path = args.html

    # 找 HTML 文件
    html_path = args.html
    if not html_path:
        candidates = list(Path(".").glob("*.html"))
        if candidates:
            html_path = str(candidates[0])

    # Banner
    print()
    print("  \033[1;35m MontExam \033[0m Local Server")
    print("  " + "─" * 40)
    print(f"  HTTP:    \033[36mhttp://localhost:{args.port}\033[0m")
    print(f"  Python:  {sys.executable} ({sys.version.split()[0]})")
    print(f"  模式:    本地 Python 执行")
    print(f"  提交目录: {Path(args.dir).resolve()}")
    if html_path:
        print(f"  HTML:    {html_path}")
    if HAS_WEBSOCKETS:
        print(f"  WebSocket: ws://localhost:{args.port + 1}")
    else:
        print(f"  WebSocket: \033[33m未安装 websockets 库，使用 HTTP 模式\033[0m")
        print(f"  (安装: pip install websockets)")
    print("  " + "─" * 40)
    print()

    # 启动 WebSocket（如果可用）
    if HAS_WEBSOCKETS:
        start_ws_server(runner, args.port)

    # 启动 HTTP 服务器
    server = HTTPServer(("localhost", args.port), MontExamHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  MontExam 服务器已停止")
        server.server_close()


if __name__ == "__main__":
    main()
