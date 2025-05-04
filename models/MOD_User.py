from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    role: list

class RegUserInDb(BaseModel):
    username: str
    password: str
    role: list





