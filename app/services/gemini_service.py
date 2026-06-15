import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


print("GROQ_API_KEY exists:", bool(os.getenv("GROQ_API_KEY")))
print("First chars:", os.getenv("GROQ_API_KEY", "")[:8])

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# In-memory session store: { session_id: [messages] }
sessions: dict[str, list] = {}


async def get_gemini_response(message: str, session_id: str) -> str:
    # Initialize session if new
    if session_id not in sessions:
        sessions[session_id] = []

    # Add user message to history
    sessions[session_id].append({
        "role": "user",
        "content": message  # Groq uses "content" not "parts"
    })

    # Call Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=sessions[session_id]
    )

    reply = response.choices[0].message.content

    # Save assistant reply to history
    sessions[session_id].append({
        "role": "assistant",  # Groq uses "assistant" not "model"
        "content": reply
    })

    return reply


def delete_session(session_id: str) -> bool:
    if session_id in sessions:
        del sessions[session_id]
        return True
    return False


def get_all_sessions_with_messages() -> dict:
    return {
        session_id: messages
        for session_id, messages in sessions.items()
    }