from pydantic import BaseModel
from typing import Optional



class AllCart(BaseModel):
    user_id : str
    product_id : str
    quantity : int
    
class UpdateCart(BaseModel):
    user_id : Optional[str] = None
    product_id : Optional[str] = None
    quantity : Optional[str] = None
   
class Product(BaseModel):
    id: int
    name: str
    price: float

class CartItem(BaseModel):
    product: Product
    quantity: int