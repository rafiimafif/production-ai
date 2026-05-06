"""Quick validation for Phase 5 MCP modules."""

import asyncio

from backend.mcp.handlers import (
    handle_health_check,
    handle_query_database,
)
from backend.mcp.server import mcp_server

# Test 1: handlers module
res_health = handle_health_check()
assert res_health == "ok"

# SELECT guard check
try:
    handle_query_database("DROP TABLE users")
    assert False, "Should have blocked destructive query"
except ValueError as e:
    assert "SELECT only" in str(e)

res_sql = handle_query_database("SELECT 1")
assert res_sql == "Query simulated: SELECT 1"

print("handlers.py — ALL CHECKS PASSED")

# Test 2: server imports and tools are registered
assert mcp_server.name == "production-ai"

# Verify all 4 tools are registered
async def check_tools():
    # mcp_server.list_tools() is async
    tools = await mcp_server.list_tools()
    tool_names = [t.name for t in tools]
    assert "search_documents" in tool_names
    assert "query_database" in tool_names
    assert "list_models" in tool_names
    assert "health_check" in tool_names
    print("server.py   — ALL CHECKS PASSED")

if __name__ == "__main__":
    asyncio.run(check_tools())
