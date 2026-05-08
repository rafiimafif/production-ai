# 🚀 Production AI System 2026

A production-grade, zero-cost AI ecosystem built with local LLMs, agentic orchestration, and full observability.

## 🌟 Overview

This project implements a complete AI stack designed for performance, privacy, and cost-efficiency. It leverages local inference via Ollama, agentic workflows with LangGraph, and a standardized tool layer using the Model Context Protocol (MCP).

## 🛠️ Technology Stack

- **LLM Layer**: Ollama (Qwen 2.5 14B, Qwen 2.5 7B) - _Local & Free_
- **Orchestration**: LangGraph / CrewAI - _Agentic workflows_
- **RAG Engine**: LlamaIndex + ChromaDB - _Local vector search_
- **Tool Layer**: Model Context Protocol (MCP) - _Unified agent connectivity_
- **Frontend**: Next.js (App Router) + Tailwind CSS
- **Data Layer**: SQLite (App Data) + DuckDB (Analytics)
- **Observability**: Langfuse / Phoenix - _Self-hosted tracing_
- **Infrastructure**: Docker + Docker Compose

## ✨ Key Features

- **Local-First Inference**: Run state-of-the-art models like Qwen 2.5 entirely on your own hardware using Ollama.
- **Smart RAG (Retrieval-Augmented Generation)**: Chat with your own PDF and text documents with high-precision vector search.
- **Agentic Workflows**: Multi-step reasoning powered by LangGraph that knows when to search files vs. query databases.
- **Unified Tooling (MCP)**: Standardized connection to external tools using the Model Context Protocol.
- **Full Observability**: Integrated Langfuse dashboard for tracing every thought and action your AI takes.
- **Premium UI**: A sleek, dark-mode dashboard built with Next.js and Tailwind CSS.

## 🚀 Quick Start

### 1. Launch Services

Everything is containerized. Start the entire ecosystem with one command:

```bash
docker-compose up -d
```

### 2. Prepare the AI Brain

Ollama runs inside Docker. Pull your preferred models to begin:

```bash
# Chat & Reasoning
docker exec -it production-ai-ollama ollama pull qwen2.5:14b
docker exec -it production-ai-ollama ollama pull qwen2.5:7b

# Embeddings (for reading documents)
docker exec -it production-ai-ollama ollama pull qwen2.5:1.5b
```

### 3. Access the Dashboard

- **Web UI**: [http://localhost:3000](http://localhost:3000)
- **API Gateway**: [http://localhost:8000](http://localhost:8000)
- **Langfuse (Tracing)**: [http://localhost:3100](http://localhost:3100)

## 📁 Project Structure

```text
production-ai/
├── backend/            # FastAPI, LangGraph & Agent logic
├── frontend/           # Next.js (App Router) Dashboard
├── docs/               # Detailed technical & user guides
├── data/               # Vector stores & local DBs (ignored by git)
├── scripts/            # Testing & utility scripts
├── docker-compose.yml  # System orchestration
└── pyproject.toml      # Python dependencies
```

## 🤝 Contributing

This repository has **Branch Protection** enabled.

- Direct pushes to `main` are restricted.
- Please create a new branch for your features and submit a **Pull Request (PR)**.
- Ensure your code passes linting (`ruff` for backend, `eslint` for frontend).

## 📖 Documentation Index

- [Architecture & Design](docs/architecture.md)
- [User Guide (Non-IT)](docs/user_guide.md)
- [Implementation Roadmap](docs/implementation.md)
- [Ollama Docker Setup](docs/ollama_docker_plan.md)
- [MCP Tool Integration](docs/mcp.md)

---

**Total Infrastructure Cost: $0.00** | **Data Privacy: 100%**
