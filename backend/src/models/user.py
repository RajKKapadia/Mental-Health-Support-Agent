from datetime import datetime
from typing import Literal

from sqlalchemy import Column, DateTime, String, Boolean, Integer

from src.models.base import generate_uuid
from src.models.base import Base


Channels = Literal["Telegram", "WhatsApp", "FBMessenger", "Instagram"]
Gender = Literal["Male", "Female", "Other"]


class User(Base):
    __tablename__ = "users"

    id = Column(String(512), primary_key=True, default=generate_uuid, index=True)
    first_name = Column(String(128))
    chat_id = Column(String(128), unique=True, index=True)
    channel = Column(String(64))
    last_name = Column(String(128), nullable=True)
    privacy_policy = Column(Boolean, default=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(128), nullable=True)
    email = Column(String(128), nullable=True)
    username = Column(String(256), default="")
    is_deleted = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_first_login = Column(Boolean, default=True)
    login_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )

    def __repr__(self) -> str:
        return f"{self.channel} -> {self.user_id}."
