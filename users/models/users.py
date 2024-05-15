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
from database import Base

timezonetash = pytz.timezone("Asia/Tashkent")

# this is models of userss
class Users(Base):  
    __tablename__ = "users"
    id = Column(BIGINT, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    address = Column(String,nullable=True)  
    name = Column(String,nullable=True)
    inn = Column(String,nullable=True)
    email = Column(String,nullable=True)
    company_name = Column(String,nullable=True) 
    phone = Column(String,nullable=True)
    status = Column(Integer,default=0)
    otp = Column(String,nullable=True)
    order = relationship("Orders", back_populates="user")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



