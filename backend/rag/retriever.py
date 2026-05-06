"""
RAG retriever — query engine that searches indexed documents.

Responsibilities:
  • Build a query engine from an existing ChromaDB collection.
  • Execute natural-language queries and return answers with sources.
"""

from __future__ import annotations

import logging
from typing import Any

from llama_index.core import VectorStoreIndex
from llama_index.core.storage import StorageContext

from backend.rag.indexer import configure_llama_index
from backend.rag.vectorstore import get_vector_store

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Query engine factory
# ---------------------------------------------------------------------------
def get_query_engine(
    collection: str = "default",
    top_k: int = 5,
):
    """
    Build a LlamaIndex query engine backed by the named ChromaDB collection.

    Args:
        collection: Name of the ChromaDB collection to search.
        top_k:      Number of similar chunks to retrieve.

    Returns:
        A LlamaIndex QueryEngine ready for `.query()` calls.
    """
    configure_llama_index()

    vector_store = get_vector_store(collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_vector_store(
        vector_store,
        storage_context=storage_context,
    )

    engine = index.as_query_engine(similarity_top_k=top_k)
    logger.debug("Query engine ready  collection='%s'  top_k=%d", collection, top_k)
    return engine


# ---------------------------------------------------------------------------
# High-level query function
# ---------------------------------------------------------------------------
def query(
    question: str,
    collection: str = "default",
    top_k: int = 5,
) -> dict[str, Any]:
    """
    Run a natural-language query against the RAG index.

    Args:
        question:   The user's question in plain English.
        collection: ChromaDB collection to search.
        top_k:      Number of source chunks to retrieve.

    Returns:
        Dict with keys:
          - "answer"  (str):  The synthesized answer from the LLM.
          - "sources" (list): Retrieved source chunks with text and score.
    """
    logger.info("RAG query  collection='%s'  q='%s'", collection, question[:80])

    engine = get_query_engine(collection, top_k)
    response = engine.query(question)

    sources = []
    for node in response.source_nodes:
        sources.append({
            "text": node.text[:300],
            "score": round(node.score, 4) if node.score is not None else None,
            "metadata": node.metadata,
        })

    logger.info("RAG response  sources=%d", len(sources))
    return {
        "answer": str(response),
        "sources": sources,
    }
