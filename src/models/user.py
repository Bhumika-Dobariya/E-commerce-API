from sqlalchemy import Column,String,DateTime,Boolean
from database.database import Base
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = 'UserInfo'
    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    first_name = Column(String(50),nullable=False)
    last_name = Column(String(50),nullable=False)
    user_name = Column(String(50),nullable=False)
    password =Column(String(70),nullable= False)
    email = Column(String(50),nullable= False)
    mob_no = Column(String(20),nullable= False)
    address = Column(String(100),nullable= False)
    created_at = Column(DateTime,default=datetime.now)
    modified_at = Column(DateTime,default=datetime.now,onupdate=datetime.now)
    is_active = Column(Boolean, default= True)
    is_deleted = Column(Boolean, default= False)
    
