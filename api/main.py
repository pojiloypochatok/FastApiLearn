from fastapi import FastAPI, Header, Depends, HTTPException, status, Request, Response
from fastapi.openapi.utils import status_code_ranges
from fastapi.params import Cookie
from pyexpat.errors import messages
from typing_extensions import Annotated
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from functools import wraps


from models import MOD_Headers
from models.MOD_User import User
from api.security.security_login import create_jwt_token, get_user_from_token, check_password, hash_password


app = FastAPI()
logger = logging.getLogger("uvicorn")
limiter = Limiter(key_func=lambda request: request.client.host)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

def get_user_from_db(username):
    for user in fakedb.Users.users:
        if user.username == username:
            return user

class PermissionChecker:
    """Декоратор для проверки ролей пользователя"""
    def __init__(self, roles: list[str]):
        self.roles = roles  # Список разрешённых ролей

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_user_from_token(kwargs.get("token"))  # Получаем текущего пользователя
            if not user:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Требуется аутентификация")

            if "admin" in user.role:  # Админ всегда имеет доступ ко всему
                return func(*args, **kwargs)

            if not any(role in user.roles for role in self.roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Недостаточно прав для доступа"
                )
            return func(*args, **kwargs)
        return wrapper

@app.get("/headers")
def headers(header: Annotated[MOD_Headers.CommonHeaders, Header()]):
    return {
        "user-agent" : header.user_agent,
        "Accept-Language": header.accept_language,
        "message": "Залупка"
    }

@app.get("/info")
def info(header: Annotated[MOD_Headers.CommonHeaders, Header()]):
    return {
        "headers": f"\nUser-Agent: {header.user_agent}\n Accept-Language:\n{header.accept_language}"
    }

@app.post("/login")
@limiter.limit("5/minute")
def login(request: Request, user_in: User, response: Response):
    response_from_db = fakedb.DB_Users.search_user(user_in)
    if response_from_db is None:
        raise HTTPException(status_code=401, detail="Такой пользователь не зарегестрирован")
    else:
        token = create_jwt_token({"sub": user_in.username})
        response.set_cookie(key="token", value=f"{token}",httponly=True,secure=True)
        return {"access_token": token, "token_tyoe": "bearer"}, response


@app.post("/about_me")
def about_me(current_user: str = Depends(get_user_from_token)):
    if current_user is None:
        raise HTTPException(status_code=401)
    user = fakedb.DB_Users.search_user_from_username(current_user)
    logger.info(f"{user}")
    if user:
        return user

@app.post("/register")
@limiter.limit("1/minute")
def register(request: Request,reg_user: RegUserInDb):
    if (reg_user.username):
        raise HTTPException(status_code=409, detail="Пользователь с таким именем уже существует")
    reg_user.password = hash_password(reg_user.password)
    fakedb.DB_Users.create_new_user(reg_user)
    return {"message": f"Успешная регистрация; {reg_user.password}"}

@app.get("/dump_db")
def dump():
    pass

@app.get("/protected_resource")
@PermissionChecker(["admin"])
def protected_resource(token = Cookie()):
    return {"message": "Молодец, ты админ!"}
