from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, unique=True)

    current_stock = Column(Integer, nullable=False, default=0)
    daily_demand = Column(Float, nullable=False, default=0)
    reorder_point = Column(Integer, nullable=False, default=0)

    product = relationship("Product", back_populates="inventory")