from typing import List

from agents import Runner
from celery import Celery
from sqlalchemy import select

from src.prompts.prompts import GUARDRAIL_FALSE_PROMPT
from src.schemas.user import UserInfo
from src.utils.telegram import send_telegram_message_sync
from src.schemas.agent import ChatHistory
from src.agents.guard_rail import GuardrailCheckOutput, guardrail_agent
from src.agents.menatl_health_support import mental_health_support_agent
from src.models.message import Message
from src.database.database import SessionLocal
from src.models.user import User
from src import config
from src import logging

celery_app = Celery(main="send_tg_message", broker="pyamqp://guest:guest@localhost//")

logger = logging.getLogger(__name__)


@celery_app.task
def handle_tg_message(
    chat_id: int,
    text: str,
    formatted_chat_history: List[ChatHistory],
):
    logger.info("Running handle_tg_message function")
    try:
        guardrail_check = Runner.run_sync(
            starting_agent=guardrail_agent, input=formatted_chat_history
        )

        input_tokens = 0
        output_tokens = 0
        total_tokens = 0

        for item in guardrail_check.raw_responses:
            input_tokens += item.usage.input_tokens
            output_tokens += item.usage.output_tokens
            total_tokens += item.usage.total_tokens

        guardrail_reault = guardrail_check.final_output_as(GuardrailCheckOutput)

        response = ""

        if guardrail_reault.is_mental_health:
            with SessionLocal() as session:
                session.begin()
                result = session.execute(
                    statement=select(User).filter(User.chat_id == str(chat_id))
                )
                db_user = result.scalars().first()

            user_info = UserInfo(
                age=db_user.age,
                gender=db_user.gender,
                chat_id=str(chat_id),
                name=db_user.first_name,
            )

            result = Runner.run_sync(
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
            completion = config.OPENAI_SYNC_CLIENT.responses.create(
                model=config.OPENAI_AGENT_MODEL,
                input=[
                    {
                        "role": "user",
                        "content": GUARDRAIL_FALSE_PROMPT.format(
                            **{
                                "reasoning": guardrail_reault.reasoning,
                                "query": text,
                            }
                        ),
                    },
                ],
            )
            response += completion.output_text
            input_tokens += completion.usage.input_tokens
            output_tokens += completion.usage.output_tokens
            total_tokens += completion.usage.total_tokens

        send_telegram_message_sync(chat_id, response)

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
        with SessionLocal() as session:
            session.begin()
            try:
                session.add(message_create)
            except Exception as e:
                logger.info(f"Exception saving message: {e}")
                session.rollback()
            else:
                session.commit()
    except Exception as e:
        logger.info(f"First error at handle_tg_message: {str(e)}")
        try:
            send_telegram_message_sync(chat_id, config.ERROR_MESSAGE)
        except Exception as e:
            logger.info(
                f"Failed to process message and notify user. handle_tg_message: {str(e)}"
            )
