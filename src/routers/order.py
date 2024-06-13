from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from src.schemas.order import Allorder,UpdateOrder
from src.models.orders import Orders
from src.models.user import User
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
orders = APIRouter(tags=['orders'])
db = Sessionlocal()



#create order

@orders.post("/create_orders",response_model=Allorder)
def create_order(Order: Allorder):
    existing_order = db.query(Orders).filter(
        Orders.user_id == Order.user_id,
        Orders.product_id == Order.product_id,
        Orders.is_active == True,
        Orders.is_deleted == False
    ).first()

    if existing_order:
        raise HTTPException(status_code=400, detail="Duplicate order not allowed")

    new_order = Orders(
        user_id=Order.user_id,
        product_id=Order.product_id,
        quantity=Order.quantity,
        status=Order.status,
        unit_price=Order.unit_price
    )
    
    db.add(new_order)
    db.commit()

    return new_order



#get order

@orders.get("/get_orders",response_model=Allorder)
def read_order(id:str):
    db_order = db.query(Orders).filter(Orders.id==id,Orders.is_active==True,Orders.is_deleted==False).first()
    if db_order is None:
        raise HTTPException(status_code=404,detail="order not found")
    return db_order


#get all order

@orders.get("/get_all_orders",response_model=list[Allorder])
def read_All_order():
    db_order = db.query(Orders).filter(Orders.is_active==True,Orders.is_deleted==False).all()
    if db_order is None:
        raise HTTPException(status_code=404,detail="order not found")
    return db_order



#update order

@orders.patch("/update_order", response_model=Allorder)
def update_order(norder: UpdateOrder,id:str):
    
    db_order = db.query(Orders).filter(Orders.id == id, Orders.is_active == True,Orders.is_deleted==False).first()

    if  db_order  is None:
        raise HTTPException(status_code=404, detail="order not found")

    for field_name, value in norder.dict().items():
        if value is not None:
            setattr( db_order , field_name, value)

    db.commit()
    return  db_order 



#delete order

@orders.delete("/delete_orders")
def delete_orders(id:str):
    db_order = db.query(Orders).filter(Orders.id==id,Orders.is_active==True,Orders.is_deleted==False).first()
    if db_order is None:
        raise HTTPException(status_code=404,detail="order not found")
    if Orders.is_deleted:
        raise HTTPException(status_code=400, detail="Order is already deleted")
    
    db_order.status = "deleted"
    db_order.is_active=False
    db_order.is_deleted =True
    
    db.commit()
    return {"message": "order deleted successfully"}



#cancle order

@orders.put("/cancel_order")
def cancel_order(order_id: str):
    db_order = db.query(Orders).filter(Orders.id == order_id).first()
    
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if not db_order.is_active:
        raise HTTPException(status_code=400, detail="Order is already cancelled")
    
    db_order.status = "cancelled"
    db_order.modified_at = datetime.now()
    db_order.is_active = False
    
    db.commit()
    
    return {"message": "Order cancelled successfully"}



#get order by user id

@orders.get("/search_order_by_user_id")
def read_order_By_user_id(user_id :str):
    db_order = db.query(Orders).filter(Orders.user_id==user_id,Orders.is_active==True,Orders.is_deleted==False).all()
    if db_order is None:
        raise HTTPException(status_code=404,detail="order not found")
    return db_order



#get all order after date

@orders.get("/get_allorder_after_date", response_model=list[Allorder])
def get_products_after_date(date: datetime):
    new_order = db.query(Orders).filter(Orders.created_at>date,Orders.is_active==True,Orders.is_deleted==False).all()
    if new_order is None:
        raise HTTPException(status_code=404,detail= "order not found ")
    return new_order



#get all order between two dates

@orders.get("/get_allorder_between_two_dates", response_model=list[Allorder])
def get_products_after_date(first_date: datetime,last_date: datetime):
    new_order = db.query(Orders).filter(Orders.created_at>first_date,Orders.created_at<last_date,Orders.is_active==True,Orders.is_deleted==False).all()
    if new_order is None:
        raise HTTPException(status_code=404,detail= "order not found ")
    return new_order



#get all users which status is done

@orders.get("/get_all_orders_status_done",response_model=list[Allorder])
def read_All_order():
    db_order = db.query(Orders).filter(Orders.status=="done",Orders.is_active==True,Orders.is_deleted==False).all()
    if db_order is None:
        raise HTTPException(status_code=404,detail="order not found")
    return db_order



#order conformation

"""
def send_order_confirmation_email(email: str,order ):
    
    order_details = f"Order ID: {order.id}\n" \
                    f"User ID: {order.user_id}\n" \
                    f"Product ID: {order.product_id}\n" \
                    f"Quantity: {order.quantity}\n" \
                    f"Status: {order.status}\n" \
                    f"Unit Price: {order.unit_price}\n" \
                  
                    
    sender_email = "bhumikadobariya2412@gmail.com"
    receiver_email = email
    password = "qzdjaauunsmgrvgd"
    subject = "Order Confirmation"
    message_text = f"Thank you for your order! Your order details: {order_details}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    
    
    message.attach(MIMEText(message_text, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Mail sent successfully")
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")
        
        
        
#order conformation email

@orders.post("/send_order_conformation")
def send_order_conformation(order_id:str):
    db_order = db.query(Orders).filter(Orders.id ==order_id).first()
    
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    user_id = db_order.user_id
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.email:
        raise HTTPException(status_code=400, detail="User email not provided")
    
 
    send_order_confirmation_email(user.email, db_order)
    
    return {"message": "Order confirmation email sent successfully"}"""
