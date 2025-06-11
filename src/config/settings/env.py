"""
Keeping this module separate from Django Settings so that we can import it in other modules where we need just one of
settings without having to import all of Django settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    DATABASE_URL: str
    SECRET_KEY: str

    EXTRA_ALLOWED_HOSTS: list[str] = []
    CSRF_TRUSTED_ORIGINS: list[str] = []

    ADMIN_URL: str = 'admin/'

    # Debug & Development Settings
    DEBUG: bool = False
    INTERNAL_IPS: list[str] = []
    USE_VITE: bool = False
    VITE_URL: str = 'http://localhost:5173'

    # Sentry Settings
    SENTRY_DSN: str = ''


pydenset = EnvSettings()  # pyright: ignore[reportCallIssue]
