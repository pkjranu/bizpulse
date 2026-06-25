import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="""You are BizPulse, a friendly business intelligence assistant in Slack. 
You help people get insights about their business data.
Keep responses concise, clear and actionable.
Use bullet points for multi-step answers."""
)

async def run_agent(
    text: str,
    session_id: str | None = None,
    deps=None,
) -> tuple[str, str | None]:
    
    response = model.generate_content(text)
    return response.text, None