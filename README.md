# 🚀 Production AI System 2026

A production-grade, zero-cost AI ecosystem built with local LLMs, agentic orchestration, and full observability.

## 🌟 Overview

This project implements a complete AI stack designed for performance, privacy, and cost-efficiency. It leverages local inference via Ollama, agentic workflows with LangGraph, and a standardized tool layer using the Model Context Protocol (MCP).

## 🛠️ Technology Stack

- **LLM Layer**: Ollama (Gemma 3, Llama 3.3, Mistral Small) - *Local & Free*
- **Orchestration**: LangGraph / CrewAI - *Agentic workflows*
- **RAG Engine**: LlamaIndex + ChromaDB - *Local vector search*
- **Tool Layer**: Model Context Protocol (MCP) - *Unified agent connectivity*
- **Frontend**: Next.js (App Router) + Tailwind CSS
- **Data Layer**: SQLite (App Data) + DuckDB (Analytics)
- **Observability**: Langfuse / Phoenix - *Self-hosted tracing*
- **Infrastructure**: Docker + Docker Compose

## 📁 Project Structure

```text
production-ai/
├── backend/            # FastAPI & LangGraph logic
├── frontend/           # Next.js web interface
├── docs/               # Detailed technical documentation
├── data/               # Local databases and vector stores (git ignored)
├── scripts/            # Setup and utility scripts
├── docker-compose.yml  # Container orchestration
└── pyproject.toml      # Backend dependencies (uv)
```

## 🚀 Quick Start

### Prerequisites
- [Ollama](https://ollama.com/) installed and running.
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.
- [uv](https://github.com/astral-sh/uv) (Python package manager).

### Setup
1. **Launch Services**:
   ```bash
   # Starts Backend, Frontend, ChromaDB, Langfuse, and Ollama
   docker-compose up -d
   ```

2. **Pull Models**:
   Since Ollama runs in Docker, pull the models into the container:
   ```bash
   docker exec -it production-ai-ollama ollama pull gemma3:4b
   docker exec -it production-ai-ollama ollama pull nomic-embed-text
   ```

3. **Environment Config**:
   Copy `.env.example` to `.env` and fill in your keys.

## 📖 Documentation Index

- [Architecture & Design](docs/architecture.md)
- [Implementation Roadmap](docs/implementation.md)
- [User Guide (Non-IT)](docs/user_guide.md)
- [Ollama Docker Setup](docs/ollama_docker_plan.md)
- [MCP Tool Integration](docs/mcp.md)

---
**Total Infrastructure Cost: $0.00**
