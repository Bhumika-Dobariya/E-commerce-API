from pydantic import BaseModel
from typing import Optional

class AllProduct(BaseModel):
    name: str
    description: str
    product_price: float
    discount_percent : float
    category_id:str
    stock_quantity: int
    

class PartialUpadate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    product_price: Optional[str] = None
    discount_percent: Optional[str] = None
    category_id:Optional[str] = None
    stock_quantity: Optional[str] = None