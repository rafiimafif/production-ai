"""
LangGraph agent workflow — the core state machine.

Flow:
    User message → Router → (RAG | Tools | Direct) → LLM → Response

The graph is compiled once at module level and reused for every request.
"""

from __future__ import annotations

import logging
from typing import Annotated

from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from backend.agents.nodes import llm_node, rag_node, router_node, tool_node

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# State schema
# ---------------------------------------------------------------------------
class AgentState(TypedDict):
    """
    The shared state that flows through every node in the graph.

    Fields:
        messages:    Conversation history (auto-appended via add_messages).
        next_action: Set by the router — "rag", "tools", or "llm".
        context:     Retrieved context injected by RAG or tool nodes.
    """

    messages: Annotated[list, add_messages]
    next_action: str
    context: str


# ---------------------------------------------------------------------------
# Routing logic
# ---------------------------------------------------------------------------
def _route_decision(state: AgentState) -> str:
    """Read the router's decision from state and return the next node name."""
    return state.get("next_action", "llm")


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------
def build_graph() -> StateGraph:
    """
    Construct and compile the LangGraph workflow.

    Returns:
        A compiled StateGraph ready for `.invoke()` or `.ainvoke()`.
    """
    graph = StateGraph(AgentState)

    # Register nodes
    graph.add_node("router", router_node)
    graph.add_node("rag", rag_node)
    graph.add_node("tools", tool_node)
    graph.add_node("llm", llm_node)

    # Entry point
    graph.set_entry_point("router")

    # Conditional branching after the router
    graph.add_conditional_edges(
        "router",
        _route_decision,
        {
            "rag": "rag",
            "tools": "tools",
            "llm": "llm",
        },
    )

    # After RAG or tools, always go to LLM for final synthesis
    graph.add_edge("rag", "llm")
    graph.add_edge("tools", "llm")

    # LLM is the terminal node
    graph.add_edge("llm", END)

    compiled = graph.compile()
    logger.info("Agent graph compiled  nodes=%s", list(compiled.nodes.keys()))
    return compiled


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------
agent = build_graph()
