import os
import anthropic
from intelligence.prompts import MACRO_ANALYST_SYSTEM

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SESSION_HISTORY: dict[str, list[dict]] = {}
SESSION_MAX_TURNS = 5

def get_session_key(user_id: int, channel_id: int) -> str:
    return f"{user_id}:{channel_id}"

def clear_session(user_id: int, channel_id: int) -> None:
    SESSION_HISTORY.pop(get_session_key(user_id, channel_id), None)

async def analyze(user_id: int, channel_id: int, document: str, question: str) -> str:
    key = get_session_key(user_id, channel_id)

    if key not in SESSION_HISTORY:
        SESSION_HISTORY[key] = [
            {"role": "user", "content": f"Document:\n\n{document}\n\nQuestion: {question}"}
        ]
    else:
        if len(SESSION_HISTORY[key]) >= SESSION_MAX_TURNS * 2:
            return "Session limit reached (5 exchanges). Use `/analyze` with a new document to start a fresh session."
        SESSION_HISTORY[key].append({"role": "user", "content": question})

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=MACRO_ANALYST_SYSTEM,
        messages=SESSION_HISTORY[key],
    )
    reply = response.content[0].text
    SESSION_HISTORY[key].append({"role": "assistant", "content": reply})
    return reply

async def complete(prompt: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=MACRO_ANALYST_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
