from logging import Logger
from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.context.say.async_say import AsyncSay
from slack_sdk.web.async_client import AsyncWebClient
from agent import AgentDeps, run_agent
from listeners.views.block_kit_builder import build_bizpulse_response

async def handle_message(
    client: AsyncWebClient,
    context: AsyncBoltContext,
    event: dict,
    logger: Logger,
    say: AsyncSay,
):
    """Handle messages sent to the agent via DM."""
    if event.get("subtype"):
        return
    if event.get("bot_id"):
        return

    is_dm = event.get("channel_type") == "im"
    if not is_dm:
        return

    try:
        text = event.get("text", "")
        thread_ts = event.get("thread_ts") or event["ts"]
        user_id = context.user_id
        channel_id = context.channel_id

        deps = AgentDeps(
            client=client,
            user_id=user_id,
            channel_id=channel_id,
            thread_ts=thread_ts,
            message_ts=event["ts"],
            user_token=context.user_token,
        )

        response_text, _ = await run_agent(text, deps=deps)

        await say(
            text=response_text,
            blocks=build_bizpulse_response(response_text),
            thread_ts=thread_ts,
        )

    except Exception as e:
        logger.exception(f"Failed to handle message: {e}")
        await say(
            text=":warning: I'm a bit busy right now. Please try again in a moment!",
            thread_ts=event.get("thread_ts") or event.get("ts"),
        )