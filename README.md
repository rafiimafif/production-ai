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

## ✨ Key Features

- **Local-First Inference**: Run state-of-the-art models like Gemma 3 and Llama 3.3 entirely on your own hardware using Ollama.
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
docker exec -it production-ai-ollama ollama pull gemma3:4b

# Embeddings (for reading documents)
docker exec -it production-ai-ollama ollama pull nomic-embed-text
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
