from sqlalchemy.testing.schema import mapped_column
import asyncio

import db.database
from db.database import Base
from sqlalchemy.orm import Mapped


class UsersModelDB(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    role: Mapped[str]

async def main():
    await db.database.setup_databes()

if __name__ == "__user_init__":
    asyncio.run(main())
