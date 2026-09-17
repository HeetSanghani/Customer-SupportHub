FROM python:3.13-slim

# Install uv for fast, reliable package installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies with uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application source
COPY app ./app
COPY main.py ./
COPY alembic.ini ./
COPY alembic ./alembic
COPY clean_and_seed.py ./
COPY start.sh ./
RUN chmod +x start.sh

# Create uploads directory
RUN mkdir -p /app/uploads

ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["./start.sh"]
