FROM python:3.12-slim
WORKDIR /app

# Install uv (Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency manifests
COPY pyproject.toml uv.lock ./

# Install dependencies (frozen to ensure lockfile is respected, no-dev to skip test tools)
RUN uv sync --frozen --no-dev

# Copy application code
COPY backend/ ./backend/
# Create data directories if they don't exist
RUN mkdir -p data/documents data/chroma_db

# Expose API port
EXPOSE 8000

# Start FastAPI using Uvicorn
CMD ["uv", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
