from pydantic import BaseModel
from typing import Optional


class ProductReviewCreate(BaseModel):
    user_id :str
    product_id: str
    description: str
    stars: float

class ProductReviewUpdate(BaseModel):
    user_id :Optional[str] = None
    product_id: Optional[str] = None
    description: Optional[str] = None
    stars: Optional[str] = None
    

class ProductStar(BaseModel):
        stars: float
