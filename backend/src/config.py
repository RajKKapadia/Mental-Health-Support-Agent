import os

from dotenv import load_dotenv, find_dotenv
from agents import set_tracing_disabled
from openai import AsyncOpenAI, OpenAI

set_tracing_disabled(disabled=True)

load_dotenv(find_dotenv())

# Database setting
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Openai settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERVER_API_KEY = os.getenv("SERVER_API_KEY")

OPENAI_AGENT_MODEL = "gpt-4o-mini"
OPENAI_GUARDRAIL_MODEL = "gpt-4o-mini"

OPENAI_ASYNC_CLIENT = AsyncOpenAI(api_key=OPENAI_API_KEY)
OPENAI_SYNC_CLIENT = OpenAI(api_key=OPENAI_API_KEY)

# Server setting
PORT = int(os.getenv("PORT"))

API_VERSION = "v0"

# Telegram setting
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

ERROR_MESSAGE = "We are facing an issue, please try after sometimes."

if os.getenv("ENVIRONMENT") == "Development":
    FRONTEND_URL = os.getenv("FRONTEND_URL_DEVELOPMENT")
else:
    FRONTEND_URL = os.getenv("FRONTEND_URL_PRODUCTION")
