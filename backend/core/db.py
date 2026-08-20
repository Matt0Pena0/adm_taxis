import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from models.chofer import *
from models.coche import *
from models.recaudacion import *


# Lee la URL de la base de datos desde una variable de entorno.
# Proporciona un valor predeterminado para desarrollo (SQLite).
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///data/db.sqlite")

# Asegura que la carpeta contenedora exista si se utiliza SQLite
if DATABASE_URL.startswith("sqlite"):
    db_path = DATABASE_URL.split("sqlite", 1)[-1].split(":///")[-1]
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

# El argumento `connect_args` es necesario solo para SQLite para evitar
# errores de concurrencia en un entorno asíncrono.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_async_engine(DATABASE_URL, echo=True, future=True, connect_args=connect_args)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
