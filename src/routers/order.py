from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from src.schemas.order import Allorder,UpdateOrder,ordern
from src.schemas.cart import Carts
from src.models.orders import Orders
from src.models.user import User
from src.models.cart import Cart,CartItem
from src. models.products import Product
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List


orders = APIRouter(tags=['orders'])
db = Sessionlocal()

#######################################################################################discount

#create order

@orders.post("/create_orders", response_model=List[Allorder])
def create_orders(order_data: ordern):
    order_items = []

    for item in order_data.Items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")

        cart = db.query(Cart).filter(Cart.id == item.cart_id).first()
        if not cart:
            raise HTTPException(status_code=404, detail=f"Cart with id {item.cart_id} not found")

        
        total_price = product.discount_price * item.quantity

        order_item = Orders(
            user_id=item.user_id,
            product_id=item.product_id,
            cart_id=item.cart_id,
            quantity=item.quantity,
            status="pending",
            total_price=total_price,   
        )

        db.add(order_item)
        order_items.append(item)
        
    order_item.status= "Done"
    db.commit()
    

    return order_items



#get order

@orders.get("/get_orders",response_model=Allorder)
def read_order(id:str):
    db_order = db.query(Orders).filter(Orders.id==id,Orders.is_active==True,Orders.is_deleted==False).first()
    if db_order is None:
        raise HTTPException(status_code=404,detail="order not found")
    return db_order


#cart
@orders.get("/get_orders_by_cart",response_model=List[Allorder])
def read_order(cart_id: str):
        db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
        if not db_cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        db_cart_items = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()

        orders = []
        for item in db_cart_items:
         order = Allorder(
            user_id=db_cart.user_id,
            product_id=item.product_id,
            quantity=item.quantity,
            status=item.status,
        )
        orders.append(order)

        return orders
    
    
#Retrieve all orders placed by a specific user.

@orders.get("/get_orders_by_user", response_model=List[Allorder])
def get_orders_by_user(user_id: str):
    orders = db.query(Orders).filter(Orders.user_id == user_id, Orders.is_active == True, Orders.is_deleted == False).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for the user")
    return orders



#Retrieve all orders containing a specific product.

@orders.get("/get_orders_by_product", response_model=List[Allorder])
def get_orders_by_product(product_id: str):
    orders = db.query(Orders).filter(Orders.product_id == product_id, Orders.is_active == True, Orders.is_deleted == False).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for the product")
    return orders


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



#Reorder a Previous Order

@orders.post("/reorder/{order_id}", response_model=Allorder)
def reorder(order_id: str):
    original_order = db.query(Orders).filter(Orders.id == order_id, Orders.is_active == True, Orders.is_deleted == False).first()
    if not original_order:
        raise HTTPException(status_code=404, detail="Order not found")

    new_order = Orders(
        user_id=original_order.user_id,
        product_id=original_order.product_id,
        cart_id=original_order.cart_id,
        quantity=original_order.quantity,
        status="pending",
        total_price=original_order.total_price,
    )

    db.add(new_order)
    db.commit()
    return new_order


#archive_order

@orders.patch("/archive_order/{order_id}")
def archive_order(order_id: str):
    order = db.query(Orders).filter(Orders.id == order_id, Orders.is_active == True, Orders.is_deleted == False).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.is_active = False
    order.is_deleted = True
    order.is_archived = True
    db.commit()
    return {"message": "Order archived successfully"}

#order conformation


def send_order_confirmation_email(email: str, order):
    order_details = f"Order ID: {order.id}\n" \
                    f"User ID: {order.user_id}\n" \
                    f"Product ID: {order.product_id}\n" \
                    f"Quantity: {order.quantity}\n" \
                    f"Status: {order.status}\n" \
                    f"Total Price: {order.total_price}\n"

    sender_email = "bhumikadobariya2412@gmail.com"
    password = "qzdjaauunsmgrvgd"
    subject = "Order Confirmation"
    message_text = f"Thank you for your order! Your order details:\n\n{order_details}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject

    message.attach(MIMEText(message_text, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())
        print("Mail sent successfully")
        server.quit()
    except smtplib.SMTPRecipientsRefused as e:
        print(f"Failed to send email: Invalid recipient email address - {email}")
       
    except Exception as e:
        print(f"Failed to send email: {e}")
        
        
        
#order conformation email

@orders.post("/send_order_conformation")
def send_order_conformation(order_id:str):
   db_order = db.query(Orders).filter(Orders.id == order_id).first()
    
   if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
   db_cart = db.query(Cart).filter(Cart.id == db_order.cart_id).first()
    
   if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found for the order")
    
   cart_products = db.query(Product).filter(Product.cart_id == db_cart.id).all()
    
   if not cart_products:
        raise HTTPException(status_code=404, detail="No products found in the cart")
    
   user_id = db_order.user_id
   user = db.query(User).filter(User.id == user_id).first()
    
   if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
   if not user.email:
        raise HTTPException(status_code=400, detail="User email not provided")
    
 
   send_order_confirmation_email(user.email, db_order)
    
   return {"message": "Order confirmation email sent successfully"}
