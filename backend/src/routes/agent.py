import json
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from agents import (
    ItemHelpers,
    Runner,
    AsyncOpenAI,
)
from openai.types.responses import ResponseTextDeltaEvent

from src.schemas.agent import AgentChatRequest, ChatHistory
from src import config
from src.agents.menatl_health_support import mental_health_support_agent
from src.agents.guard_rail import GuardrailCheckOutput, guardrail_agent
from src.utils.utils import verify_api_key
from src.prompts.prompts import GUARDRAIL_FALSE_PROMPT
from src import logging


router = APIRouter(prefix=f"/api/{config.API_VERSION}/agent", tags=["AGENT"])

logger = logging.getLogger(__name__)


client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)


def format_chat_history(
    agent_chat_request: AgentChatRequest,
) -> List[ChatHistory]:
    formatted_messages = []
    for ch in agent_chat_request.chat_history:
        formatted_messages.append({"role": "user", "content": ch.query})
        formatted_messages.append({"role": "assistant", "content": ch.response})
    formatted_messages.append({"role": "user", "content": agent_chat_request.query})
    return formatted_messages


@router.post("/chat", response_model=None)
async def post_chat(
    agent_chat_request: AgentChatRequest, is_varified: bool = Depends(verify_api_key)
):
    formatted_chat_history = format_chat_history(agent_chat_request=agent_chat_request)

    async def generate():
        input_checks = await Runner.run(
            starting_agent=guardrail_agent, input=formatted_chat_history
        )

        input_tokens = 0
        output_tokens = 0
        total_tokens = 0

        for item in input_checks.raw_responses:
            input_tokens += item.usage.input_tokens
            output_tokens += item.usage.output_tokens
            total_tokens += item.usage.total_tokens

        final_output = input_checks.final_output_as(GuardrailCheckOutput)

        if final_output.is_mental_health:
            result = Runner.run_streamed(
                starting_agent=mental_health_support_agent, input=formatted_chat_history
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
                        if event.item.raw_item.type == "function_call":
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
            completion = await client.responses.create(
                model=config.OPENAI_AGENT_MODEL,
                input=[
                    {
                        "role": "user",
                        "content": GUARDRAIL_FALSE_PROMPT.format(
                            **{
                                "reasoning": final_output.reasoning,
                                "query": agent_chat_request.query,
                            }
                        ),
                    },
                ],
                stream=True,
            )
            async for chunk in completion:
                if chunk.type == "response.output_text.delta":
                    yield (
                        json.dumps(
                            {
                                "type": "answer",
                                "content": chunk.delta,
                            }
                        )
                        + "\n"
                    )
                elif chunk.type == "response.completed":
                    input_tokens += chunk.response.usage.input_tokens
                    output_tokens += chunk.response.usage.output_tokens
                    total_tokens += chunk.response.usage.total_tokens

        yield (
            json.dumps(
                {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens,
                }
            )
            + "\n"
        )

    return StreamingResponse(generate(), media_type="application/json")
