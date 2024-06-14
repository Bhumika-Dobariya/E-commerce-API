from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class AllPayment(BaseModel):
    user_id: str
    cart_id: str
    order_id: str
    payment_method: str
    card_number: str
    cvv: str
    expiry_month: str
    expiry_year: str
    transaction_id: str
    billing_address: str
    shipping_address: str