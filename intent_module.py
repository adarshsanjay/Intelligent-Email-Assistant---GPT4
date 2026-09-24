from utils import ask_ollama

INTENTS = [
    "Delivery Issue",
    "Refund Request",
    "Product Complaint",
    "Technical Support",
    "Order Cancellation",
    "General Inquiry",
]


def detect_intent(customer_email: str) -> str:

    labels = "\n".join(
        f"- {x}"
        for x in INTENTS
    )

    prompt = f"""Classify the customer email into exactly ONE of these intents:
{labels}

Customer email:
{customer_email}

Return ONLY the exact intent label. Do not add explanations."""

    result = ask_ollama(prompt)

    for intent in INTENTS:

        if intent.lower() in result.lower():
            return intent

    return "General Inquiry"