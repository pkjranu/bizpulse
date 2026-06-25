from google import genai
from google.genai import types
import os
import requests
import asyncio
import json
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_sf_token():
    url = "https://nagarro227-dev-ed.develop.my.salesforce.com/services/oauth2/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': os.environ.get('SF_CONSUMER_KEY'),
        'client_secret': os.environ.get('SF_CONSUMER_SECRET'),
    }
    response = requests.post(url, data=payload)
    data = response.json()
    return data.get('access_token'), data.get('instance_url')

def load_business_data():
    try:
        token, instance_url = get_sf_token()
        headers = {'Authorization': f'Bearer {token}'}
        base = f"{instance_url}/services/data/v59.0/query"

        opps = requests.get(base, headers=headers,
            params={'q': 'SELECT Name, Amount, StageName, CloseDate FROM Opportunity LIMIT 20'}).json()

        accounts = requests.get(base, headers=headers,
            params={'q': 'SELECT Name, Industry, AnnualRevenue, BillingCountry FROM Account LIMIT 20'}).json()

        cases = requests.get(base, headers=headers,
            params={'q': 'SELECT Subject, Status, Priority FROM Case LIMIT 20'}).json()

        data = "=== SALESFORCE OPPORTUNITIES ===\n"
        for o in opps.get('records', []):
            data += f"Deal: {o['Name']} | Amount: ${o['Amount']} | Stage: {o['StageName']} | Close: {o['CloseDate']}\n"

        data += "\n=== SALESFORCE ACCOUNTS ===\n"
        for a in accounts.get('records', []):
            data += f"Account: {a['Name']} | Industry: {a['Industry']} | Revenue: ${a['AnnualRevenue']} | Country: {a['BillingCountry']}\n"

        data += "\n=== SALESFORCE CASES ===\n"
        for c in cases.get('records', []):
            data += f"Case: {c['Subject']} | Status: {c['Status']} | Priority: {c['Priority']}\n"

        print("✅ Salesforce data loaded successfully!")
        return data

    except Exception as e:
        print(f"❌ Salesforce error: {e}")
        return "No data available"

SYSTEM_PROMPT_TEMPLATE = """You are BizPulse, an AI-powered business intelligence assistant in Slack.
You have access to live Salesforce CRM data:

{business_data}

Answer questions based ONLY on this real data. Be specific with numbers and names.
Keep responses concise and scannable.
Always end with an actionable insight or recommendation.
Use Slack markdown formatting:
- Use *bold* for emphasis (not **bold**)
- Use • for bullet points
- Keep responses clean and scannable

If the question involves pipeline by stage, revenue breakdown, account comparison,
or any data that can be visualized, also return a JSON block at the END of your response
in this exact format on a new line:
CHART_DATA:{{"type":"bar","title":"Chart Title","data":{{"Label1":value1,"Label2":value2}}}}

For pie charts use type "pie", for leaderboards use type "leaderboard", for bar charts use type "bar", for trends use type "line".
Only include CHART_DATA when you have actual numeric data to chart."""

async def run_agent(
    text: str,
    session_id: str | None = None,
    deps=None,
) -> tuple[str, str | None, bytes | None, str | None]:
    """Run the agent and optionally generate a chart.
    Returns: (response_text, session_id, chart_bytes, chart_filename)
    """
    chart_keywords = ['chart', 'graph', 'plot', 'show', 'visualize',
                      'pipeline', 'breakdown', 'distribution', 'compare',
                      'trend', 'leaderboard', 'ranking', 'by stage',
                      'by region', 'by account', 'top', 'best', 'worst']

    wants_chart = any(kw in text.lower() for kw in chart_keywords)

    fresh_data = load_business_data()
    fresh_prompt = SYSTEM_PROMPT_TEMPLATE.format(business_data=fresh_data)

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction=fresh_prompt,
                )
            )

            response_text = response.text
            chart_bytes = None
            chart_filename = None

            if wants_chart and "CHART_DATA:" in response_text:
                from chart_generator import (generate_pipeline_chart,
                                             generate_pie_chart,
                                             generate_leaderboard_chart,
                                             generate_line_chart)
                try:
                    parts = response_text.split("CHART_DATA:")
                    clean_text = parts[0].strip()
                    chart_json = json.loads(parts[1].strip())

                    chart_type = chart_json.get("type", "bar")
                    chart_title = chart_json.get("title", "BizPulse Chart")
                    chart_data = chart_json.get("data", {})

                    if chart_type == "pie":
                        chart_bytes = generate_pie_chart(chart_data, chart_title)
                    elif chart_type == "leaderboard":
                        chart_bytes = generate_leaderboard_chart(chart_data, chart_title)
                    elif chart_type == "line":
                        chart_bytes = generate_line_chart(chart_data, chart_title)
                    else:
                        chart_bytes = generate_pipeline_chart(chart_data)

                    chart_filename = f"bizpulse_{chart_type}.png"
                    response_text = clean_text

                except Exception as e:
                    print(f"Chart generation error: {e}")
                    if "CHART_DATA:" in response_text:
                        response_text = response_text.split("CHART_DATA:")[0].strip()

            return response_text, None, chart_bytes, chart_filename

        except Exception as e:
            if "429" in str(e) and attempt < 2:
                wait_time = (attempt + 1) * 15
                await asyncio.sleep(wait_time)
            else:
                raise e

    return "Sorry, I'm busy right now. Please try again in a moment!", None, None, None