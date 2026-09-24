from utils import ask_ollama


def generate_reply(
    customer_email: str,
    previous_reply: str,
    customer_name: str
) -> str:

    prompt = f"""You are a professional customer-support email assistant.

Customer name: {customer_name}

New customer email:
{customer_email}

A similar historical reply is:
{previous_reply}

Write a professional, concise reply to the NEW customer email.
Use the historical reply only as context.
Do not invent order numbers, dates, refunds, tracking numbers, or policies that were not provided.
Address the customer politely.
Return only the email body, including a suitable greeting and closing."""

    return ask_ollama(prompt)