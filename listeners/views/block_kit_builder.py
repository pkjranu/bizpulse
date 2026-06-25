def build_bizpulse_response(response_text: str) -> list:
    """Convert plain text response to rich Block Kit blocks."""
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": response_text
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "🤖 _BizPulse AI_ | 📊 _Live Salesforce CRM Data_ | ⚡ _Powered by Gemini AI_"
                }
            ]
        }
    ]
    return blocks