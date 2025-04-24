from datetime import datetime
from typing import Literal

from sqlalchemy import Column, DateTime, String, Boolean, Integer, Text, ForeignKey

from src.models.base import generate_uuid
from src.models.base import Base


Provider = Literal["Openai"]


class Message(Base):
    __tablename__ = "messages"

    id = Column(String(512), primary_key=True, default=generate_uuid, index=True)
    query = Column(Text)
    response = Column(Text)
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    total_tokens = Column(Integer)
    model = Column(String(64), index=True)
    provider = Column(String(64))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )

    chat_id = Column(String(512), ForeignKey("users.chat_id"))

    def __repr__(self) -> str:
        return f"Message id: {self.id} Chat: {self.chat_id}"
