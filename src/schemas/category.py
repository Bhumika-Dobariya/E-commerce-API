from pydantic import BaseModel
from typing import Optional

class Allcategories(BaseModel):
    name: str
    description: str
    
class Partialcategories(BaseModel):
    name:Optional[str] = None
    description: Optional[str] = None