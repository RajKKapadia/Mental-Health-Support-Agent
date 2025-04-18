from random import random

from agents import RunContextWrapper, FunctionTool
from pydantic import BaseModel, Field

from src.config import UserInfo


class JoinWaitlistToolInput(BaseModel):
    restaurant_name: str = Field(description="Name of the restaurant to join waitlist")
    date: str = Field(description="Desired date, format dd/mm/yyyy")
    time: str = Field(description="Desired time, format hh:mm")
    number_of_person: int = Field(description="Number of people in the party")
    customer_name: str = Field(description="Name of the customer joining waitlist")
    customer_phone: str = Field(description="Contact phone number for notifications")


async def join_waitlist(
    ctx: RunContextWrapper[UserInfo], args: JoinWaitlistToolInput
) -> str:
    """Add a customer to the waiting list for a restaurant"""
    # In a real implementation, this would call an API to add to waitlist
    waitlist_position = int(random() * 10) + 1
    return f"""Added {args.customer_name} to the waitlist for {args.restaurant_name} on {args.date} at {args.time}. You are currently position #{waitlist_position} on 
    the waitlist. We'll contact you at {args.customer_phone} if a table becomes available."""


async def run_join_waitlist(ctx: RunContextWrapper[UserInfo], args: str) -> str:
    """Validate and run the join waitlist function"""
    parsed_args = JoinWaitlistToolInput.model_validate_json(args)
    return await join_waitlist(ctx=ctx, args=parsed_args)


JoinWaitlistTool = FunctionTool(
    name="join_waitlist",
    description="Add a customer to the waiting list for a restaurant.",
    params_json_schema=JoinWaitlistToolInput.model_json_schema(),
    on_invoke_tool=run_join_waitlist,
    strict_json_schema=False,
)
