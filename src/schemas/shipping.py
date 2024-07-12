
from pydantic import BaseModel
from typing import Optional,List


class ShippingItem(BaseModel):
    item_name: str
    quantity: int
    weight: float  



class ShippingCreate(BaseModel):
    address: str
    shipping_method: str
    shipping_cost  : float
    carrier_name : str
    estimated_delivery: str
    tracking_number: str = None
    delivery_status :str
    notes : str
    items: List[ShippingItem]
