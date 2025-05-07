from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from models.MOD_User import User
from api.security.security_login import check_password

async def search_user_from_username(session: AsyncSession, username_in):
    return await session.get(User, username_in)

async def search_user(session: AsyncSession, user_for_search):
    search_user_from_username()


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
    session.add(User)
    await session.commit()





