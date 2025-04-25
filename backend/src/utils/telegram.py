import httpx

from src import config


async def send_telegram_message(chat_id: int, text: str):
    async with httpx.AsyncClient() as client:
        payload = {
            "chat_id": chat_id,
            "text": escape_markdown_v2(text),
            "parse_mode": "MarkdownV2",
        }
        await client.post(f"{config.TELEGRAM_API_BASE}/sendMessage", data=payload)


def send_telegram_message_sync(chat_id: int, text: str):
    with httpx.Client() as client:
        payload = {
            "chat_id": chat_id,
            "text": escape_markdown_v2(text),
            "parse_mode": "MarkdownV2",
        }
        client.post(f"{config.TELEGRAM_API_BASE}/sendMessage", data=payload)


def escape_markdown_v2(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    for char in escape_chars:
        text = text.replace(char, f"\\{char}")
    return text
