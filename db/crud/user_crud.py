from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from models.MOD_User import User
from db.inits.users_init import Users
from api.security.security_login import check_password


async def exit_user(session: AsyncSession, username_in: str):
    stmt = select(Users).where(Users.username == username_in)
    result = await session.execute(stmt)
    return result.scalars().first()

"""
def check_user(username):
    for user in users:
        if user.username == username:
            return True
    return False
    
def dump_db():
    users_dump = {}
    for u in users:
        users_dump.update(u)
    return users_dump
"""


async def create_new_user(session: AsyncSession, user: User):
    new_user = Users(**user.model_dump())
    session.add(new_user)
    await session.commit()


async def search_user_from_username(session: AsyncSession, username_in: str):
    stmt = select(Users).where(Users.username == username_in)
    result = await session.execute(stmt)
    user_obj = result.scalar_one_or_none()
    return User.model_validate(user_obj)


async def login_user(session: AsyncSession, user_in: User):
    user = await search_user_from_username(session, user_in.username)
    if check_password(user_in.password, user.password):
        return await user




