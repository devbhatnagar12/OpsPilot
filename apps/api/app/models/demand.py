from datetime import date

from sqlalchemy import Date, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class DemandHistory(Base):
    __tablename__ = "demand_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    demand_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    units_sold: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    product = relationship("Product")

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "demand_date",
            name="uq_demand_product_date",
        ),
    )