import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# In-memory session store: { session_id: [messages] }
sessions: dict[str, list] = {}


async def get_gemini_response(message: str, session_id: str) -> str:
    # Initialize session if new
    if session_id not in sessions:
        sessions[session_id] = []

    # Add user message to history
    sessions[session_id].append({
        "role": "user",
        "parts": [{"text": message}]
    })

    # Call Gemini with full conversation history
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=sessions[session_id]
    )

    reply = response.text

    # Save assistant reply to history
    sessions[session_id].append({
        "role": "model",
        "parts": [{"text": reply}]
    })

    return reply


def delete_session(session_id: str) -> bool:
    if session_id in sessions:
        del sessions[session_id]
        return True
    return False


def get_all_sessions() -> list[str]:
    return list(sessions.keys())