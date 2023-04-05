import logging
from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

engine: AsyncEngine = create_async_engine(settings.postgres_uri)
logging.info("Database connected.")

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)
logging.info("Session created.")


def get_session() -> Generator:
    """Retorna uma sessão do banco de dados"""
    session: AsyncSession = Session()
    logging.info("Dependecies loaded.")

    try:
        yield session
    finally:
        session.close
    logging.info("Session closed.")
