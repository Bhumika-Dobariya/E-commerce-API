from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey,Boolean
from database.database import Base
from datetime import datetime
import uuid

class Category(Base):
    
    __tablename__ = 'categories'


    id = Column(String(70), primary_key=True, default=str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=False)
    parent_id = Column(String(70), ForeignKey('categories.id'), nullable=False) 
    created_at = Column(DateTime, default=datetime.now())
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
