"""
Agent nodes — individual processing steps within the LangGraph workflow.

Each function receives the current AgentState and returns a partial state
update. LangGraph merges the returned dict into the running state.

Node responsibilities:
  • router_node  — classify intent → decide next step
  • rag_node     — retrieve context from the knowledge base
  • tool_node    — execute a registered tool
  • llm_node     — generate the final response using Ollama
"""

from __future__ import annotations

import logging

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from backend.agents.tools import search_knowledge_base
from backend.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Shared LLM instance for all nodes
# ---------------------------------------------------------------------------
_llm: ChatOllama | None = None


def _get_llm() -> ChatOllama:
    """Lazy-init the ChatOllama instance."""
    global _llm
    if _llm is None:
        _llm = ChatOllama(
            model=settings.default_model,
            base_url=settings.ollama_host,
        )
    return _llm


# ---------------------------------------------------------------------------
# Intent keywords for the router
# ---------------------------------------------------------------------------
_RAG_KEYWORDS = frozenset([
    "search", "find", "document", "knowledge", "lookup",
    "what does", "tell me about", "explain",
])
_TOOL_KEYWORDS = frozenset([
    "calculate", "run", "execute", "tool", "query", "sql", "database",
])


# ---------------------------------------------------------------------------
# Router node
# ---------------------------------------------------------------------------
def router_node(state: dict) -> dict:
    """
    Analyse the last user message and decide which path to take.

    Returns:
        {"next_action": "rag" | "tools" | "llm"}
    """
    messages = state.get("messages", [])
    if not messages:
        return {"next_action": "llm"}

    last_content = messages[-1].content.lower() if hasattr(messages[-1], "content") else ""

    if any(kw in last_content for kw in _RAG_KEYWORDS):
        logger.info("Router → RAG")
        return {"next_action": "rag"}

    if any(kw in last_content for kw in _TOOL_KEYWORDS):
        logger.info("Router → Tools")
        return {"next_action": "tools"}

    logger.info("Router → LLM (direct)")
    return {"next_action": "llm"}


# ---------------------------------------------------------------------------
# RAG node
# ---------------------------------------------------------------------------
def rag_node(state: dict) -> dict:
    """
    Retrieve context from the knowledge base using the last user message.

    Returns:
        {"context": <retrieved answer text>}
    """
    messages = state.get("messages", [])
    question = messages[-1].content if messages and hasattr(messages[-1], "content") else ""

    try:
        result = search_knowledge_base(question)
        context = result.get("answer", "No relevant documents found.")
        logger.info("RAG node returned %d sources", len(result.get("sources", [])))
    except Exception as exc:
        logger.warning("RAG retrieval failed: %s", exc)
        context = "Knowledge base is unavailable. Answering from general knowledge."

    return {"context": context}


# ---------------------------------------------------------------------------
# Tool node
# ---------------------------------------------------------------------------
def tool_node(state: dict) -> dict:
    """
    Execute a tool based on the user's request.

    For now this delegates to the RAG search tool. In Phase 5, MCP tools
    will be integrated here for richer tool dispatch.

    Returns:
        {"context": <tool execution result>}
    """
    messages = state.get("messages", [])
    question = messages[-1].content if messages and hasattr(messages[-1], "content") else ""

    # Simple heuristic: if the message contains SQL-like content, try DB query
    if any(kw in question.lower() for kw in ["select", "from", "where"]):
        from backend.agents.tools import query_database

        result = query_database(question)
        return {"context": f"Database result:\n{result}"}

    # Default: search knowledge base
    try:
        result = search_knowledge_base(question)
        return {"context": result.get("answer", "No result from tool.")}
    except Exception as exc:
        logger.warning("Tool execution failed: %s", exc)
        return {"context": f"Tool execution failed: {exc}"}


# ---------------------------------------------------------------------------
# LLM node (final response generation)
# ---------------------------------------------------------------------------
def llm_node(state: dict) -> dict:
    """
    Generate the final response using the Ollama LLM.

    If context was provided by the RAG or tool node, it's injected as a
    system message so the LLM can ground its answer.

    Returns:
        {"messages": [AIMessage(...)]}
    """
    context = state.get("context", "")
    messages = list(state.get("messages", []))

    # Build the message list for the LLM
    llm_messages = []

    if context:
        llm_messages.append(SystemMessage(
            content=(
                "Use the following context to answer the user's question. "
                "If the context is not relevant, say so and answer from your "
                "general knowledge.\n\n"
                f"Context:\n{context}"
            )
        ))

    # Convert state messages to langchain message types
    for msg in messages:
        if isinstance(msg, (HumanMessage, AIMessage, SystemMessage)):
            llm_messages.append(msg)
        elif hasattr(msg, "content"):
            # Handle generic message objects
            role = getattr(msg, "type", "human")
            if role == "ai":
                llm_messages.append(AIMessage(content=msg.content))
            else:
                llm_messages.append(HumanMessage(content=msg.content))

    llm = _get_llm()
    response = llm.invoke(llm_messages)

    logger.info("LLM node generated response (%d chars)", len(response.content))
    return {"messages": [response]}
