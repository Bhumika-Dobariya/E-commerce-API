from sqlalchemy import Column,String,DateTime,ForeignKey,Boolean,Integer,Float,Text
from database.database import Base
from datetime import datetime
import uuid


class ShippingItem(Base):
    
    
    __tablename__ = "shipping_items"

    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    item_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    weight = Column(Float(10, 2), nullable=False)  # in kilograms

class Shipping(Base):
    
    
    __tablename__ = "shippings"

    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    address_id = Column(String(50), ForeignKey("address.id"), nullable=False)
    shipping_method = Column(String(100), nullable=False)
    shipping_cost = Column(Float(10, 2), nullable=False)
    carrier_name = Column(String(100), nullable=False)
    estimated_delivery = Column(String(100), nullable=False)
    tracking_number = Column(String(100), unique=True)
    shipping_date = Column(DateTime, default=datetime.now)
    delivery_status = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)