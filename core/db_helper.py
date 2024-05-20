from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, \
    AsyncSession

from core.config import settings


class DBHelper:
    def __init__(self):
        self.async_engine = create_async_engine(
            url=settings.db_url
        )
        self.async_session = async_sessionmaker(
            bind=self.async_engine
        )

    async def session_getter(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session


db_helper = DBHelper()
