from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from src.models.payment import Payment
from src.models.cart import Cart
from src.schemas.payment import AllPayment,UpdatePayment,PaymentIntentRequest
from datetime import datetime
import stripe

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
            card_holder_name = payment_data.card_holder_name,
            card_number=payment_data.card_number,
            cvv=payment_data.cvv,
            expiry_month=payment_data.expiry_month,
            expiry_year=payment_data.expiry_year,
            currency=payment_data.currency,
            transaction_id = payment_data.transaction_id,
            billing_address=payment_data.billing_address,
            shipping_address=payment_data.shipping_address,
            payment_date=datetime.now(),
        )
        db.add(payment)
        db.commit()
        return payment            
    
    
    
#get payment

@payments.get("/get_payments",response_model=AllPayment)
def get_payments(id:str):
    db_payment = db.query(Payment).filter(Payment.id ==id,Payment.is_active==True,Payment.is_deleted==False).first()
    if db_payment is None:
        raise HTTPException(status_code=404,detail="payment not found")
    return db_payment


#update payment

@payments.patch("/update_payment", response_model=AllPayment)
def update_payment(product: UpdatePayment,id:str):
    
    db_payments = db.query(Payment).filter(Payment.id == id, Payment.is_active == True,Payment.is_deleted==False).first()

    if  db_payments  is None:
        raise HTTPException(status_code=404, detail="payment not found")

    for field_name, value in product.dict().items():
        if value is not None:
            setattr( db_payments , field_name, value)

    db.commit()
    return  db_payments


#delete payment

@payments.delete("/delete_payments")
def delete_product(id:str):
    db_payments = db.query(Payment).filter(Payment.id==id,Payment.is_active==True,Payment.is_deleted==False).first()
    if db_payments is None:
        raise HTTPException(status_code=404,detail="payment not found")
    db_payments.is_active=False
    db_payments.is_deleted =True
    db.commit()
    return {"message": "payment deleted successfully"}




@payments.post("/create-payment-intent")
def create_payment_intent(request: PaymentIntentRequest):
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=request.amount,
            currency=request.currency
        )
        return {"client_secret": payment_intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
