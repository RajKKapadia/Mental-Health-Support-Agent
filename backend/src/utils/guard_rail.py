from agents import (
    Agent,
    OpenAIResponsesModel,
    AsyncOpenAI,
)
from pydantic import BaseModel

from src import config


class GaurdrailCheckOutput(BaseModel):
    is_mental_health: bool
    reasoning: str


guardrail_agent = Agent(
    name="Gaurdrail Check",
    instructions="Check if the user is asking about mental health, well being, greetings, good byes and request callbacks.",
    output_type=GaurdrailCheckOutput,
    model=OpenAIResponsesModel(
        model=config.OPENAI_GUARDRAIL_MODEL,
        openai_client=AsyncOpenAI(api_key=config.OPENAI_API_KEY),
    ),
)
