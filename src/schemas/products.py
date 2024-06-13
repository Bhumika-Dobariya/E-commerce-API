from pydantic import BaseModel
from typing import Optional

class AllProduct(BaseModel):
    name: str
    description: str
    price: float
    category_id:str
    stock_quantity: int
    

class PartialUpadate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[str] = None
    category_id:Optional[str] = None
    stock_quantity: Optional[str] = None