from typing import Dict
import json

from agents import FunctionTool, RunContextWrapper
from pydantic import BaseModel, Field

from src.models.schemas import UserInfo


class SaveCallbackToolInput(BaseModel):
    name: str = Field(description="Name of user")
    mobile: str = Field(description="Mobile number of the user")
    email: str = Field(description="Email address of the user")


async def save_callback_request(
    ctx: RunContextWrapper[UserInfo], args: SaveCallbackToolInput
) -> Dict[str, str]:
    """TODO
    [ ] Add actual database call here"""
    return json.dumps(
        {
            "status": "Success",
            "message": "User callback request registered successfully.",
        }
    )


async def run_save_callback_request(ctx: RunContextWrapper[UserInfo], args: str) -> str:
    parsed_args = SaveCallbackToolInput.model_validate_json(args)
    return await save_callback_request(ctx=ctx, args=parsed_args)


SaveCallbackRequestTool = FunctionTool(
    name="save_callback_request",
    description="Fetch the table availability at the restaurant via API call.",
    params_json_schema=SaveCallbackToolInput.model_json_schema(),
    on_invoke_tool=run_save_callback_request,
    strict_json_schema=False,
)
