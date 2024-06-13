from pydantic import BaseModel
from typing import Optional


class AllAddress(BaseModel):
    city : str
    state : str
    zip_code : str
    user_id : str
    

class AddressUpdate(BaseModel):
    city : Optional[str] = None
    state : Optional[str] = None
    zip_code : Optional[str] = None
    user_id : Optional[str] = None