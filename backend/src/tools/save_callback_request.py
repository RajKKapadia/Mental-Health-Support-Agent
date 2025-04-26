from typing import Dict
import json

from agents import FunctionTool, RunContextWrapper
from pydantic import BaseModel, Field

from src.schemas.user import UserInfo
from src import logging

logger = logging.getLogger(__name__)


class SaveCallbackToolInput(BaseModel):
    mobile: str = Field(description="Mobile number of the user")


async def save_callback_request(
    ctx: RunContextWrapper[UserInfo], args: SaveCallbackToolInput
) -> Dict[str, str]:
    """TODO
    [ ] Add actual database call here"""
    logger.info(ctx)
    logger.info(args)
    logger.info(SaveCallbackToolInput.model_validate(args))
    return json.dumps(
        {
            "status": "Success",
            "message": f"A callback request registered successfully for {ctx.context.name}.",
        }
    )


async def run_save_callback_request(ctx: RunContextWrapper[UserInfo], args: str) -> str:
    parsed_args = SaveCallbackToolInput.model_validate_json(args)
    return await save_callback_request(ctx=ctx, args=parsed_args)


SaveCallbackRequestTool = FunctionTool(
    name="register_callback_request",
    description="Register a callback request for consultation, mental support, help ease the pain.",
    params_json_schema=SaveCallbackToolInput.model_json_schema(),
    on_invoke_tool=run_save_callback_request,
    strict_json_schema=False,
)
