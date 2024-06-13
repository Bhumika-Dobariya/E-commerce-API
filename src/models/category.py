from sqlalchemy import Column,String,DateTime,Boolean,Text
from database.database import Base
from datetime import datetime
import uuid



class Category(Base):
    
    __tablename__ = 'categories'

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4())) 
    name = Column(String(255), nullable=False)         
    description = Column(Text, nullable=False)           
    created_at = Column(DateTime, default=datetime.now)  
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.utcnow) 
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)