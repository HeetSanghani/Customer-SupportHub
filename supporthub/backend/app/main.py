"""SupportHub FastAPI application — entry point."""
from __future__ import annotations

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.config import get_settings
from app.database import init_db
from app.routers import auth, tickets, knowledge
from app.routers.ws import chat

settings = get_settings()

# ─── Sentry ───────────────────────────────────────────────────────────────────
if settings.sentry_dsn and not settings.sentry_dsn.startswith("https://..."):
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.app_env,
        traces_sample_rate=0.1,
    )

# ─── Rate Limiter ─────────────────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)

# ─── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="SupportHub API",
    version="1.0.0",
    description="AI-Powered Omnichannel Customer Support Platform",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ─── CORS ─────────────────────────────────────────────────────────────────────
origins = [settings.frontend_url]
if not settings.is_production:
    origins += ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Global exception handler ─────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if settings.is_production:
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})
    return JSONResponse(status_code=500, content={"detail": str(exc)})

# ─── Startup ──────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def on_startup():
    if not settings.is_production:
        await init_db()  # Use Alembic migrations in production

# ─── Routers ──────────────────────────────────────────────────────────────────
API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(tickets.router, prefix=API_PREFIX)
app.include_router(knowledge.router, prefix=API_PREFIX)
app.include_router(chat.router)           # WebSocket — no prefix

# ─── Health check ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "env": settings.app_env}
