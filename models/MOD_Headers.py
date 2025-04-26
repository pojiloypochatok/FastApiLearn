from pydantic import BaseModel
from fastapi import Header


class CommonHeaders(BaseModel):
    user_agent: str = Header()
    accept_language: str = Header()
