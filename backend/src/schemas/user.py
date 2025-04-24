from pydantic import BaseModel


class UserInfo(BaseModel):
    name: str = "User"
    chat_id: str
    age: int
    gender: str
