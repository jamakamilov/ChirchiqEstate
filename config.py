import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "REPLACE_WITH_TOKEN")
    ADMIN_IDS: str = os.getenv("ADMIN_IDS", "")  # comma separated
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data.db")
    CHANNEL_ID: str = os.getenv("CHANNEL_ID", "")  # @channelusername or -100...
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "uz")
    MEDIA_PATH: str = os.getenv("MEDIA_PATH", "./media")
    COMMISSION_PERCENT: float = float(os.getenv("COMMISSION_PERCENT", "2.0"))
    OSM_STATIC_MAP_URL: str = os.getenv("OSM_STATIC_MAP_URL", "https://staticmap.openstreetmap.de/staticmap.php")
    ENV: str = os.getenv("ENV", "dev")

    class Config:
        env_file = ".env"


settings = Settings()
