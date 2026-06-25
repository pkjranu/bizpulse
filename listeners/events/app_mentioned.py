import re
from logging import Logger
from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.context.say.async_say import AsyncSay
from slack_sdk.web.async_client import AsyncWebClient
from agent import run_agent
from listeners.views.block_kit_builder import build_bizpulse_response

async def handle_app_mentioned(
    client: AsyncWebClient,
    context: AsyncBoltContext,
    event: dict,
    logger: Logger,
    say: AsyncSay,
):
    """Handle @mentions in channels."""
    try:
        channel_id = context.channel_id
        text = event.get("text", "")
        thread_ts = event.get("thread_ts") or event["ts"]

        cleaned_text = re.sub(r"<@[A-Z0-9]+>", "", text).strip()

        if not cleaned_text:
            await say(
                text="Hey there! Ask me anything about your business data!",
                thread_ts=thread_ts,
            )
            return

        response_text, _ = await run_agent(cleaned_text)

        await say(
            text=response_text,
            blocks=build_bizpulse_response(response_text),
            thread_ts=thread_ts,
        )

    except Exception as e:
        logger.exception(f"Failed to handle app mention: {e}")
        await say(
            text=":warning: I'm a bit busy right now. Please try again in a moment!",
            thread_ts=event.get("thread_ts") or event["ts"],
        )