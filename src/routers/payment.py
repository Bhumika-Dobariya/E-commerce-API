from fastapi import FastAPI, HTTPException, APIRouter,Request
from database.database import Sessionlocal
from src.models.payment import Payment
from src.models.cart import Cart,CartItem
from src.schemas.payment import AllPayment,PaymentIntentRequest
from datetime import datetime
import stripe
from stripe import SignatureVerificationError
from logs.log_config import logger
import os


payments = APIRouter(tags=["Payment"])
db = Sessionlocal()


#___________create_payment_________________


@payments.post("/create_payment", response_model=AllPayment)
def create_payment(payment_data: AllPayment):
    logger.info("Creating payment for cart_id: %s", payment_data.cart_id)
    
    cart = db.query(CartItem).filter(CartItem.id == payment_data.cart_id).first()
    if cart is None:
        logger.error("Cart not found for cart_id: %s", payment_data.cart_id)
        raise HTTPException(status_code=404, detail="cart not found")
    
    amount = cart.total_price

    payment = Payment(
        user_id=payment_data.user_id,
        cart_id=payment_data.cart_id,
        order_id=payment_data.order_id,
        amount=amount,
        payment_method=payment_data.payment_method,
        card_holder_name=payment_data.card_holder_name,
        card_number=payment_data.card_number,
        cvv=payment_data.cvv,
        expiry_month=payment_data.expiry_month,
        expiry_year=payment_data.expiry_year,
        currency=payment_data.currency,
        transaction_id=payment_data.transaction_id,
        billing_address=payment_data.billing_address,
        shipping_address=payment_data.shipping_address,
        payment_date=datetime.now(),
    )
    db.add(payment)
    db.commit()
    logger.info("Payment created successfully for cart_id: %s", payment_data.cart_id)
    return payment



#_____________get_payments_________________


@payments.get("/get_payments", response_model=AllPayment)
def get_payments(id: str):
    logger.info("Fetching payment with id: %s", id)
    db_payment = db.query(Payment).filter(Payment.id == id, Payment.is_active == True, Payment.is_deleted == False).first()
    if db_payment is None:
        logger.error("Payment not found with id: %s", id)
        raise HTTPException(status_code=404, detail="payment not found")
    logger.info("Payment fetched with id: %s", id)
    return db_payment



#________________delete_payments_________________


@payments.delete("/delete_payments")
def delete_payment(id: str):
    logger.info("Deleting payment with id: %s", id)
    db_payment = db.query(Payment).filter(Payment.id == id, Payment.is_active == True, Payment.is_deleted == False).first()
    if db_payment is None:
        logger.error("Payment not found with id: %s", id)
        raise HTTPException(status_code=404, detail="payment not found")
    db_payment.is_active = False
    db_payment.is_deleted = True
    db.commit()
    logger.info("Payment deleted successfully with id: %s", id)
    return {"message": "payment deleted successfully"}



#________________create_payment_intent________________


@payments.post("/create_payment_intent")
def create_payment_intent(request: PaymentIntentRequest):
    try:
        logger.info("Received request to create payment intent with amount: %d and currency: %s", request.amount, request.currency)
        
        payment_intent = stripe.PaymentIntent.create(
            amount=request.amount * 100,
            currency=request.currency
        )
        
        logger.info("Payment intent created successfully. Client secret: %s", payment_intent.client_secret)
        return {"client_secret": payment_intent.client_secret}
    except Exception as e:
        logger.error("Error creating payment intent: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))



#___________webhook_stripe________________


@payments.post("/webhook_stripe")
async def stripe_webhook(request: Request):
    logger.info("Received Stripe webhook event")
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature", None)
    stripe_webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_webhook_secret
        )
        logger.info("Webhook event received: %s", event)
    except ValueError as e:
        logger.error("Invalid payload: %s", str(e))
        raise HTTPException(status_code=400, detail="Invalid payload")
    except SignatureVerificationError as e:
        logger.error("Invalid signature: %s", str(e))
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "payment_intent.succeeded":
        logger.info("Payment succeeded: %s", event)

    elif event["type"] == "payment_intent.payment_failed":
        logger.error("Payment failed: %s", event)

    return {"status": "success"}
