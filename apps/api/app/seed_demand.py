from datetime import date, timedelta

from apps.api.app.database import SessionLocal
from apps.api.app.models import DemandHistory, Product


def seed_demand_history():
    db = SessionLocal()

    try:
        product = (
            db.query(Product)
            .filter(Product.sku == "MTR-4821")
            .first()
        )

        if product is None:
            raise ValueError("MTR-4821 not found")

        db.query(DemandHistory).filter(
            DemandHistory.product_id == product.id
        ).delete()

        demand_values = [
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            53,
            55,
            57,
            59,
            61,
            64,
        ]

        start_date = date.today() - timedelta(days=13)

        for offset, units in enumerate(demand_values):
            db.add(
                DemandHistory(
                    product_id=product.id,
                    demand_date=start_date + timedelta(days=offset),
                    units_sold=units,
                )
            )

        db.commit()

        print("Demand history seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_demand_history()