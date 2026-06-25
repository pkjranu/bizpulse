from logging import Logger
from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.context.say.async_say import AsyncSay
from slack_sdk.web.async_client import AsyncWebClient
from agent import run_agent
from listeners.views.block_kit_builder import build_bizpulse_response

async def handle_bizpulse_command(
    ack,
    body: dict,
    context: AsyncBoltContext,
    client: AsyncWebClient,
    say: AsyncSay,
    logger: Logger,
):
    # Acknowledge immediately within 3 seconds
    await ack("_Analyzing your question..._")
    
    text = body.get("text", "").strip()
    
    if not text:
        await say(
            "Hi! Ask me anything about your business data.\n"
            "Example: `/bizpulse what are my top deals?`"
        )
        return

    try:
        response_text, _ = await run_agent(text)
        await say(
            text=response_text,
            blocks=build_bizpulse_response(response_text),
        )
    except Exception as e:
        logger.exception(f"Slash command error: {e}")
        await say(":warning: I'm a bit busy right now. Please try again in a moment!")