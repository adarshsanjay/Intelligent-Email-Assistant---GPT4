from utils import ask_ollama


TONES = [
    "Friendly",
    "Formal",
    "Empathetic"
]


def improve_tone(
    reply: str,
    tone: str
) -> str:

    prompt = f"""Rewrite the following customer-support email in a {tone.lower()} tone.

Keep the meaning and factual information unchanged.
Do not add invented details.
Return only the rewritten email.

Original email:
{reply}"""

    return ask_ollama(prompt)
