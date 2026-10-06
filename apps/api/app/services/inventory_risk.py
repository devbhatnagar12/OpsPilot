from dataclasses import dataclass
from typing import Protocol


class InventoryData(Protocol):
    product_id: int
    current_stock: int
    daily_demand: float
    reorder_point: int
    product: object


@dataclass
class InventoryRisk:
    product_id: int
    sku: str
    product_name: str
    category: str
    current_stock: int
    daily_demand: float
    reorder_point: int
    days_of_stock: float
    risk_level: str
    explanation: str


def calculate_inventory_risk(inventory: InventoryData) -> InventoryRisk:
    if inventory.daily_demand <= 0:
        days_of_stock = float("inf")
        risk_level = "LOW"
    else:
        days_of_stock = inventory.current_stock / inventory.daily_demand

        if days_of_stock < 5:
            risk_level = "HIGH"
        elif days_of_stock <= 10:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

    if inventory.current_stock < inventory.reorder_point:
        explanation = (
            f"{inventory.product.name} has {days_of_stock:.1f} days of stock "
            f"remaining at the current daily demand of "
            f"{inventory.daily_demand:.0f} units. "
            f"Current stock of {inventory.current_stock} units is below "
            f"the reorder point of {inventory.reorder_point} units."
        )

    else:
        explanation = (
            f"{inventory.product.name} has {days_of_stock:.1f} days of stock "
            f"remaining at the current daily demand of "
            f"{inventory.daily_demand:.0f} units."
        )

    return InventoryRisk(
        product_id=inventory.product_id,
        sku=inventory.product.sku,
        product_name=inventory.product.name,
        category=inventory.product.category,
        current_stock=inventory.current_stock,
        daily_demand=inventory.daily_demand,
        reorder_point=inventory.reorder_point,
        days_of_stock=days_of_stock,
        risk_level=risk_level,
        explanation=explanation,
    )