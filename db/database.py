from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import asyncio

DB_NAME = "FastAPILearn"
engine = create_async_engine(f'sqlite+aiosqlite:///{DB_NAME}.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session


class Base(DeclarativeBase):
    pass

async def setup_databes():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



"""inits"""
class UsersModelDB(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    role: Mapped[str]

asyncio.run(setup_databes())




