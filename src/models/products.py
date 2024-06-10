from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey,Boolean
from database.database import Base
from datetime import datetime
import uuid


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    name = Column(String(50),nullable=False)
    description = Column(String(200),nullable=False)
    price = Column(Float(50),nullable=False)
    category_id = Column(String, ForeignKey('categories.id'),default=str(uuid.uuid4()),nullable=False)
    stock_quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    modified_at = Column(DateTime,default=datetime.now,onupdate=datetime.now)
    is_active = Column(Boolean, default= True)
    is_deleted = Column(Boolean, default= False)
