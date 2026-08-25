"""Core configuration module re-exporting settings."""
from app.config import Settings, get_settings

settings = get_settings()

__all__ = ["Settings", "get_settings", "settings"]
