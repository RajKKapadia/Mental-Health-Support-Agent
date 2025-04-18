from typing import List

from pydantic import BaseModel


class HealthResponse(BaseModel):
    message: str


class ChatHistory(BaseModel):
    query: str
    response: str


class AgentChatRequest(BaseModel):
    query: str
    chat_history: List[ChatHistory] = []
    user_id: str


class AgentChatResponse(BaseModel):
    response: str


class UserInfo(BaseModel):
    name: str = "User"
    user_id: str
    age: int
    gender: str
