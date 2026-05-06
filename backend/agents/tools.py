"""
Agent tools — callable functions that LangGraph nodes can invoke.

Each tool is a plain Python function. They are referenced by the tool_node
in the graph and can also be exposed via MCP in Phase 5.
"""

from __future__ import annotations

import logging
from typing import Any

from backend.rag.retriever import query as rag_query

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# RAG search tool
# ---------------------------------------------------------------------------
def search_knowledge_base(
    question: str,
    collection: str = "default",
    top_k: int = 5,
) -> dict[str, Any]:
    """
    Search the RAG knowledge base for relevant documents.

    Args:
        question:   Natural-language query.
        collection: ChromaDB collection to search.
        top_k:      Number of chunks to retrieve.

    Returns:
        Dict with "answer" and "sources" keys.
    """
    logger.info("Tool: search_knowledge_base  q='%s'", question[:80])
    return rag_query(question, collection, top_k)


# ---------------------------------------------------------------------------
# Database query tool (placeholder — DuckDB integration in Phase 5)
# ---------------------------------------------------------------------------
def query_database(sql: str) -> str:
    """
    Execute a read-only SQL query against the analytics database.

    Args:
        sql: A SELECT statement to execute.

    Returns:
        Query results as a formatted string.
    """
    logger.info("Tool: query_database  sql='%s'", sql[:80])
    try:
        import duckdb

        from backend.config import settings

        conn = duckdb.connect(settings.duckdb_path, read_only=True)
        result = conn.execute(sql).fetchdf()
        conn.close()
        return result.to_string()
    except Exception as exc:
        logger.error("Database query failed: %s", exc)
        return f"Error executing query: {exc}"


# ---------------------------------------------------------------------------
# Tool registry — maps tool names to callables
# ---------------------------------------------------------------------------
TOOL_REGISTRY: dict[str, callable] = {
    "search_knowledge_base": search_knowledge_base,
    "query_database": query_database,
}


def get_tool(name: str) -> callable:
    """Look up a tool by name. Raises KeyError if not found."""
    if name not in TOOL_REGISTRY:
        available = ", ".join(TOOL_REGISTRY.keys())
        raise KeyError(f"Unknown tool '{name}'. Available: {available}")
    return TOOL_REGISTRY[name]
