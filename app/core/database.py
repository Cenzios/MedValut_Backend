from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# ------------------ Singleton Engine & Session ------------------
_engine = None
_SessionLocal = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            pool_pre_ping=True,
            future=True,
        )
    return _engine

def get_sessionmaker() -> sessionmaker:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _SessionLocal

# Dependency for FastAPI routes
async def get_db() -> AsyncSession:
    """
    Async dependency to provide a session
    """
    async_session = get_sessionmaker()
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()