def build_app_home_view(
    install_url: str | None = None, is_connected: bool = False
) -> dict:
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "📊 Welcome to BizPulse!",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Your AI-powered business intelligence assistant.*\nAsk anything about your Salesforce CRM data — deals, accounts, cases, and more — right here in Slack.",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*🚀 Try these questions:*",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "• What are my top deals by value?\n• Which accounts need follow-up?\n• Show me open opportunities this month\n• What is our total pipeline value?\n• Which cases are high priority?",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*💡 How to use BizPulse:*\n1️⃣ Click *Chat* tab above and ask any business question\n2️⃣ Use */bizpulse [question]* in any channel\n3️⃣ Mention *@Bizpulse* in a channel",
            },
        },
        {"type": "divider"},
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "🟢 *Connected to Salesforce CRM* | Powered by Gemini AI | Built for Slack Agent Builder Challenge",
                }
            ],
        },
    ]
    return {
        "type": "home",
        "blocks": blocks,
    }