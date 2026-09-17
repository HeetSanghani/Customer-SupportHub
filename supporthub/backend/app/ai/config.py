"""Configuration settings for SupportHub AI Architecture."""
import os
from pathlib import Path
from dataclasses import dataclass, field




def _default_dataset_path() -> str:
    """Compute the dataset path fallback safely for both local and Docker environments."""
    _this = Path(__file__).resolve()
    # Try progressively shallower parent levels (local dev has deeper nesting)
    for level in (5, 4, 3):
        try:
            candidate = _this.parents[level] / "supporthub-data-generator" / "output"
            return str(candidate)
        except IndexError:
            continue
    # Final fallback: sibling of /app inside container
    return "/app/data/output"


@dataclass
class Settings:
    """System settings for data access, RAG pipeline, and AI orchestration."""
    
    # Base paths
    BASE_DIR: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent)
    
    # Dataset path (configurable via DATASET_PATH env variable)
    DATASET_PATH: Path = field(default_factory=lambda: Path(
        os.getenv("DATASET_PATH", _default_dataset_path())
    ))
    
    # RAG Settings
    RAG_CHUNK_SIZE: int = int(os.getenv("RAG_CHUNK_SIZE", "500"))
    RAG_CHUNK_OVERLAP: int = int(os.getenv("RAG_CHUNK_OVERLAP", "50"))
    RAG_SIMILARITY_THRESHOLD: float = float(os.getenv("RAG_SIMILARITY_THRESHOLD", "0.05"))
    RAG_TOP_K: int = int(os.getenv("RAG_TOP_K", "3"))
    
    # Provider Settings (Provider-independent abstractions)
    EMBEDDING_PROVIDER: str = os.getenv("EMBEDDING_PROVIDER", "local")  # "local", "openai", "vertex"
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "local-tfidf-vector")
    VECTOR_STORE_PROVIDER: str = os.getenv("VECTOR_STORE_PROVIDER", "memory")  # "memory", "chroma", "pgvector"
    
    # LLM Settings
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini" if os.getenv("GEMINI_API_KEY") or os.getenv("LLM_API_KEY") else "gemini")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.0"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "1000"))
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "15"))
    GROUNDING_STRICTNESS: str = os.getenv("GROUNDING_STRICTNESS", "strict")
    
    # Security Settings
    ENFORCE_CUSTOMER_OWNERSHIP: bool = True
    INTERCEPT_SENSITIVE_CREDENTIALS: bool = True

    def get_resolved_dataset_path(self) -> Path:
        """Resolve dataset directory and verify existence."""
        path = self.DATASET_PATH
        if not path.exists():
            _this = Path(__file__).resolve()
            for _level in (3, 4):
                try:
                    _candidate = _this.parents[_level] / "output"
                    if _candidate.exists():
                        return _candidate
                except IndexError:
                    continue
        if not path.is_absolute():
            path = (self.BASE_DIR / path).resolve()
        return path


# Singleton global settings instance
settings = Settings()
