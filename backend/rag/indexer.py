"""
Document indexer — ingests files into the RAG vector store.

Responsibilities:
  • Configure LlamaIndex to use Ollama for both LLM and embeddings.
  • Read documents from a local directory.
  • Chunk, embed, and store them in ChromaDB via the vector store adapter.
"""

from __future__ import annotations

import logging
from pathlib import Path

from llama_index.core import (
    Settings as LlamaSettings,
)
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

from backend.config import settings
from backend.rag.vectorstore import get_vector_store

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# LlamaIndex global configuration
# ---------------------------------------------------------------------------
_configured = False


def configure_llama_index() -> None:
    """
    Set the global LlamaIndex LLM and embedding model to use Ollama.

    This is idempotent — safe to call multiple times.
    """
    global _configured
    if _configured:
        return

    LlamaSettings.llm = Ollama(
        model=settings.default_model,
        base_url=settings.ollama_host,
        request_timeout=120.0,
    )
    LlamaSettings.embed_model = OllamaEmbedding(
        model_name="qwen2.5:1.5b",
        base_url=settings.ollama_host,
    )
    _configured = True
    logger.info(
        "LlamaIndex configured  llm=%s  embed=qwen2.5:1.5b",
        settings.default_model,
    )


# ---------------------------------------------------------------------------
# Document ingestion
# ---------------------------------------------------------------------------
def ingest_documents(
    doc_dir: str | Path = "./data/documents",
    collection: str = "default",
) -> VectorStoreIndex:
    """
    Read all supported files from `doc_dir`, chunk them, and index
    into the named ChromaDB collection.

    Args:
        doc_dir:    Path to the directory containing source documents.
        collection: ChromaDB collection name to index into.

    Returns:
        The constructed VectorStoreIndex (can be used immediately for queries).

    Raises:
        FileNotFoundError: If doc_dir does not exist.
        ValueError:        If doc_dir contains no readable files.
    """
    doc_path = Path(doc_dir)
    if not doc_path.exists():
        raise FileNotFoundError(f"Document directory not found: {doc_path}")

    configure_llama_index()

    logger.info("Ingesting documents from %s → collection '%s'", doc_path, collection)
    documents = SimpleDirectoryReader(str(doc_path)).load_data()

    if not documents:
        raise ValueError(f"No readable documents found in {doc_path}")

    logger.info("Loaded %d document chunks", len(documents))

    vector_store = get_vector_store(collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True,
    )

    logger.info("Indexing complete — %d chunks stored in '%s'", len(documents), collection)
    return index
