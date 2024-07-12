from sqlalchemy import Column,String,DateTime,Boolean,ForeignKey,Integer,Float
from database.database import Base
from datetime import datetime
import uuid



class Orders(Base):
    
    __tablename__ = 'order'
      
    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    user_id = Column(String(50), ForeignKey('user.id'), nullable=False)
    product_id = Column(String(50), ForeignKey('products.id'), nullable=False)
    cart_id = Column(String(50), ForeignKey('carts.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String(100), nullable=False)
    total_price = Column(Float(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
