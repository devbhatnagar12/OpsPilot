from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Inventory
from ..services.inventory_risk import calculate_inventory_risk

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
)


@router.get("/risks")
def get_inventory_risks(
    db: Session = Depends(get_db),
):
    inventory_items = db.query(Inventory).all()

    return [
        calculate_inventory_risk(item)
        for item in inventory_items
    ]