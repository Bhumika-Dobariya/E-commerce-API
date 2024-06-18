from sqlalchemy import Column,String,DateTime,Boolean,ForeignKey,Float
from database.database import Base
from datetime import datetime
import uuid


class Payment(Base):
    
    __tablename__ = 'payments'
    
    id = Column(String(50), primary_key=True, default=str(uuid.uuid4())) 
    user_id = Column(String(50), ForeignKey('UserInfo.id'), nullable=False)
    cart_id = Column(String(50),ForeignKey("carts.id"),nullable=False)
    order_id = Column(String(50),ForeignKey("order.id"), nullable=True)
    amount = Column(Float(10,3),nullable=False)
    payment_method = Column(String(20),nullable=False)
    card_holder_name = Column(String(100), nullable=False) 
    card_number = Column(String(16), nullable=False)
    cvv = Column(String(4), nullable=False)
    expiry_month = Column(String(2), nullable=False)
    expiry_year = Column(String(4), nullable=False)
    currency = Column(String(3), default='INR') 
    status = Column(String, nullable=False, default="pending")
    payment_date = Column(DateTime, nullable=False)
    transaction_id = Column(String(50), nullable=True)
    billing_address = Column(String(255), nullable=False)
    shipping_address = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now) 
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)  
    is_active = Column(Boolean, default=True)     
    is_deleted = Column(Boolean, default=False)