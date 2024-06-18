from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class AllPayment(BaseModel):
    user_id: str
    cart_id: str
    order_id: str
    payment_method: str
    card_holder_name:str
    card_number: str
    cvv: str
    expiry_month: str
    expiry_year: str
    currency:str
    transaction_id: str
    billing_address: str
    shipping_address: str
    
    

class UpdatePayment(BaseModel):
    user_id: Optional[str] = None
    cart_id: Optional[str] = None
    order_id: Optional[str] = None
    payment_method: Optional[str] = None
    card_holder_name:Optional[str] = None
    card_number: Optional[str] = None
    cvv: Optional[str] = None
    expiry_month: Optional[str] = None
    expiry_year: Optional[str] = None
    currency:Optional[str] = None
    transaction_id: Optional[str] = None
    billing_address: Optional[str] = None
    shipping_address: Optional[str] = None
    
class PaymentIntentRequest(BaseModel):
    amount: int
    currency: str = 'usd'