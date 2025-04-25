from typing import Optional

from pydantic import BaseModel, HttpUrl, Field


class SetWebhookRequest(BaseModel):
    url: HttpUrl = Field(..., description="HTTPS URL to send updates to")


class WebhookResponse(BaseModel):
    ok: bool
    description: str


class TelegramMessageFrom(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None


class TelegramChat(BaseModel):
    id: int
    type: str
    title: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None


class TelegramMessage(BaseModel):
    message_id: int
    from_user: TelegramMessageFrom = Field(..., alias="from")
    chat: TelegramChat
    date: int
    text: str

    class Config:
        populate_by_name = True


class Update(BaseModel):
    update_id: int
    message: Optional[TelegramMessage] = None

    @property
    def has_text_message(self) -> bool:
        return self.message is not None and hasattr(self.message, "text")
