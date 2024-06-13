from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey,Boolean,Text
from database.database import Base
from datetime import datetime
import uuid



class Product(Base):
    
    __tablename__ = "products"

    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))  
    name = Column(String(255), nullable=False)        
    description = Column(Text, nullable=False)           
    price = Column(Float(10,2), nullable=False)        
    category_id = Column(String(50), ForeignKey("categories.id"), nullable=False)
    stock_quantity = Column(Integer, default=0)        
    created_at = Column(DateTime, default=datetime.now) 
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.now)  
    is_active = Column(Boolean, default=True)     
    is_deleted = Column(Boolean, default=False)
    
    