from agents import Agent, OpenAIResponsesModel, WebSearchTool

from src.tools.current_date_tool import fetch_current_date_time
from src.tools.save_callback_request import SaveCallbackRequestTool
from src import config
from src.schemas.user import UserInfo
from src.prompts.prompts import SYSTEM_PROMPT


mental_health_support_agent = Agent[UserInfo](
    name="Mental Health Support Agent",
    tools=[
        fetch_current_date_time,
        SaveCallbackRequestTool,
        WebSearchTool(
            user_location={
                "country": "IN",
                "timezone": "Asia/Kolkata",
                "type": "approximate",
            },
            search_context_size="high",
        ),
    ],
    model=OpenAIResponsesModel(
        model=config.OPENAI_AGENT_MODEL,
        openai_client=config.OPENAI_ASYNC_CLIENT,
    ),
    instructions=SYSTEM_PROMPT,
)
