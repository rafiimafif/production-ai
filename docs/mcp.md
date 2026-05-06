# 🔌 Model Context Protocol (MCP) Integration

This project uses MCP to bridge the gap between AI models and external data/tools.

## What is MCP?
MCP is an open protocol that standardizes how AI agents interact with tools, resources, and prompts. Instead of writing custom connectors for every agent, we build an MCP server that any compatible agent can use.

## Implemented Tools

### 1. `search_documents`
- **Description**: Semantic search across the indexed RAG collection.
- **Inputs**: `query` (string), `collection` (string).
- **Returns**: Formatted text snippets from relevant documents.

### 2. `query_database`
- **Description**: Executes analytical SQL queries against the local DuckDB instance.
- **Inputs**: `sql` (string).
- **Returns**: JSON array of results.

### 3. `list_models`
- **Description**: Queries the local Ollama instance for currently downloaded models.
- **Returns**: A list of model names and versions.

## How to Add New Tools

New tools should be added in `backend/mcp/server.py` using the `@mcp_server.tool()` decorator:

```python
@mcp_server.tool()
def get_weather(location: str) -> str:
    """Fetches weather for a given location."""
    # Implementation here
    return f"The weather in {location} is sunny."
```

## Client Connection
The FastAPI backend acts as the MCP client, connecting to the local MCP server via a `StdioServerTransport` or `SSE`.
