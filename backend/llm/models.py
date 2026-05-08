"""
Model registry — defines all available local LLM models and their metadata.

This module acts as a single source of truth for model names, Ollama tags,
and capabilities. Add new models here when pulling them via `ollama pull`.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelInfo:
    """Immutable descriptor for an Ollama model."""

    id: str            # Internal identifier (used in API requests)
    ollama_tag: str    # Exact tag passed to `ollama.chat(model=...)`
    description: str   # Human-readable summary
    context_window: int  # Max context length in tokens
    use_case: str      # Primary intended use


# ---------------------------------------------------------------------------
# Registry — extend this dict when you pull new models.
# ---------------------------------------------------------------------------
MODELS: dict[str, ModelInfo] = {
    "qwen2.5-14b": ModelInfo(
        id="qwen2.5-14b",
        ollama_tag="qwen2.5:14b",
        description="Alibaba Qwen 2.5 14B — highly capable for agentic workflows.",
        context_window=32768,
        use_case="complex",
    ),
    "qwen2.5-7b": ModelInfo(
        id="qwen2.5-7b",
        ollama_tag="qwen2.5:7b",
        description="Alibaba Qwen 2.5 7B — extremely fast and efficient for daily use.",
        context_window=32768,
        use_case="general",
    ),
    "qwen2.5-1.5b": ModelInfo(
        id="qwen2.5-1.5b",
        ollama_tag="qwen2.5:1.5b",
        description="Alibaba Qwen 2.5 1.5B — small, fast model for embeddings and light tasks.",
        context_window=32768,
        use_case="embedding",
    ),
}

DEFAULT_CHAT_MODEL = "qwen2.5-7b"
DEFAULT_EMBED_MODEL = "qwen2.5-1.5b"


def get_model(model_id: str) -> ModelInfo:
    """Look up a model by its internal ID. Raises KeyError if not found."""
    if model_id not in MODELS:
        available = ", ".join(MODELS.keys())
        raise KeyError(f"Unknown model '{model_id}'. Available: {available}")
    return MODELS[model_id]


def get_ollama_tag(model_id: str) -> str:
    """Shortcut — return the Ollama tag string for a given model ID."""
    return get_model(model_id).ollama_tag


def list_registered_models() -> list[dict]:
    """Return all registered models as serializable dicts."""
    return [
        {
            "id": m.id,
            "ollama_tag": m.ollama_tag,
            "description": m.description,
            "context_window": m.context_window,
            "use_case": m.use_case,
        }
        for m in MODELS.values()
    ]
