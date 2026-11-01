"""End-to-end stdio MCP test: advertised schema, real call, source fingerprint.

Unlike direct-function unit tests, this checks the tool schema shown to a freshly
connected client. It does not prove Codex/Claude's separately configured runtime
has refreshed its older tool definitions.
"""
import asyncio
import hashlib
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT = Path(__file__).resolve().parent
STANDARD = "guidelines/REFACTORING_OPTIMIZATION_STANDARD.md"


def decoded(result):
    assert not result.isError, result
    structured = getattr(result, "structuredContent", None)
    if isinstance(structured, dict):
        return structured.get("result", structured)
    for item in result.content:
        text = getattr(item, "text", None)
        if isinstance(text, str):
            parsed = json.loads(text)
            return parsed.get("result", parsed) if isinstance(parsed, dict) else parsed
    raise AssertionError("No readable response content")


async def verify():
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(ROOT / "guidelines_mcp.py")],
        cwd=str(ROOT),
    )
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            tools = {tool.name: tool for tool in (await session.list_tools()).tools}
            assert "check_setup" in tools
            assert "read_guideline" in tools
            assert "get_guidelines_for_task" in tools
            schema = json.dumps(
                tools["get_guidelines_for_task"].input_schema, sort_keys=True
            )
            for task in ("refactoring", "optimization"):
                assert task in schema, f"task not advertised in live MCP schema: {task}"

            status = decoded(await session.call_tool("check_setup", {}))
            assert status["ready"], status["missing_expected_files"]
            assert set(("refactoring", "optimization")) <= set(
                status["available_task_types"]
            )
            identity = status["specialist_standard"]
            assert identity["available"]
            original_bytes = (ROOT / STANDARD).read_bytes()
            assert identity["sha256"] == hashlib.sha256(original_bytes).hexdigest()

            for task in ("refactoring", "optimization"):
                response = decoded(
                    await session.call_tool("get_guidelines_for_task", {"task_type": task})
                )
                assert not response["missing"]
                assert not response["truncated"]
                doc = next(d for d in response["documents"] if d["path"] == STANDARD)
                assert not doc["truncated"]
                assert doc["content"] == original_bytes.decode("utf-8")

            fallback = decoded(
                await session.call_tool("read_guideline", {"relative_path": STANDARD})
            )
            assert not fallback["truncated"]
            assert fallback["content"].encode("utf-8") == original_bytes

    print("MCP_STDIO_SCHEMA_AND_SPECIALIST_READ_PASS")


if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(verify(), timeout=60))
