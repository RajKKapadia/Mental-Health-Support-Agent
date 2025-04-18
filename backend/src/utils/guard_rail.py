from agents import (
    Agent,
    OpenAIResponsesModel,
    AsyncOpenAI,
)
from pydantic import BaseModel

from src import config


class TableBookingOutput(BaseModel):
    is_table_booking: bool
    reasoning: str


guardrail_agent = Agent(
    name="Gaurdrail Check",
    instructions="Check if the user is asking you about restaurant and table booking at a restaurant.",
    output_type=TableBookingOutput,
    model=OpenAIResponsesModel(
        model=config.OPENAI_GUARDRAIL_MODEL,
        openai_client=AsyncOpenAI(api_key=config.OPENAI_API_KEY),
    ),
)
