"""
MCP tool handlers — business logic for each MCP-exposed tool.

These functions are pure logic, separated from the MCP server wiring
so they can be tested independently and reused by the agent nodes.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Knowledge base search
# ---------------------------------------------------------------------------
def handle_search_documents(query: str, collection: str = "default") -> str:
    """
    Search the RAG knowledge base and return a formatted answer.

    Args:
        query:      Natural-language question.
        collection: ChromaDB collection name.

    Returns:
        A formatted string with the answer and source excerpts.
    """
    from backend.rag.retriever import query as rag_query

    logger.info("MCP handler: search_documents  q='%s'  col='%s'", query[:60], collection)

    try:
        result = rag_query(query, collection)
        answer = result.get("answer", "No answer found.")
        sources = result.get("sources", [])

        lines = [f"Answer: {answer}", "", "Sources:"]
        for i, src in enumerate(sources, 1):
            score = src.get("score")
            score_str = f" (score: {score})" if score is not None else ""
            lines.append(f"  [{i}]{score_str} {src.get('text', '')[:150]}")

        return "\n".join(lines)
    except Exception as exc:
        logger.error("search_documents failed: %s", exc)
        return f"Error searching knowledge base: {exc}"


# ---------------------------------------------------------------------------
# Database query
# ---------------------------------------------------------------------------
def handle_query_database(sql: str) -> str:
    """
    Execute a read-only SQL query against the DuckDB analytics database.

    Args:
        sql: A SELECT statement (write operations are blocked).

    Returns:
        Query results as a formatted table string.
    """
    import duckdb

    from backend.config import settings

    logger.info("MCP handler: query_database  sql='%s'", sql[:80])

    # Basic safety check — only allow SELECT
    stripped = sql.strip().upper()
    if not stripped.startswith("SELECT"):
        return "Error: Only SELECT queries are allowed for safety."

    try:
        conn = duckdb.connect(settings.duckdb_path, read_only=True)
        result = conn.execute(sql).fetchdf()
        conn.close()
        return result.to_string() if not result.empty else "Query returned no results."
    except Exception as exc:
        logger.error("query_database failed: %s", exc)
        return f"Error executing query: {exc}"


# ---------------------------------------------------------------------------
# List available models
# ---------------------------------------------------------------------------
def handle_list_models() -> str:
    """
    List all models currently available on the local Ollama instance.

    Returns:
        Formatted list of model names, or an error message.
    """
    from backend.llm.provider import list_models

    logger.info("MCP handler: list_models")

    try:
        models = list_models()
        if not models:
            return "No models found. Pull models with: ollama pull <model>"

        lines = ["Available Ollama models:", ""]
        for m in models:
            name = m.get("name", "unknown")
            size = m.get("size", 0)
            size_gb = size / (1024**3) if size else 0
            lines.append(f"  • {name}  ({size_gb:.1f} GB)")

        return "\n".join(lines)
    except Exception as exc:
        logger.error("list_models failed: %s", exc)
        return f"Error listing models: {exc}"


# ---------------------------------------------------------------------------
# System health check
# ---------------------------------------------------------------------------
def handle_health_check() -> str:
    """
    Check the health of all system components.

    Returns:
        A formatted health report.
    """
    from backend.llm.provider import health_check as ollama_health
    from backend.rag.vectorstore import get_chroma_client

    logger.info("MCP handler: health_check")

    checks: dict[str, Any] = {}

    # Ollama
    checks["ollama"] = ollama_health()

    # ChromaDB
    try:
        client = get_chroma_client()
        client.heartbeat()
        checks["chromadb"] = True
    except Exception:
        checks["chromadb"] = False

    # Format report
    lines = ["System Health Report:", ""]
    for component, status in checks.items():
        icon = "✓" if status else "✗"
        lines.append(f"  {icon} {component}: {'healthy' if status else 'unreachable'}")

    all_ok = all(checks.values())
    lines.append("")
    lines.append(f"Overall: {'ALL SYSTEMS GO' if all_ok else 'DEGRADED'}")

    return "\n".join(lines)
