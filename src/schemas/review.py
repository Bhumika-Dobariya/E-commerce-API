from pydantic import BaseModel
from typing import Optional


class ProductReviewCreate(BaseModel):
    user_id :str
    product_id: str
    comment: str
    rating: int

class ProductReviewUpdate(BaseModel):
    user_id :Optional[str] = None
    product_id: Optional[str] = None
    comment: Optional[str] = None
    rating: Optional[str] = None
    

class ProductStar(BaseModel):
        rating: int
