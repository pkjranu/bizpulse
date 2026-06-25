from logging import Logger
from slack_bolt.context.set_suggested_prompts.async_set_suggested_prompts import (
    AsyncSetSuggestedPrompts,
)

SUGGESTED_PROMPTS = [
    {"title": "Top Deals", "message": "What are my top deals by value?"},
    {"title": "Pipeline Value", "message": "What is our total pipeline value?"},
    {"title": "Accounts Follow-up", "message": "Which accounts need follow-up?"},
    {"title": "High Priority Cases", "message": "Which cases are high priority?"},
]

async def handle_assistant_thread_started(
    set_suggested_prompts: AsyncSetSuggestedPrompts, logger: Logger
):
    """Handle assistant thread started events by setting suggested prompts."""
    try:
        await set_suggested_prompts(
            prompts=SUGGESTED_PROMPTS,
            title="Ask me anything about your Salesforce CRM data 📊",
        )
    except Exception as e:
        logger.exception(f"Failed to handle assistant thread started: {e}")