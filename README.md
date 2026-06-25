# 📊 BizPulse — AI Business Intelligence Agent for Slack

> Ask your business anything in Slack — get real-time insights from Salesforce CRM instantly.

Built for the **Slack Agent Builder Challenge 2026**

---

## 🚀 What is BizPulse?

BizPulse is an AI-powered business intelligence agent that lives inside Slack. Ask any business question in plain English and get instant answers, insights, and recommendations — powered by live Salesforce CRM data.

**No dashboards. No exports. No context switching. Just ask.**

---

## ✨ Features

- 💬 **Natural language queries** — Ask anything about your business data
- 📊 **Live Salesforce data** — Real-time Opportunities, Accounts, Cases
- 🤖 **AI recommendations** — Actionable insights with every answer
- ⚡ **3 ways to interact** — DM, `/bizpulse` slash command, or `@Bizpulse` mention
- 🎯 **Suggested prompts** — One-click questions to get started
- 🏠 **Rich Agent Home** — Beautiful Block Kit UI

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Slack Bolt Python | Core agent framework |
| Slack AI Agent Builder | Required technology ✅ |
| Slack MCP Server | Required technology ✅ |
| Salesforce CRM (OAuth 2.0) | Live business data |
| Google Gemini 2.5 Flash | AI intelligence layer |
| Block Kit | Rich Slack UI |

---

## 📸 Demo

> Try asking BizPulse:
> - *"What are my top deals by value?"*
> - *"Which accounts need follow-up?"*
> - *"What is our total pipeline value?"*
> - *"Which cases are high priority?"*

---

## 🏗️ Architecture

```
User asks in Slack
      ↓
BizPulse Bolt Python Agent (Socket Mode)
      ↓
Salesforce OAuth 2.0 → Live CRM Data
      ↓
Gemini 2.5 Flash AI → Analyzes + Recommends
      ↓
Block Kit Response in Slack
```

---

## ⚙️ Setup

### Prerequisites
- Python 3.12+
- Slack Developer Sandbox
- Salesforce Developer Account
- Google Gemini API Key

### Installation

```bash
git clone https://github.com/pkjranu/bizpulse.git
cd bizpulse
py -3.12 -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

### Environment Variables

Copy `.env.sample` to `.env` and fill in:

```
GEMINI_API_KEY=your_gemini_api_key
SLACK_APP_TOKEN=xapp-your-app-token
SLACK_BOT_TOKEN=xoxb-your-bot-token
SF_CONSUMER_KEY=your_salesforce_consumer_key
SF_CONSUMER_SECRET=your_salesforce_consumer_secret
SF_INSTANCE_URL=https://your-org.my.salesforce.com
```

### Run

```bash
.venv\Scripts\python.exe app.py
```

---

## 🏆 Hackathon

Built for the **Slack Agent Builder Challenge 2026**
Track: **New Slack Agent**
Prize Target: **$8,000 First Place**

---

## 👨‍💻 Author

Built with ❤️ by Praveen Jain