from fastapi import APIRouter, Depends, HTTPException
import httpx
from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

from src.tasks.tasks import handle_tg_message
from src.utils.telegram import send_telegram_message
from src.database.database import get_db
from src.models.user import User
from src.models.message import Message
from src import config
from src.schemas.telegram import WebhookResponse, SetWebhookRequest, Update
from src import logging
from src.prompts.prompts import SYSTEM_PROMPT


router = APIRouter(prefix=f"/api/{config.API_VERSION}/telegram", tags=["TELEGRAM"])

logger = logging.getLogger(__name__)


@router.post("/set-webhook", response_model=WebhookResponse)
async def set_webhook(webhook_data: SetWebhookRequest):
    """Set webhook URL for the Telegram bot"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{config.TELEGRAM_API_BASE}/setWebhook",
            params={"url": str(webhook_data.url)},
        )
        data = response.json()
        if not data.get("ok"):
            raise HTTPException(
                status_code=400, detail=data.get("description", "Failed to set webhook")
            )
        return data


@router.post("/webhook")
async def telegram_webhook(
    update: Update,
    db: AsyncSession = Depends(get_db),
):
    """Receive updates from Telegram"""
    if not update.has_text_message:
        # Ignore non-text messages
        return {"status": "ignored"}

    # Process text message
    text = update.message.text
    chat_id = update.message.chat.id
    first_name = update.message.from_user.first_name

    result = await db.execute(
        statement=select(User).filter(User.chat_id == str(chat_id))
    )

    db_user = result.scalars().first()

    formatted_chat_history = []

    raw_verify_message = (
        "To get started and unlock all the features, you need to **register** first 📝 👉 "
        f"**Click here to register**: [Link]({config.FRONTEND_URL}/register?chatId={chat_id}). "
        "Once you're done, come back and start chatting with the bot! 💬✨"
    )

    if db_user:
        if db_user.is_verified:
            formatted_chat_history.append({"role": "system", "content": SYSTEM_PROMPT})
            result = await db.execute(
                statement=select(Message)
                .filter(Message.chat_id == str(chat_id), Message.is_deleted.is_(False))
                .order_by(asc(Message.created_at))
                .limit(8)
            )
            db_messages = result.scalars().all()
            for message in db_messages:
                formatted_chat_history.append(
                    {"role": "user", "content": message.query}
                )
                formatted_chat_history.append(
                    {"role": "assistant", "content": message.response}
                )
            formatted_chat_history.append({"role": "user", "content": text})

            handle_tg_message.delay(
                chat_id=chat_id,
                text=text,
                formatted_chat_history=formatted_chat_history,
            )
        else:
            await send_telegram_message(
                chat_id=chat_id,
                text=raw_verify_message.format(chat_id=chat_id),
            )
    else:
        user_create = User(
            first_name=first_name,
            chat_id=str(chat_id),
            channel="Telegram",
            last_name="",
        )
        db.add(user_create)
        await db.commit()
        await send_telegram_message(
            chat_id=chat_id,
            text=raw_verify_message.format(chat_id=chat_id),
        )

    return {"status": "processing"}
