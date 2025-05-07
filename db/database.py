from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session
from sqlalchemy.log import echo_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import asyncio
from asyncio import current_task

from .config import settings



class DatabaseHelper:
    def __init__(self, db_url: str, echo: bool = True):
        self.engine = create_async_engine(
            url=db_url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        return session


    async def session_dependency(self):
        session = self.get_scoped_session()
        try:
            yield session
        finally:
            await session.close()


db_engine_session = DatabaseHelper(settings.db_url, settings.echo)