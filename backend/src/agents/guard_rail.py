from agents import (
    Agent,
    OpenAIResponsesModel,
)
from pydantic import BaseModel

from src import config
from src.prompts.prompts import GUARDRAIL_PROMPT


class GuardrailCheckOutput(BaseModel):
    is_mental_health: bool
    reasoning: str


guardrail_agent = Agent(
    name="Gaurdrail Check",
    instructions=GUARDRAIL_PROMPT,
    output_type=GuardrailCheckOutput,
    model=OpenAIResponsesModel(
        model=config.OPENAI_GUARDRAIL_MODEL,
        openai_client=config.OPENAI_ASYNC_CLIENT,
    ),
)
