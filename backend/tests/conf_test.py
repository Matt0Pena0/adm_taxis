import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from backend.main import app
from backend.core.db import get_session


DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(
    DATABASE_URL_TEST, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

# 2. Fixture de la Sesión de BD
@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    # Crea las tablas en la BD en memoria
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Genera la sesión
    async_session = sessionmaker(
        engine_test, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session
    
    # Al terminar el test, borra todo
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:

    # Sobreescribe la dependencia get_session de la app, para poder usar la de test
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override

    # Crea el cliente apuntando a la app
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

        # Limpia los overrides al terminar
        app.dependency_overrides.clear()
