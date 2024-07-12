from fastapi import FastAPI, HTTPException, APIRouter,Request
from database.database import Sessionlocal
from src.models.payment import Payment
from src.models.cart import Cart,CartItem
from src.schemas.payment import AllPayment,UpdatePayment,PaymentIntentRequest
from datetime import datetime
import stripe
from stripe import SignatureVerificationError
from logs.log_config import logger
import os


payments = APIRouter(tags=["Payment"])
db = Sessionlocal()


@payments.post("/create_payment",response_model=AllPayment)
def create_payment(payment_data:AllPayment):
    
        cart = db.query(CartItem).filter(CartItem.id ==payment_data.cart_id).first()
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




@payments.post("/create_payment_intent")
def create_payment_intent(request: PaymentIntentRequest):
    try:
        logger.info(f"Received request to create payment intent with amount={request.amount} and currency={request.currency}")

        payment_intent = stripe.PaymentIntent.create(
            amount=request.amount*100,
            currency=request.currency
        )

        logger.info(f"Payment intent created successfully. Client secret: {payment_intent.client_secret}")

        return {"client_secret": payment_intent.client_secret}
    except Exception as e:
        logger.error(f"Error creating payment intent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))




# Endpoint to handle Stripe webhook events


@payments.post("/webhook_stripe")
async def stripe_webhook(request: Request):
    payload =  request.body()
    sig_header = request.headers.get("Stripe-Signature", None)
    stripe_webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_webhook_secret
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "payment_intent.succeeded":

        print("Payment succeeded:", event)

    elif event["type"] == "payment_intent.payment_failed":

        print("Payment failed:", event)

    return {"status": "success"}