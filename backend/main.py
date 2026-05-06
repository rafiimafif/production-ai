"""
FastAPI Entry Point — The API Gateway.

Exposes REST endpoints for the Next.js frontend to interact with the
LLMs, RAG pipeline, and agent orchestration.
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.agents.graph import agent
from backend.config import settings
from backend.llm.provider import chat, health_check, list_models
from backend.observability.tracing import get_langfuse_handler, observe
from backend.rag.indexer import ingest_documents
from backend.rag.retriever import query as rag_query

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# FastAPI App Initialization
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Production AI Gateway",
    version="0.1.0",
    description="API for local LLMs, RAG, and LangGraph agents.",
)

# CORS configuration for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "*"],  # * for local development ease
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    messages: list[dict]
    model: str | None = None
    use_agent: bool = False


class QueryRequest(BaseModel):
    question: str
    collection: str = "default"


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/health")
def health_endpoint():
    """System health check endpoint."""
    ollama_ok = health_check()
    return {"status": "ok", "ollama": ollama_ok}


@app.get("/api/models")
def get_models_endpoint():
    """List available Ollama models."""
    return {"models": list_models()}


@app.post("/api/chat")
@observe()
async def chat_endpoint(req: ChatRequest):
    """
    Send a message to the LLM.
    If `use_agent` is True, routes through the LangGraph workflow.
    """
    if req.use_agent:
        logger.info("Routing chat through LangGraph agent.")
        # Setup Langfuse tracing if enabled
        handler = get_langfuse_handler()
        config = {"callbacks": [handler]} if handler else {}

        # Invoke agent asynchronously
        result = await agent.ainvoke({"messages": req.messages}, config=config)

        # Extract the last message (AIMessage) content
        last_message = result["messages"][-1]
        content = getattr(last_message, "content", str(last_message))
        return {"response": content}

    # Direct chat bypasses the agent (synchronous fallback, handled in threadpool)
    logger.info("Routing chat directly to Ollama.")
    response = chat(req.messages, req.model)
    return {"response": response.message.content}


@app.post("/api/query")
@observe()
def query_endpoint(req: QueryRequest):
    """Directly query the RAG pipeline."""
    logger.info("Direct RAG query received.")
    return rag_query(req.question, req.collection)


@app.post("/api/documents")
def upload_documents_endpoint(files: list[UploadFile] = File(...)):
    """Upload and ingest documents into the ChromaDB vector store."""
    logger.info("Received %d files for indexing.", len(files))

    doc_dir = Path("./data/documents")
    doc_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []
    for f in files:
        if not f.filename:
            continue
        dest = doc_dir / f.filename
        # Save file to disk
        with dest.open("wb") as buf:
            shutil.copyfileobj(f.file, buf)
        saved_files.append(f.filename)

    if saved_files:
        logger.info("Ingesting newly uploaded documents...")
        ingest_documents(str(doc_dir))

    return {"indexed": saved_files}
