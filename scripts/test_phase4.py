"""Quick validation for Phase 4 agent modules."""

# Test 1: tools module
from backend.agents.tools import TOOL_REGISTRY, get_tool

assert "search_knowledge_base" in TOOL_REGISTRY
assert "query_database" in TOOL_REGISTRY

try:
    get_tool("nonexistent")
    assert False, "Should have raised KeyError"
except KeyError:
    pass

print("tools.py  — ALL CHECKS PASSED")

# Test 2: nodes module
from langchain_core.messages import HumanMessage

from backend.agents.nodes import llm_node, rag_node, router_node, tool_node

state_rag = {"messages": [HumanMessage(content="search for documents about Python")]}
result = router_node(state_rag)
assert result["next_action"] == "rag", f"Expected rag, got {result['next_action']}"

state_tool = {"messages": [HumanMessage(content="execute a database query")]}
result = router_node(state_tool)
assert result["next_action"] == "tools", f"Expected tools, got {result['next_action']}"

state_llm = {"messages": [HumanMessage(content="hello how are you")]}
result = router_node(state_llm)
assert result["next_action"] == "llm", f"Expected llm, got {result['next_action']}"

state_empty = {"messages": []}
result = router_node(state_empty)
assert result["next_action"] == "llm", f"Expected llm for empty, got {result['next_action']}"

print("nodes.py  — ALL CHECKS PASSED")

# Test 3: graph compiles
from backend.agents.graph import AgentState, agent

assert agent is not None
assert "router" in agent.nodes
assert "rag" in agent.nodes
assert "tools" in agent.nodes
assert "llm" in agent.nodes

print("graph.py  — ALL CHECKS PASSED")
