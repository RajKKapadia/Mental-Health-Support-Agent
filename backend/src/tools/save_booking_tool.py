from random import random

from agents import FunctionTool, RunContextWrapper
from pydantic import BaseModel, Field

from src.config import UserInfo


class SaveBookingToolInput(BaseModel):
    restaurant_name: str = Field(description="Name of the restaurant to book")
    date: str = Field(description="Reservation date, format dd/mm/yyyy")
    time: str = Field(description="Reservation time, format hh:mm")
    number_of_person: int = Field(
        description="Number of people to book reservation for"
    )
    customer_name: str = Field(description="Name of the customer making the booking")
    customer_phone: str = Field(description="Contact phone number for the booking")


async def save_booking(
    ctx: RunContextWrapper[UserInfo], args: SaveBookingToolInput
) -> str:
    """Save a confirmed booking to the reservation system"""
    # In a real implementation, this would call an API to create the booking
    booking_id = int(random() * 10000)
    return f"""Booking confirmed at {args.restaurant_name} for {args.customer_name} on {args.date} at {args.time} for {args.number_of_person} people. Your booking reference 
    is #{booking_id}."""


async def run_save_booking(ctx: RunContextWrapper[UserInfo], args: str) -> str:
    """Validate and run the save booking function"""
    parsed_args = SaveBookingToolInput.model_validate_json(args)
    return await save_booking(ctx=ctx, args=parsed_args)


SaveBookingTool = FunctionTool(
    name="save_booking",
    description="Save a confirmed booking at a restaurant.",
    params_json_schema=SaveBookingToolInput.model_json_schema(),
    on_invoke_tool=run_save_booking,
    strict_json_schema=False,
)
