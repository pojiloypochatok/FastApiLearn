import sys
import logging
import jwt
import datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Dict
from passlib.context import CryptContext

logger = logging.getLogger("uvicorn")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

secret_key = "mysupersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_jwt_token(data: Dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    logger.error("токен создан")
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)

def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        logger.error("SignatureError")
        pass
    except jwt.InvalidTokenError:
        logger.error("InvalidTokenError")
        pass

def hash_password(password: str):
    return pwd_context.hash(password)

def check_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

