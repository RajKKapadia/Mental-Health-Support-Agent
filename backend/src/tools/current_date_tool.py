from datetime import datetime, timezone

from agents import function_tool


@function_tool
async def fetch_current_date_time() -> str:
    """Fetch the today's date and time"""
    now = datetime.now(tz=timezone.utc)
    return now.strftime("%c")
