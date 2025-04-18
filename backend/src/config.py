import os

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel
from agents import set_tracing_disabled

set_tracing_disabled(disabled=True)

load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERVER_API_KEY = os.getenv("SERVER_API_KEY")

API_VERSION = "v0"

OPENAI_AGENT_MODEL = "gpt-4o"
OPENAI_GUARDRAIL_MODEL = "gpt-4o-mini"

ERROR_MESSAGE = "We are facing an issue, please try after sometimes."


class UserInfo(BaseModel):
    name: str
    uid: str
