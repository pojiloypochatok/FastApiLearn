from models.MOD_User import User, RegUserInDb
from api.security.security_login import check_password

users = []


def search_user(user_for_search):
    for user in users:
        if user.username == user_for_search.username:
            if check_password(user_for_search.password, user.password):
                return user
    return None

def search_user_from_username(username_in):
    for user in users:
        if user.username == username_in:
            return user

def check_user(username):
    for user in users:
        if user.username == username:
            return True
    return False

def create_new_user(user: RegUserInDb):
    users.append(user)

def dump_db():
    users_dump = {}
    for u in users:
        users_dump.update(u)
    return users_dump


