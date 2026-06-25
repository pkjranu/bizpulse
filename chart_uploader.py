import asyncio
from slack_sdk.web.async_client import AsyncWebClient

async def upload_chart_to_slack(
    client: AsyncWebClient,
    channel_id: str,
    chart_bytes: bytes,
    filename: str,
    title: str,
    thread_ts: str = None
) -> str:
    """Upload a chart image to Slack and return the file URL."""
    try:
        response = await client.files_upload_v2(
            channel=channel_id,
            content=chart_bytes,
            filename=filename,
            title=title,
            thread_ts=thread_ts
        )
        return response.get("file", {}).get("permalink", "")
    except Exception as e:
        print(f"Chart upload error: {e}")
        return ""