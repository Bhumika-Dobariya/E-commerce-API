from sqlalchemy import Column,String,DateTime,Boolean,ForeignKey
from database.database import Base
from datetime import datetime
import uuid


class OTPS(Base):
    __tablename__ = 'OTP'

    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    user_email = Column(String(50), ForeignKey('UserInfo.email'), nullable=False)  
    otp = Column(String(6), nullable=False)
    expiration_time = Column(DateTime, nullable=False, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)