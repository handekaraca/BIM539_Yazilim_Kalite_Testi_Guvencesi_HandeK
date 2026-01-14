

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from app.main import app
from app.database import Base, get_db, DATABASE_URL
from typing import AsyncGenerator

# Test için ayrı bir SQLite dosyası kullanalım
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_database.db"

test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool, future=True)

TestingSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def db_session():
    # Bağlantıyı başlat
    async with test_engine.connect() as connection:
        # Ana transaction başlat
        transaction = await connection.begin()
        
        # Test izolasyonu için SAVEPOINT oluştur
        nested = await connection.begin_nested()
        
        # Test için session oluştur, bu connection'a bağla
        session_factory = async_sessionmaker(
            bind=connection,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
            join_transaction_mode="create_savepoint" # SQLAlchemy 2.0+ özelliği
        )
        session = session_factory()

        yield session

        # Temizlik
        await session.close()
        
        # Eğer nested transaction hala aktifse rollback yap
        if nested.is_active:
            await nested.rollback()
            
        await transaction.rollback()

@pytest.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()
