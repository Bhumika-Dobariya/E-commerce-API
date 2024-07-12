from pydantic import BaseModel
from typing import Optional,List

class Allorder(BaseModel):
    
    user_id :str
    product_id :str
    quantity :int
    status:str
 


class UpdateOrder(BaseModel):
    
    user_id :Optional[str] = None
    product_id :Optional[str] = None
    quantity :Optional[int] = None
    status:Optional[str] = None
    total_price :Optional[str] = None
    
    
class ordern(BaseModel):
    Items: List[Allorder]