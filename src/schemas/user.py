from pydantic import BaseModel
from typing import Optional

class UserAll(BaseModel):
    first_name : str
    last_name : str
    user_name : str
    password  : str
    email : str
    mob_no : str
    address :str

class PartialUser(BaseModel):
    first_name :Optional[str] = None
    last_name : Optional[str] = None
    user_name : Optional[str] = None
    password  : Optional[str] = None
    email : Optional[str] = None
    mob_no : Optional[str] = None
    address :Optional[str] = None


class userpass(BaseModel):
    password :str
    
