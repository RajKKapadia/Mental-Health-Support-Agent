import json
from typing import List

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import StreamingResponse
from agents import (
    Agent,
    ItemHelpers,
    OpenAIResponsesModel,
    Runner,
    AsyncOpenAI,
    WebSearchTool,
)
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_db
from src.schemas.agent import AgentChatRequest, ChatHistory
from src.models.user import User
from src import config
from src.tools.current_date_tool import fetch_current_date_time
from src.tools.save_callback_request import SaveCallbackRequestTool
from src.utils.guard_rail import GaurdrailCheckOutput, guardrail_agent
from src.utils.utils import verify_api_key
from src import logging


router = APIRouter(prefix=f"/api/{config.API_VERSION}/user", tags=["USER"])

logger = logging.getLogger(__name__)


class RegisterRequest(BaseModel):
    firstName: str
    lastName: str
    email: str
    age: int
    gender: str
    privacyPolicy: bool
    chatId: str


class RegisterResponse(BaseModel):
    status: bool
    message: str


@router.post(
    "/register", response_model=RegisterResponse, status_code=status.HTTP_200_OK
)
async def handle_post_register(
    register_request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
    is_verified: bool = Depends(verify_api_key),
):
    logger.info("Registering a new user")

    result = await db.execute(
        statement=select(User).filter(User.chat_id == register_request.chatId)
    )

    db_user = result.scalars().first()

    if db_user is None:
        logger.info(f"User with the chat id: {register_request.chatId} not found.")
        return RegisterResponse(
            status=False,
            message="User not found, contact the admin of the Telegram Bot.",
        )

    db_user.first_name = register_request.firstName
    db_user.last_name = register_request.lastName
    db_user.email = register_request.email
    db_user.age = register_request.age
    db_user.gender = register_request.gender
    db_user.privacy_policy = register_request.privacyPolicy
    db_user.is_verified = True

    try:
        await db.commit()
        logger.info("User updated successfully.")
        return RegisterResponse(status=True, message="User registration successfull.")
    except Exception as e:
        logger.error(f"User registration facing error: {e}")
        return RegisterResponse(
            status=False, message="Server error, contact the admin of the Telegram Bot."
        )
