"""
Ollama LLM provider — thin async wrapper around the Ollama Python client.

Responsibilities:
  • Send chat completions (streaming and non-streaming).
  • List locally available models from the Ollama server.
  • Health-check the Ollama connection at startup.

All functions resolve the model tag through the central registry so callers
can use friendly IDs ("qwen2.5-7b") instead of raw Ollama tags ("qwen2.5:7b").
"""

from __future__ import annotations

import logging
from typing import Any, AsyncGenerator

import ollama as _ollama

from backend.config import settings
from backend.llm.models import MODELS, get_ollama_tag

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Client singleton
# ---------------------------------------------------------------------------
_client: _ollama.Client | None = None


def _get_client() -> _ollama.Client:
    """Lazy-initialise and return the Ollama client."""
    global _client
    if _client is None:
        _client = _ollama.Client(host=settings.ollama_host)
        logger.info("Ollama client connected to %s", settings.ollama_host)
    return _client


# ---------------------------------------------------------------------------
# Resolve model — accepts either a registry ID or a raw Ollama tag
# ---------------------------------------------------------------------------
def _resolve_model(model: str | None) -> str:
    """
    Turn a model identifier into an Ollama tag.

    Accepts:
      • None          → falls back to settings.default_model
      • Registry ID   → looked up in MODELS ("qwen2.5-7b" → "qwen2.5:7b")
      • Raw tag       → passed through as-is ("qwen2.5:7b" → "qwen2.5:7b")
    """
    if model is None:
        return settings.default_model
    if model in MODELS:
        return get_ollama_tag(model)
    return model  # assume it's already a valid Ollama tag


# ---------------------------------------------------------------------------
# Chat — non-streaming
# ---------------------------------------------------------------------------
def chat(
    messages: list[dict[str, str]],
    model: str | None = None,
) -> dict[str, Any]:
    """
    Send a chat completion request and return the full response.

    Args:
        messages: OpenAI-style message list [{"role": "user", "content": "..."}].
        model:    Registry ID or Ollama tag. Defaults to settings.default_model.

    Returns:
        The raw Ollama response dict containing `.message.content`, etc.
    """
    tag = _resolve_model(model)
    logger.debug("chat  model=%s  msgs=%d", tag, len(messages))
    response = _get_client().chat(model=tag, messages=messages)
    return response


# ---------------------------------------------------------------------------
# Chat — streaming
# ---------------------------------------------------------------------------
def chat_stream(
    messages: list[dict[str, str]],
    model: str | None = None,
) -> AsyncGenerator[str, None]:
    """
    Stream chat tokens one chunk at a time.

    Yields:
        Individual content strings as they arrive from Ollama.
    """
    tag = _resolve_model(model)
    logger.debug("chat_stream  model=%s  msgs=%d", tag, len(messages))
    stream = _get_client().chat(model=tag, messages=messages, stream=True)
    for chunk in stream:
        content = chunk.get("message", {}).get("content", "")
        if content:
            yield content


# ---------------------------------------------------------------------------
# List models available on the Ollama server
# ---------------------------------------------------------------------------
def list_models() -> list[dict[str, Any]]:
    """Return models currently downloaded on the local Ollama instance."""
    response = _get_client().list()
    return [
        {
            "name": m.model,
            "size": m.size,
            "modified_at": str(m.modified_at) if m.modified_at else None,
        }
        for m in response.models
    ]


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
def health_check() -> bool:
    """Return True if the Ollama server is reachable."""
    try:
        _get_client().list()
        return True
    except Exception as exc:
        logger.warning("Ollama health check failed: %s", exc)
        return False
