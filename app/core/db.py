from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from ..models.chofer import *
from ..models.coche import *
from ..models.recaudacion import *


sqlite_file_name = "db.sqlite"
DATABASE_URL = f"sqlite+aiosqlite:///{sqlite_file_name}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async def get_session():
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

# DATABASE_URL = "postgresql://user:password@localhost/taxi_db"

# engine = create_engine(DATABASE_URL, echo=True)


# def get_session():
#     with Session(engine) as session:
#         yield session
