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
    instructions="""Check if the user is asking about one the following things:
    (1) General greetings and good bye messages
    (2) mental health and well being advice or conversations
    (3) books about mental health, well being and meditation
    (4) excercises about mental health, well being and meditation
    (5) User can request a callback in case of needs""",
    output_type=GaurdrailCheckOutput,
    model=OpenAIResponsesModel(
        model=config.OPENAI_GUARDRAIL_MODEL,
        openai_client=AsyncOpenAI(api_key=config.OPENAI_API_KEY),
    ),
)
