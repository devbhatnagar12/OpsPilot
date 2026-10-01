from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import Inventory, Product


PRODUCTS = [
    {
        "sku": "MTR-4821",
        "name": "Industrial Motor",
        "category": "Industrial Motors",
        "current_stock": 420,
        "daily_demand": 58,
        "reorder_point": 500,
    },
    {
        "sku": "PMP-1042",
        "name": "Hydraulic Pump",
        "category": "Hydraulic Equipment",
        "current_stock": 850,
        "daily_demand": 35,
        "reorder_point": 300,
    },
    {
        "sku": "BRG-8821",
        "name": "Bearing Assembly",
        "category": "Mechanical Components",
        "current_stock": 120,
        "daily_demand": 30,
        "reorder_point": 200,
    },
    {
        "sku": "VAL-2291",
        "name": "Control Valve",
        "category": "Industrial Valves",
        "current_stock": 620,
        "daily_demand": 20,
        "reorder_point": 250,
    },
    {
        "sku": "SEN-7712",
        "name": "Pressure Sensor",
        "category": "Sensors",
        "current_stock": 45,
        "daily_demand": 15,
        "reorder_point": 100,
    },
]


def seed_database() -> None:
    db: Session = SessionLocal()

    try:
        for item in PRODUCTS:
            product = (
                db.query(Product)
                .filter(Product.sku == item["sku"])
                .first()
            )

            if product is None:
                product = Product(
                    sku=item["sku"],
                    name=item["name"],
                    category=item["category"],
                )
                db.add(product)
                db.flush()

            inventory = (
                db.query(Inventory)
                .filter(Inventory.product_id == product.id)
                .first()
            )

            if inventory is None:
                inventory = Inventory(
                    product_id=product.id,
                    current_stock=item["current_stock"],
                    daily_demand=item["daily_demand"],
                    reorder_point=item["reorder_point"],
                )
                db.add(inventory)

        db.commit()
        print("Database seeded successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()