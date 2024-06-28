from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey,Boolean,Text
from database.database import Base
from datetime import datetime
import uuid

class ProductReview(Base):
    __tablename__ = "reviews"

    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))  
    user_id = Column(String(50), ForeignKey('user.id'), nullable=False)
    product_id = Column(String(50), nullable=False)
    description = Column(String(200),nullable=False)
    stars = Column(Float)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)