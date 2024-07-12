from sqlalchemy import Column,String,DateTime,Boolean,CheckConstraint
from database.database import Base
from datetime import datetime
import uuid



class User(Base):
    
    __tablename__ = 'user'
    
    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    first_name = Column(String(50),nullable=False)
    last_name = Column(String(50),nullable=False)
    user_name = Column(String(50),nullable=False)
    password =Column(String(70),nullable= False)
    email = Column(String(50),nullable= False,unique=True)
    mob_no = Column(String(10),nullable= False)
    address = Column(String(100),nullable= False)
    created_at = Column(DateTime,default=datetime.now)
    modified_at = Column(DateTime,default=datetime.now,onupdate=datetime.now)
    is_active = Column(Boolean, default= True)
    is_deleted = Column(Boolean, default= False)
    is_verified = Column(Boolean, default=False)
    
# Add a CHECK constraint for the mobile number length
    __table_args__ = (
        CheckConstraint('length(mo_number) = 10', name='check_mo_number_length'),
    )
    