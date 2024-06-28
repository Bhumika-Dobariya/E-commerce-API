from sqlalchemy import Column,String,DateTime,Boolean,ForeignKey,Integer,Float
from database.database import Base
from datetime import datetime
import uuid

class Cart(Base):
    
    __tablename__ = 'carts'
    
    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    user_id = Column(String(50), ForeignKey('user.id'), nullable=False)
    product_id = Column(String(50), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float(10, 2), nullable=False)
    total_price = Column(Float(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.now)  
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.utcnow) 
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)