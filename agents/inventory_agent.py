from ollama import chat

from apps.api.app.database import SessionLocal
from tools.inventory_tools import get_inventory_risk_by_sku


SYSTEM_PROMPT = """
You are OpsPilot, an AI operations assistant for a manufacturing company.

You help operations teams investigate inventory risks.

When a user asks about a specific SKU, use the inventory risk tool
to retrieve the actual operational data before answering.

Do not invent inventory numbers.

After receiving tool data, explain:
1. What the current risk is
2. Why the SKU is at risk
3. What evidence supports the conclusion

Keep the response concise and operational.
"""


def investigate_inventory_risk(sku: str) -> str:
    db = SessionLocal()

    try:
        inventory_data = get_inventory_risk_by_sku(db, sku)

        if not inventory_data["found"]:
            return inventory_data["message"]

        response = chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": (
                        f"Investigate inventory risk for SKU {sku}.\n\n"
                        f"Operational evidence:\n{inventory_data}"
                    ),
                },
            ],
        )

        return response["message"]["content"]

    finally:
        db.close()