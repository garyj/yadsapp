"""
Keeping this module separate from Django Settings so that we can import it in other modules where we need just one of
settings without having to import all of Django settings.
"""

from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    DEBUG: bool = False
    USE_VITE: bool = False
    INTERNAL_IPS: list[str] = []

    EXTRA_ALLOWED_HOSTS: list[str] = []
    CSRF_TRUSTED_ORIGINS: list[str] = []

    class Config:
        env_file = '.env'


pydenset = EnvSettings()  # pyright: ignore[reportCallIssue]
