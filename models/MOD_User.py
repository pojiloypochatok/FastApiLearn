from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class UserBase():
    username: str

class UserInDB(UserBase):
    hashed_password: str

class RegUserInDb(BaseModel):
    username: str
    password: str



