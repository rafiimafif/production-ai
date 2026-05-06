"""
Observability and Tracing — Integrates Langfuse for telemetry.

Provides a Langfuse client for manual tracing, a callback handler for
LangGraph/LangChain workflows, and graceful degradation if keys are missing.
"""

from __future__ import annotations

import logging
import os

from langfuse import Langfuse, observe
from langfuse.langchain import CallbackHandler

from backend.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Singleton Langfuse client
# ---------------------------------------------------------------------------
_langfuse_client: Langfuse | None = None


def get_langfuse() -> Langfuse | None:
    """
    Lazy-init and return the Langfuse client if configured.
    Returns None if keys are missing, allowing the app to degrade gracefully.
    """
    global _langfuse_client
    if _langfuse_client is None:
        if not settings.langfuse_secret_key or not settings.langfuse_public_key:
            logger.warning("Langfuse keys missing. Tracing disabled.")
            return None

        try:
            _langfuse_client = Langfuse(
                secret_key=settings.langfuse_secret_key,
                public_key=settings.langfuse_public_key,
                host=settings.langfuse_host,
            )
            logger.info("Langfuse client initialised (host=%s)", settings.langfuse_host)
        except Exception as exc:
            logger.error("Failed to init Langfuse client: %s", exc)

    return _langfuse_client

# ---------------------------------------------------------------------------
# LangChain / LangGraph Callback Handler
# ---------------------------------------------------------------------------
def get_langfuse_handler() -> CallbackHandler | None:
    """
    Return a Langfuse CallbackHandler for LangChain/LangGraph.
    Pass this to agent.invoke(..., config={"callbacks": [handler]})
    """
    if not settings.langfuse_secret_key or not settings.langfuse_public_key:
        return None

    try:
        # Langfuse CallbackHandler reads from environment variables
        os.environ["LANGFUSE_SECRET_KEY"] = settings.langfuse_secret_key
        os.environ["LANGFUSE_PUBLIC_KEY"] = settings.langfuse_public_key
        os.environ["LANGFUSE_HOST"] = settings.langfuse_host

        handler = CallbackHandler(public_key=settings.langfuse_public_key)
        return handler
    except Exception as exc:
        logger.error("Failed to init Langfuse callback handler: %s", exc)
        return None

# Re-export @observe for manual function tracing if needed elsewhere
__all__ = ["get_langfuse", "get_langfuse_handler", "observe"]
