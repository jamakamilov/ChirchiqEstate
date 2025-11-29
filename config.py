import os
from typing import Optional


def _get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    v = os.getenv(name)
    return v if v is not None else default


class Settings:
    BOT_TOKEN: str
    ADMIN_IDS: str
    DATABASE_URL: str
    CHANNEL_ID: str
    DEFAULT_LANGUAGE: str
    MEDIA_PATH: str
    COMMISSION_PERCENT: float
    OSM_STATIC_MAP_URL: str
    ENV: str

    def __init__(self):
        self.BOT_TOKEN = _get_env("BOT_TOKEN", "REPLACE_WITH_TOKEN")
        self.ADMIN_IDS = _get_env("ADMIN_IDS", "")
        self.DATABASE_URL = _get_env("DATABASE_URL", "sqlite+aiosqlite:///./data.db")
        self.CHANNEL_ID = _get_env("CHANNEL_ID", "")
        self.DEFAULT_LANGUAGE = _get_env("DEFAULT_LANGUAGE", "uz")
        self.MEDIA_PATH = _get_env("MEDIA_PATH", "./media")
        # safe float parsing with fallback
        try:
            self.COMMISSION_PERCENT = float(_get_env("COMMISSION_PERCENT", "2.0"))
        except Exception:
            self.COMMISSION_PERCENT = 2.0
        self.OSM_STATIC_MAP_URL = _get_env(
            "OSM_STATIC_MAP_URL", "https://staticmap.openstreetmap.de/staticmap.php"
        )
        self.ENV = _get_env("ENV", "dev")


# единый экземпляр настроек, как раньше
settings = Settings()