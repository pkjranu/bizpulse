from logging import Logger
from slack_bolt.context.async_context import AsyncBoltContext
from slack_bolt.context.say.async_say import AsyncSay
from slack_sdk.web.async_client import AsyncWebClient
from agent import run_agent
from listeners.views.block_kit_builder import build_bizpulse_response
from chart_uploader import upload_chart_to_slack


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
        response_text, _, chart_bytes, chart_filename = await run_agent(text)

        await say(
            text=response_text,
            blocks=build_bizpulse_response(response_text),
        )

        if chart_bytes and chart_filename:
            await upload_chart_to_slack(
                client=client,
                channel_id=body["channel_id"],
                chart_bytes=chart_bytes,
                filename=chart_filename,
                title="📊 BizPulse Chart",
            )

    except Exception as e:
        logger.exception(f"Slash command error: {e}")
        await say(":warning: I'm a bit busy right now. Please try again in a moment!")