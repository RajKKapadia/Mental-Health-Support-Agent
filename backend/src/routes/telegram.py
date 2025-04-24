from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from agents import (
    Agent,
    OpenAIResponsesModel,
    Runner,
    AsyncOpenAI,
    WebSearchTool,
)
import httpx
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_db
from src.models.user import User
from src.models.message import Message
from src.schemas.agent import ChatHistory
from src.schemas.user import UserInfo
from src import config
from src.tools.current_date_tool import fetch_current_date_time
from src.tools.save_callback_request import SaveCallbackRequestTool
from src.tools.save_user_info import SaveUserInfoTool
from src.utils.guard_rail import GaurdrailCheckOutput, guardrail_agent
from src import logging


router = APIRouter(prefix=f"/api/{config.API_VERSION}/telegram", tags=["TELEGRAM"])

logger = logging.getLogger(__name__)


TELEGRAM_API_BASE = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}"


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

    # We only care about text messages
    @property
    def has_text_message(self) -> bool:
        return self.message is not None and hasattr(self.message, "text")


async def send_telegram_message(chat_id: int, text: str):
    async with httpx.AsyncClient() as client:
        payload = {"chat_id": chat_id, "text": text, "parse_mode": "MarkdownV2"}
        await client.post(f"{TELEGRAM_API_BASE}/sendMessage", data=payload)


def escape_markdown_v2(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    for char in escape_chars:
        text = text.replace(char, f"\\{char}")
    return text


@router.post("/set-webhook", response_model=WebhookResponse)
async def set_webhook(webhook_data: SetWebhookRequest):
    """Set webhook URL for the Telegram bot"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TELEGRAM_API_BASE}/setWebhook", params={"url": str(webhook_data.url)}
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
    background_tasks: BackgroundTasks,
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
        "**Click here to register**: [Link](https://localhost:3000/register?chat_id={chat_id}). "
        "Once you're done, come back and start chatting with the bot! 💬✨"
    )

    if db_user:
        if db_user.is_verified:
            formatted_chat_history.append(
                {"role": "system", "content": config.SYSTEM_PROMPT}
            )
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
            # Process the message in the background
            background_tasks.add_task(
                handle_text_message,
                chat_id=chat_id,
                text=text,
                formatted_chat_history=formatted_chat_history,
                db=db,
                first_name=first_name,
            )
        else:
            await send_telegram_message(
                chat_id=chat_id,
                text=escape_markdown_v2(
                    text=raw_verify_message.format(chat_id=chat_id)
                ),
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
            text=escape_markdown_v2(text=raw_verify_message.format(chat_id=chat_id)),
        )

    return {"status": "processing"}


"""Agent"""
mental_health_support_agent = Agent[UserInfo](
    name="Mental Health Support Agent",
    tools=[
        fetch_current_date_time,
        SaveCallbackRequestTool,
        WebSearchTool(
            user_location={
                "country": "IN",
                "timezone": "Asia/Kolkata",
                "type": "approximate",
            },
            search_context_size="high",
        ),
        SaveUserInfoTool,
    ],
    model=OpenAIResponsesModel(
        model=config.OPENAI_AGENT_MODEL,
        openai_client=AsyncOpenAI(api_key=config.OPENAI_API_KEY),
    ),
    instructions=config.SYSTEM_PROMPT,
)

client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)


async def handle_text_message(
    chat_id: int,
    text: str,
    formatted_chat_history: List[ChatHistory],
    db: AsyncSession,
    first_name: str,
):
    """Handle the received text message"""
    try:
        guardrail_check = await Runner.run(
            starting_agent=guardrail_agent, input=formatted_chat_history
        )

        input_tokens = 0
        output_tokens = 0
        total_tokens = 0

        for item in guardrail_check.raw_responses:
            input_tokens += item.usage.input_tokens
            output_tokens += item.usage.output_tokens
            total_tokens += item.usage.total_tokens

        guardrail_reault = guardrail_check.final_output_as(GaurdrailCheckOutput)

        response = ""

        if guardrail_reault.is_mental_health:
            user_info = UserInfo(
                age=40, gender="Male", chat_id=str(chat_id), name=first_name
            )

            result = await Runner.run(
                starting_agent=mental_health_support_agent,
                input=formatted_chat_history,
                context=user_info,
            )

            response = result.final_output
            for item in result.raw_responses:
                input_tokens += item.usage.input_tokens
                output_tokens += item.usage.output_tokens
                total_tokens += item.usage.total_tokens
        else:
            completion = await client.responses.create(
                model=config.OPENAI_AGENT_MODEL,
                input=[
                    {
                        "role": "user",
                        "content": f"""You are a helpful assistant, polietly say that you can't answer user's query: {text} 
                        because of {guardrail_reault.reasoning}. Ask user to stick to mental health being questions.""",
                    },
                ],
            )
            response += completion.output_text
            input_tokens += completion.usage.input_tokens
            output_tokens += completion.usage.output_tokens
            total_tokens += completion.usage.total_tokens

        await send_telegram_message(chat_id, escape_markdown_v2(text=response))

        message_create = Message(
            query=text,
            response=response,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            model=config.OPENAI_AGENT_MODEL,
            provider="Openai",
            chat_id=str(chat_id),
        )

        db.add(message_create)
        await db.commit()

        # Typing indicator is automatically turned off when the message is sent
    except Exception as e:
        # If there's an error, try to notify the user
        error_message = (
            f"Sorry, I encountered an error processing your message: {str(e)}"
        )
        try:
            await send_telegram_message(chat_id, escape_markdown_v2(error_message))
        except Exception as e:
            # If we can't even send the error message, just log it
            logger.info(f"Failed to process message and notify user. Error: {str(e)}")
