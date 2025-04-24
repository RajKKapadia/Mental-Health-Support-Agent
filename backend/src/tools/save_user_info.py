from typing import Dict
import json

from agents import FunctionTool, RunContextWrapper
from pydantic import BaseModel, Field

from src.schemas.user import UserInfo
from src import logging

logger = logging.getLogger(__name__)


class SaveUserInfoToolInput(BaseModel):
    name: str = Field(description="Name of user")
    age: str = Field(description="Age of the user")
    gender: str = Field(
        description="Gender of the user", examples=["Male", "Female", "Other"]
    )


async def save_user_info(
    ctx: RunContextWrapper[UserInfo], args: SaveUserInfoToolInput
) -> Dict[str, str]:
    """TODO
    [ ] Add actual database call here"""
    logger.info("In save user info...")
    logger.info(ctx)
    logger.info(args)
    logger.info(SaveUserInfoToolInput.model_validate_json(args))
    return json.dumps(
        {
            "status": "Success",
            "message": f"A callback request registered successfully for {ctx.context.name}.",
        }
    )


async def run_save_user_info(ctx: RunContextWrapper[UserInfo], args: str) -> str:
    parsed_args = SaveUserInfoToolInput.model_validate_json(args)
    return await save_user_info(ctx=ctx, args=parsed_args)


SaveUserInfoTool = FunctionTool(
    name="save_user_info",
    description="Save user information in database.",
    params_json_schema=SaveUserInfoToolInput.model_json_schema(),
    on_invoke_tool=run_save_user_info,
    strict_json_schema=False,
)
