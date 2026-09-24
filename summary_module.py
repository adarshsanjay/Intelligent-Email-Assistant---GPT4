from utils import ask_ollama


def summarize_conversation(
    customer_email: str,
    reply: str
) -> str:

    prompt = f"""Summarize the customer issue and response in EXACTLY 50 words.
Focus on the customer's problem, relevant context, and the support action/response.
Do not invent information.

Customer email:
{customer_email}

Support reply:
{reply}

Return only the 50-word summary."""

    summary = ask_ollama(prompt)

    words = summary.split()

    if len(words) > 50:
        summary = " ".join(
            words[:50]
        )

    return summary
