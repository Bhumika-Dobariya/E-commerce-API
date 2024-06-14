from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from src.models.payment import Payment
from src.models.cart import Cart
from src.schemas.payment import AllPayment
from datetime import datetime

payments = APIRouter(tags=["Payment"])
db = Sessionlocal()


@payments.post("/create payment",response_model=AllPayment)
def create_payment(payment_data:AllPayment):
    
        cart = db.query(Cart).filter(Cart.id ==payment_data.cart_id).first()
        if cart is None:
            raise HTTPException(status_code=404,detail= "cart not found")
        
        amount = cart.total_price
        
      
        payment = Payment(
            user_id=payment_data.user_id,
            cart_id=payment_data.cart_id,
            order_id=payment_data.order_id,
            amount=amount,
            payment_method=payment_data.payment_method,
            card_number=payment_data.card_number,
            cvv=payment_data.cvv,
            expiry_month=payment_data.expiry_month,
            expiry_year=payment_data.expiry_year,
            transaction_id = payment_data.transaction_id,
            billing_address=payment_data.billing_address,
            shipping_address=payment_data.shipping_address,
            payment_date=datetime.now(),
        )
        db.add(payment)
        db.commit()
        return payment            
    
    
    
