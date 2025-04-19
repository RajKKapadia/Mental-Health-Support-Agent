import json
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from agents import (
    Agent,
    ItemHelpers,
    OpenAIResponsesModel,
    Runner,
    AsyncOpenAI,
)
from openai.types.responses import ResponseTextDeltaEvent
from openai import OpenAI

from src.models.schemas import AgentChatRequest, ChatHistory, UserInfo
from src import config
from src.tools.current_date_tool import fetch_current_date_time
from src.tools.save_callback_request import SaveCallbackRequestTool
from src.utils.guard_rail import GaurdrailCheckOutput, guardrail_agent
from src.utils.utils import verify_api_key
from src import logging


router = APIRouter(prefix=f"/api/{config.API_VERSION}/agent", tags=["AGENT"])

logger = logging.getLogger(__name__)


client = OpenAI(api_key=config.OPENAI_API_KEY)


def format_chat_history(
    agent_chat_request: AgentChatRequest,
) -> List[ChatHistory]:
    formatted_messages = []
    for ch in agent_chat_request.chat_history:
        formatted_messages.append({"role": "user", "content": ch.query})
        formatted_messages.append({"role": "assistant", "content": ch.response})
    formatted_messages.append({"role": "user", "content": agent_chat_request.query})
    return formatted_messages


"""Agent"""
table_booking_agent = Agent[UserInfo](
    name="Mental Health Support Agent",
    tools=[
        fetch_current_date_time,
        SaveCallbackRequestTool,
    ],
    model=OpenAIResponsesModel(
        model=config.OPENAI_AGENT_MODEL,
        openai_client=AsyncOpenAI(api_key=config.OPENAI_API_KEY),
    ),
    instructions=config.SYSTEM_PROMPT,
)


@router.post("/chat", response_model=None)
async def post_chat(
    agent_chat_request: AgentChatRequest, is_varified: bool = Depends(verify_api_key)
):
    formatted_chat_history = format_chat_history(agent_chat_request=agent_chat_request)

    async def generate():
        input_checks = await Runner.run(
            starting_agent=guardrail_agent, input=formatted_chat_history
        )

        final_output = input_checks.final_output_as(GaurdrailCheckOutput)

        if final_output.is_mental_health:
            result = Runner.run_streamed(
                starting_agent=table_booking_agent, input=formatted_chat_history
            )

            async for event in result.stream_events():
                """We'll ignore the raw responses event deltas
                If you want to stream the information use this."""

                # When you receive delta of the final answer
                if event.type == "raw_response_event" and isinstance(
                    event.data, ResponseTextDeltaEvent
                ):
                    yield (
                        json.dumps({"type": "answer", "content": event.data.delta})
                        + "\n"
                    )

                # When the agent updates
                elif event.type == "agent_updated_stream_event":
                    continue

                # When items are generated
                elif event.type == "run_item_stream_event":
                    if event.item.type == "tool_call_item":
                        yield (
                            json.dumps(
                                {
                                    "type": "tool_name",
                                    "content": event.item.raw_item.name,
                                }
                            )
                            + "\n"
                        )
                        yield (
                            json.dumps(
                                {
                                    "type": "tool_args",
                                    "content": event.item.raw_item.arguments,
                                }
                            )
                            + "\n"
                        )
                    elif event.item.type == "tool_call_output_item":
                        yield (
                            json.dumps(
                                {"type": "tool_content", "content": event.item.output}
                            )
                            + "\n"
                        )
                    # When final answer
                    elif event.item.type == "message_output_item":
                        yield (
                            json.dumps(
                                {
                                    "type": "final_answer",
                                    "content": ItemHelpers.text_message_output(
                                        event.item
                                    ),
                                }
                            )
                            + "\n"
                        )
                    else:
                        # Ignore other event types
                        pass
        else:
            completion = client.chat.completions.create(
                model=config.OPENAI_AGENT_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": f"""You are a helpful assistant, polietly say that you can't answer user's query: {agent_chat_request.query} 
                        because of {final_output.reasoning}. Ask user to stick to mental health being questions.""",
                    },
                ],
                stream=True,
            )
            for chunk in completion:
                if (
                    chunk.choices[0].delta.content is not None
                    and chunk.choices[0].delta.content != ""
                ):
                    yield (
                        json.dumps(
                            {
                                "type": "answer",
                                "content": chunk.choices[0].delta.content,
                            }
                        )
                        + "\n"
                    )

    return StreamingResponse(generate(), media_type="application/json")
