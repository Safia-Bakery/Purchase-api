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

# class ParentPermissions(Base):
#     __tablename__ = "parent_permissions"
#     id = Column(BIGINT, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)
#     description = Column(String,nullable=True)
#     status = Column(Integer,default=1)
#     created_at = Column(DateTime(timezone=True), default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
#     permission = relationship("Permissions", back_populates="parent")
#
# class Permissions(Base):
#     __tablename__ = "permissions"
#     id = Column(BIGINT, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)
#     description = Column(String,nullable=True)
#     parent_id = Column(BIGINT, ForeignKey("parent_permissions.id"))
#     parent = relationship("ParentPermissions", back_populates="permission")
#     status = Column(Integer,default=1)
#     created_at = Column(DateTime(timezone=True), default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
#     access = relationship("Accesses", back_populates="permission")
#
#
# class Accesses(Base):
#     __tablename__ = "accesses"
#     id = Column(BIGINT, primary_key=True, index=True)
#     role_id = Column(BIGINT, ForeignKey("roles.id"))
#     role = relationship("Roles", back_populates="access")
#     permission_id = Column(BIGINT, ForeignKey("permissions.id"))
#     permission = relationship("Permissions", back_populates="access")
#     status = Column(Integer,default=1)
#     created_at = Column(DateTime(timezone=True), default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
#
# class Roles(Base):
#     __tablename__ = "roles"
#     id = Column(BIGINT, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)
#     description = Column(String,nullable=True)
#     status = Column(Integer,default=1)
#     created_at = Column(DateTime(timezone=True), default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
#     access = relationship("Accesses", back_populates="role")
#     user = relationship("Users", back_populates="role")

# this is models of users
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
    #role_id = Column(BIGINT, ForeignKey("roles.id"))
    #role = relationship("Roles", back_populates="user")
    order = relationship("Orders", back_populates="user")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



