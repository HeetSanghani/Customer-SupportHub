from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    app_env: str = "development"
    secret_key: str = "change_me"
    frontend_url: str = "http://localhost:5173"
    backend_url: str = "http://localhost:8001"   # Set to your public domain in production

    # Database
    database_url: str = "postgresql+asyncpg://supporthub:supporthub_dev@localhost:5432/supporthub"

    # Redis / Celery
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # Auth
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Claude AI
    anthropic_api_key: str = ""
    ai_default_model: str = "claude-sonnet-4-5"
    ai_cheap_model: str = "claude-haiku-4-5"
    ai_confidence_threshold: float = 0.75

    # Gemini AI
    gemini_api_key: str = ""

    # Email
    postmark_server_token: str = ""
    postmark_from_email: str = "support@yourdomain.com"
    support_contact_email: str = "support@yourdomain.com"

    # Storage
    supabase_url: str = ""
    supabase_service_key: str = ""
    supabase_bucket: str = "supporthub-attachments"

    # Sentry
    sentry_dsn: str = ""

    # Mailgun Email
    mailgun_api_key: str = ""
    mailgun_domain: str = ""

    # Meta (WhatsApp / Instagram / Facebook)
    meta_app_secret: str = ""
    meta_verify_token: str = "supporthub_verify"
    meta_app_token: str = ""
    whatsapp_phone_id: str = ""
    whatsapp_access_token: str = ""
    page_access_token: str = ""
    ig_page_id: str = ""
    fb_page_id: str = ""
    instagram_access_token: str = ""
    instagram_account_id: str = ""
    instagram_app_secret: str = ""

    # OpenAI / LLM
    openai_api_key: str = ""

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    @property
    def mailgun_is_sandbox(self) -> bool:
        return "sandbox" in (self.mailgun_domain or "").lower()


@lru_cache
def get_settings() -> Settings:
    return Settings()
