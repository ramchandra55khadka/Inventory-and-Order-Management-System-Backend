FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps for postgres
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv
RUN pip install --upgrade pip && pip install uv

# Copy dependency manifests first for better caching
COPY pyproject.toml uv.lock /app/

# Sync dependencies (frozen to lockfile)
RUN uv sync --frozen

# Copy application source
COPY . /app

# Expose port
EXPOSE 8000

# Environment defaults
ENV DATABASE_URL=postgresql://postgres:ramchandra@db:5432/inventory_db \
    API_KEY=mysecretkey \
    LOW_STOCK_THRESHOLD=5

# Ensure Python can import the app package when running Alembic
ENV PYTHONPATH=/app

# Run Alembic migrations on container start, then launch server
CMD uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
