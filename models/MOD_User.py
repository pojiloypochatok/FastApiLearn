from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    role: str

    model_config = {
        "from_attributes": True
    }






