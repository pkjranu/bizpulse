from google import genai
from google.genai import types
import os
import requests
import asyncio
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

BUSINESS_DATA = load_business_data()

SYSTEM_PROMPT = f"""You are BizPulse, an AI-powered business intelligence assistant in Slack.
You have access to live Salesforce CRM data:

{BUSINESS_DATA}

Answer questions based ONLY on this real data. Be specific with numbers and names.
Keep responses concise and scannable.
Always end with an actionable insight or recommendation.
Use Slack markdown formatting:
- Use *bold* for emphasis (not **bold**)
- Use • for bullet points
- Keep responses clean and scannable"""

async def run_agent(
    text: str,
    session_id: str | None = None,
    deps=None,
) -> tuple[str, str | None]:
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                )
            )
            return response.text, None
        except Exception as e:
            if "429" in str(e) and attempt < 2:
                wait_time = (attempt + 1) * 15
                await asyncio.sleep(wait_time)
            else:
                raise e
    return "Sorry, I'm busy right now. Please try again in a moment!", None