import json
from typing import List

from fastapi import APIRouter
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

from src.models.schemas import AgentChatRequest, ChatHistory
from src import config
from src.tools.current_date_tool import fetch_current_date_time
from src.tools.table_availability_tool import FetchTableAvailabilityTool
from src.tools.save_booking_tool import SaveBookingTool
from src.tools.join_waitlist_tool import JoinWaitlistTool
from src.utils.guard_rail import TableBookingOutput, guardrail_agent


router = APIRouter(prefix=f"/api/{config.API_VERSION}/agent", tags=["AGENT"])


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
table_booking_agent = Agent[config.UserInfo](
    name="Table Booking Agent",
    tools=[
        fetch_current_date_time,
        FetchTableAvailabilityTool,
        SaveBookingTool,
        JoinWaitlistTool,
    ],
    model=OpenAIResponsesModel(
        model=config.OPENAI_AGENT_MODEL,
        openai_client=AsyncOpenAI(api_key=config.OPENAI_API_KEY),
    ),
    instructions="""You are an AI agent to helps users book tables at restaurants and provide information about restraurants.
Never assume any value, try to use the tools otherwise always ask for clarity if the request is ambiguous.""",
)


@router.post("/chat", response_model=None)
async def post_chat(agent_chat_request: AgentChatRequest):
    formatted_chat_history = format_chat_history(agent_chat_request=agent_chat_request)

    async def generate():
        input_checks = await Runner.run(
            starting_agent=guardrail_agent, input=formatted_chat_history
        )

        final_output = input_checks.final_output_as(TableBookingOutput)

        if final_output.is_table_booking:
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
                    yield json.dumps({"type": "answer", "content": event.data.delta})

                # When the agent updates
                elif event.type == "agent_updated_stream_event":
                    continue

                # When items are generated
                elif event.type == "run_item_stream_event":
                    if event.item.type == "tool_call_item":
                        yield json.dumps(
                            {"type": "tool_name", "content": event.item.raw_item.name}
                        )
                        yield json.dumps(
                            {
                                "type": "tool_arguments",
                                "content": event.item.raw_item.arguments,
                            }
                        )
                    elif event.item.type == "tool_call_output_item":
                        yield json.dumps(
                            {"type": "tool_output", "content": event.item.output}
                        )
                    # When final answer
                    elif event.item.type == "message_output_item":
                        yield json.dumps(
                            {
                                "type": "final_answer",
                                "content": ItemHelpers.text_message_output(event.item),
                            }
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
                        "content": f"""You are a helpful assistant, polietly say that you can't answer {agent_chat_request.query} because it is out of scope, you can only answer about 
                restaurant and table booking at a restaurant.""",
                    },
                ],
                stream=True,
            )
            for chunk in completion:
                if (
                    chunk.choices[0].delta.content is not None
                    and chunk.choices[0].delta.content != ""
                ):
                    yield json.dumps(
                        {"type": "answer", "content": chunk.choices[0].delta.content}
                    )

    return StreamingResponse(generate(), media_type="application/json")
