# 02 — Backend Container Specifications

- **Dockerfile**: `supporthub/backend/Dockerfile`
- **Base Image**: `python:3.13-slim`
- **Dependency Management**: `pyproject.toml` with `pip install --no-cache-dir .`
- **Runtime Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- **Health Check**: `curl -f http://localhost:8000/health || exit 1`
