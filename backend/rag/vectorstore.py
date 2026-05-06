"""
Vector store adapter — abstracts ChromaDB setup and collection management.

This module provides a clean interface to create, access, and manage
ChromaDB collections. All persistent storage goes to the path defined
in settings.chroma_persist_dir.
"""

from __future__ import annotations

import logging

import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

from backend.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# ChromaDB client (singleton)
# ---------------------------------------------------------------------------
_chroma_client: chromadb.ClientAPI | None = None


def get_chroma_client() -> chromadb.ClientAPI:
    """Return a persistent ChromaDB client, creating it on first call."""
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        logger.info("ChromaDB client initialised at %s", settings.chroma_persist_dir)
    return _chroma_client


# ---------------------------------------------------------------------------
# Collection helpers
# ---------------------------------------------------------------------------
def get_or_create_collection(name: str = "default") -> chromadb.Collection:
    """Get an existing collection or create a new one."""
    client = get_chroma_client()
    collection = client.get_or_create_collection(name=name)
    logger.debug("Collection '%s' ready  (count=%d)", name, collection.count())
    return collection


def delete_collection(name: str) -> None:
    """Delete a collection by name. No-op if it doesn't exist."""
    client = get_chroma_client()
    try:
        client.delete_collection(name=name)
        logger.info("Deleted collection '%s'", name)
    except ValueError:
        logger.warning("Collection '%s' not found — nothing to delete", name)


def list_collections() -> list[str]:
    """Return the names of all existing collections."""
    client = get_chroma_client()
    return [c.name for c in client.list_collections()]


# ---------------------------------------------------------------------------
# LlamaIndex-compatible vector store
# ---------------------------------------------------------------------------
def get_vector_store(collection_name: str = "default") -> ChromaVectorStore:
    """
    Return a LlamaIndex ChromaVectorStore backed by the named collection.

    This is the object you pass into StorageContext.from_defaults().
    """
    collection = get_or_create_collection(collection_name)
    return ChromaVectorStore(chroma_collection=collection)
