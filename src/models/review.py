from sqlalchemy import Column,Integer,String,ForeignKey,Boolean
from database.database import Base
from datetime import datetime
import uuid

class ProductReview(Base):
    __tablename__ = "reviews"

    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))  
    user_id = Column(String(50), ForeignKey('user.id'), nullable=False)
    product_id = Column(String(50), nullable=False)
    comment = Column(String(200),nullable=False)
    rating = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)