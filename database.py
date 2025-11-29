import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import make_url
from config import settings

logger = logging.getLogger("realestate_bot.database")
logger.setLevel(logging.INFO)

DATABASE_URL = os.getenv("DATABASE_URL", settings.DATABASE_URL)

def _normalize_async_url(url: str) -> str:
    """
    Ensure the URL uses an async driver compatible with SQLAlchemy async engine.
    - If postgres URL uses 'postgresql://' or 'postgres://', convert to 'postgresql+asyncpg://'
    - If sqlite uses 'sqlite://', convert to 'sqlite+aiosqlite://'
    Otherwise return as-is.
    """
    if not url:
        return url

    try:
        parsed = make_url(url)
    except Exception:
        # fallback: simple string checks
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+asyncpg://", 1)
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        if url.startswith("sqlite://") and "+aiosqlite" not in url:
            return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
        return url

    drivername = parsed.drivername  # e.g., 'postgresql', 'postgresql+psycopg2', 'sqlite'
    # Normalize postgres
    if drivername.startswith("postgresql"):
        if "asyncpg" not in drivername:
            # build new URL with asyncpg
            new_driver = "postgresql+asyncpg"
            parsed = parsed.set(drivername=new_driver)
            return str(parsed)
    # Normalize postgres short form 'postgres'
    if drivername == "postgres":
        parsed = parsed.set(drivername="postgresql+asyncpg")
        return str(parsed)
    # Normalize sqlite
    if drivername.startswith("sqlite") and "aiosqlite" not in drivername:
        parsed = parsed.set(drivername="sqlite+aiosqlite")
        return str(parsed)

    return str(parsed)


NORMALIZED_DATABASE_URL = _normalize_async_url(DATABASE_URL)
logger.info("Using database URL: %s", NORMALIZED_DATABASE_URL.split("://")[0] + "://***")

# Create async engine
engine = create_async_engine(NORMALIZED_DATABASE_URL, echo=False, future=True)

# Async session factory
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Declarative base
Base = declarative_base()


async def init_db():
    """
    Initialize database schema for local testing.
    For production use Alembic migrations instead.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized (create_all executed).")