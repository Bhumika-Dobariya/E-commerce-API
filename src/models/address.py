from sqlalchemy import Column,String,DateTime,ForeignKey,Boolean
from database.database import Base
from datetime import datetime
import uuid


class Address(Base):
    
    __tablename__ = 'address'
    
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    city = Column(String(20),nullable=False)
    state = Column(String(20),nullable=False)
    zip_code = Column(String(10),nullable=True)
    user_id = Column(String(50),ForeignKey('user.id'),nullable=False)
    created_at = Column(DateTime, default=datetime.now)  
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.utcnow) 
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    