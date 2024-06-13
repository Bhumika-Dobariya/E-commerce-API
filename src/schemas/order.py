from pydantic import BaseModel
from typing import Optional

class Allorder(BaseModel):
    
    user_id :str
    product_id :str
    quantity :int
    status:str
    unit_price :float


class UpdateOrder(BaseModel):
    
    user_id :Optional[str] = None
    product_id :Optional[str] = None
    quantity :Optional[str] = None
    status:Optional[str] = None
    unit_price :Optional[str] = None