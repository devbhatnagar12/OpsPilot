from sqlalchemy.orm import Session

from apps.api.app.models import Inventory
from apps.api.app.services.inventory_risk import calculate_inventory_risk


def get_inventory_risk_by_sku(
    db: Session,
    sku: str,
):
    inventory = (
        db.query(Inventory)
        .join(Inventory.product)
        .filter(Inventory.product.has(sku=sku))
        .first()
    )

    if inventory is None:
        return {
            "found": False,
            "sku": sku,
            "message": f"No inventory data found for SKU '{sku}'.",
        }

    risk = calculate_inventory_risk(inventory)

    return {
        "found": True,
        "sku": risk.sku,
        "product_name": risk.product_name,
        "current_stock": risk.current_stock,
        "daily_demand": risk.daily_demand,
        "reorder_point": risk.reorder_point,
        "days_of_stock": risk.days_of_stock,
        "risk_level": risk.risk_level,
        "explanation": risk.explanation,
    }