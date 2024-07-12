from pydantic import BaseModel
from typing import Optional,List



class CartItemBase(BaseModel):
    product_id: str
    quantity: int
    price: float
    total_price: float
    status:str
    
class updateCart(BaseModel):
    product_id: Optional[str] = None
    quantity: Optional[str] = None
    price: Optional[str] = None
    total_price: Optional[str] = None
    status: Optional[str] = None


class CartItems(CartItemBase): 
    cart_id: str
    
class Cartn(BaseModel):
    product_id: str
    quantity: int
    
class CartBase(BaseModel):
    user_id: str

class Carts(CartBase):
    id: str
    user_id: str
    items: List[CartItemBase] = []

class CartCreate(BaseModel):
    user_id: str
    
class CartItemCreate(CartItemBase):
    price: float
    total_price: float
