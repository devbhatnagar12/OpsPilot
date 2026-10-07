from ollama import chat

from apps.api.app.database import SessionLocal
from tools.inventory_tools import get_inventory_risk_by_sku


SYSTEM_PROMPT = """
You are OpsPilot, an AI operations assistant for a manufacturing company.

Your job is to investigate operational questions using the available tools.

GROUNDING RULES:
- Tool results are the authoritative source of operational facts.
- Never invent numbers, thresholds, policies, recommendations, trends, or business rules.
- Only state a number if that number appears in the tool result.
- Never describe a value as "recommended", "optimal", "target", or "required"
  unless the tool result explicitly says so.
- Do not introduce external inventory-management rules.
- You may interpret the evidence, but clearly distinguish interpretation
  from factual data.
- If the available evidence is insufficient to answer something, say so.

For inventory-risk questions:
- Report the risk level returned by the tool.
- Report relevant stock, demand, reorder point, and days-of-stock values
  exactly as supported by the tool.
- Explain why the tool classified the inventory at that risk level.
- Do not create additional risk thresholds.

Keep the final answer concise and useful to an operations team.
"""


INVENTORY_RISK_TOOL = {
    "type": "function",
    "function": {
        "name": "get_inventory_risk_by_sku",
        "description": (
            "Get current inventory risk and operational evidence for a "
            "specific product SKU."
        ),
        "parameters": {
            "type": "object",
            "required": ["sku"],
            "properties": {
                "sku": {
                    "type": "string",
                    "description": "The product SKU to investigate.",
                }
            },
        },
    },
}


def investigate_inventory_risk(user_question: str) -> str:
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_question,
        },
    ]

    response = chat(
        model="llama3.2:3b",
        messages=messages,
        tools=[INVENTORY_RISK_TOOL],
    )

    tool_calls = response["message"].get("tool_calls", [])

    if not tool_calls:
        return response["message"]["content"]

    messages.append(response["message"])

    db = SessionLocal()

    try:
        for tool_call in tool_calls:
            if tool_call["function"]["name"] != "get_inventory_risk_by_sku":
                continue

            arguments = tool_call["function"]["arguments"]
            sku = arguments["sku"]

            tool_result = get_inventory_risk_by_sku(db, sku)

            messages.append(
                {
                    "role": "tool",
                    "content": str(tool_result),
                }
            )
    finally:
        db.close()

    final_response = chat(
        model="llama3.2:3b",
        messages=messages,
    )

    return final_response["message"]["content"]