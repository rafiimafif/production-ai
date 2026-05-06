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
    "gemma3": ModelInfo(
        id="gemma3",
        ollama_tag="gemma3:4b",
        description="Google Gemma 3 4B — fast reasoning and instruction following.",
        context_window=8192,
        use_case="general",
    ),
    "llama3": ModelInfo(
        id="llama3",
        ollama_tag="llama3.3:8b",
        description="Meta Llama 3.3 8B — high-quality generation for complex tasks.",
        context_window=8192,
        use_case="complex",
    ),
    "mistral": ModelInfo(
        id="mistral",
        ollama_tag="mistral-small:latest",
        description="Mistral Small — balanced speed and quality.",
        context_window=32768,
        use_case="general",
    ),
    "nomic-embed": ModelInfo(
        id="nomic-embed",
        ollama_tag="nomic-embed-text",
        description="Nomic Embed Text — embedding model for RAG pipelines.",
        context_window=8192,
        use_case="embedding",
    ),
}

DEFAULT_CHAT_MODEL = "gemma3"
DEFAULT_EMBED_MODEL = "nomic-embed"


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
