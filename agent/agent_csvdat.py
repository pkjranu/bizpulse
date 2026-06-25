import google.generativeai as genai
import os
import pandas as pd
import asyncio
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def load_business_data():
    try:
        df = pd.read_csv("data/sales_data.csv")
        return df.to_string(index=False)
    except Exception as e:
        return "No data available"

BUSINESS_DATA = load_business_data()

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=f"""You are BizPulse, an AI business intelligence assistant in Slack.
You have access to the following business data:
{BUSINESS_DATA}

Answer questions based ONLY on this data. Be specific with numbers.
Keep responses concise and use bullet points for lists.
Always end with an actionable insight or recommendation.
Use Slack markdown formatting rules:
- Use *bold* for emphasis (not **bold**)
- Use bullet points with • symbol (not *)
- Keep responses clean and scannable"""
)

async def run_agent(
    text: str,
    session_id: str | None = None,
    deps=None,
) -> tuple[str, str | None]:
    for attempt in range(3):
        try:
            response = model.generate_content(text)
            return response.text, None
        except Exception as e:
            if "429" in str(e) and attempt < 2:
                wait_time = (attempt + 1) * 15
                await asyncio.sleep(wait_time)
            else:
                raise e
    return "Sorry, I'm busy right now. Please try again in a moment!", None