"""Quick validation for Phase 5 MCP modules."""

# Test 1: handlers import and basic logic
from backend.mcp.handlers import (
    handle_health_check,
    handle_list_models,
    handle_query_database,
    handle_search_documents,
)

# Test SELECT-only guard
result = handle_query_database("DROP TABLE users")
assert "Only SELECT" in result, f"Expected safety block, got: {result}"

result = handle_query_database("  delete FROM users")
assert "Only SELECT" in result, f"Expected safety block, got: {result}"

print("handlers.py — SAFETY CHECKS PASSED")

# Test health check (Ollama down is expected)
health = handle_health_check()
assert "System Health Report" in health
assert "chromadb" in health
print("handlers.py — HEALTH CHECK FORMAT PASSED")

# Test 2: server imports and tools are registered
from backend.mcp.server import mcp_server

assert mcp_server.name == "production-ai"

# Verify all 4 tools are registered
import asyncio

async def check_tools():
    tools = await mcp_server.list_tools()
    tool_names = [t.name for t in tools]
    assert "search_documents" in tool_names, f"Missing search_documents: {tool_names}"
    assert "query_database" in tool_names, f"Missing query_database: {tool_names}"
    assert "list_models" in tool_names, f"Missing list_models: {tool_names}"
    assert "health_check" in tool_names, f"Missing health_check: {tool_names}"
    print(f"server.py   — {len(tool_names)} TOOLS REGISTERED: {tool_names}")

asyncio.run(check_tools())

print("ALL PHASE 5 CHECKS PASSED")
