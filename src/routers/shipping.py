from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from src.schemas.shipping import ShippingItem,ShippingCreate
from src.models import shipping




Shippings = APIRouter(tags=["Shippings"])
db = Sessionlocal()


@Shippings.post("/shipping/", response_model=ShippingCreate)
def create_shipping(shippings: ShippingCreate):
    db_shipping = shipping(
        address=shippings.address,
        shipping_method=shippings.shipping_method,
        shipping_cost=shippings.shipping_cost,
        carrier_name=shippings.carrier_name,
        estimated_delivery=shippings.estimated_delivery,
        tracking_number=shippings.tracking_number,
        delivery_status=shippings.delivery_status,
        notes=shippings.notes
    )
    db.add(db_shipping)
    db.commit()
    db.refresh(db_shipping)
    return db_shipping
