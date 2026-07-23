import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

logger = logging.getLogger(__name__)

# We no longer define Base here. It's imported from app.models.base where needed.

# Create Async Engine
try:
    engine = create_async_engine(
        settings.async_database_uri,
        pool_pre_ping=settings.DB_POOL_PRE_PING,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_recycle=settings.DB_POOL_RECYCLE,
        echo=settings.DEBUG,
    )
    
    # Session factory
    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
except Exception as e:
    logger.error(f"Failed to initialize database engine: {e}")
    raise e

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function that yields database sessions.
    Handles rollback on exceptions and always closes the session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error, rolled back transaction: {e}")
            raise e
        finally:
            await session.close()
