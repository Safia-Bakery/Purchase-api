from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    DateTime,
    Boolean,
    BIGINT,
    Table,
    Time,
    JSON,
    VARCHAR,
    Date,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from datetime import datetime
import pytz
import uuid
from users.models.users import Base

timezonetash = pytz.timezone("Asia/Tashkent")

class Categories(Base):
    __tablename__ = "categories"
    id = Column(BIGINT, primary_key=True, index=True)
    name_uz = Column(String, unique=True, index=True)
    name_ru = Column(String, unique=True, index=True)
    status = Column(Integer,default=1)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    order = relationship("Orders", back_populates="category")


class Orders(Base):
    __tablename__ = "orders"
    id = Column(BIGINT, primary_key=True, index=True)
    user_id = Column(BIGINT, ForeignKey("users.id"))
    user = relationship("Users", back_populates="order")
    status = Column(Integer,default=0)
    brend = Column(String,nullable=True)  
    product = Column(String,nullable=True)
    role = Column(String,nullable=True)
    sertificate = Column(String,nullable=True)
    brochure = Column(String,nullable=True) 
    category_id = Column(BIGINT, ForeignKey("categories.id"))
    category = relationship("Categories", back_populates="order")
    safia_worker = Column(Boolean,nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    

