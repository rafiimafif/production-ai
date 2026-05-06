"""
MCP server — exposes tools via the Model Context Protocol.

This module creates a FastMCP server instance and registers all tools.
The server can be run standalone (for external agents like Claude Code / Aider)
or its tools can be called programmatically from the LangGraph agent.

Usage (standalone):
    uv run python -m backend.mcp.server

Usage (programmatic):
    from backend.mcp.server import mcp_server
    result = await mcp_server.call_tool("search_documents", {"query": "..."})
"""

from __future__ import annotations

import logging

from mcp.server.fastmcp import FastMCP

from backend.mcp.handlers import (
    handle_health_check,
    handle_list_models,
    handle_query_database,
    handle_search_documents,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Server instance
# ---------------------------------------------------------------------------
mcp_server = FastMCP(
    name="production-ai",
    instructions=(
        "Production AI MCP server. Provides tools for searching a RAG knowledge "
        "base, querying an analytics database, listing available LLM models, and "
        "checking system health."
    ),
)


# ---------------------------------------------------------------------------
# Tool registrations
# ---------------------------------------------------------------------------
@mcp_server.tool()
def search_documents(query: str, collection: str = "default") -> str:
    """Search the RAG knowledge base for documents relevant to the query.

    Args:
        query: Natural-language question to search for.
        collection: ChromaDB collection to search (default: "default").

    Returns:
        Formatted answer with source excerpts.
    """
    return handle_search_documents(query, collection)


@mcp_server.tool()
def query_database(sql: str) -> str:
    """Execute a read-only SQL query against the analytics database.

    Only SELECT statements are allowed. The database uses DuckDB.

    Args:
        sql: A valid SELECT query.

    Returns:
        Query results as a formatted table.
    """
    return handle_query_database(sql)


@mcp_server.tool()
def list_models() -> str:
    """List all LLM models currently available on the local Ollama instance.

    Returns:
        Formatted list of model names and sizes.
    """
    return handle_list_models()


@mcp_server.tool()
def health_check() -> str:
    """Check the health status of all system components.

    Returns:
        A health report for Ollama, ChromaDB, and other services.
    """
    return handle_health_check()


# ---------------------------------------------------------------------------
# Standalone entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting MCP server (stdio transport)...")
    mcp_server.run()
