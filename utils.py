from datetime import datetime
from pathlib import Path
import ollama

# IMPORTANT:
# Replace this with the exact model shown by:
# ollama list
MODEL = "qwen3:4b"


def ask_ollama(prompt: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.message.content.strip()


def save_reply(
    customer_email: str,
    generated_reply: str,
    intent: str,
    tone: str,
    summary: str
) -> str:

    output_path = Path(
        "outputs/generated_reply.txt"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    content = f"""INTELLIGENT EMAIL ASSISTANT
================================

Date:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Intent:
{intent}

Tone:
{tone}

Customer Email:
{customer_email}

Conversation Summary:
{summary}

Generated Reply:
{generated_reply}
"""

    output_path.write_text(
        content,
        encoding="utf-8"
    )

    return str(output_path)
