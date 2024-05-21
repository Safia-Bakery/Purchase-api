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


class Files(Base):
    __tablename__ = "files"
    id = Column(BIGINT, primary_key=True, index=True)
    url = Column(String,nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    relation = relationship("FilesRelations", back_populates="file")



class FilesRelations(Base):
    __tablename__ = "files_relations"
    id = Column(BIGINT, primary_key=True, index=True)
    file_id = Column(BIGINT, ForeignKey("files.id"))
    file = relationship("Files", back_populates="relation")
    order_id = Column(BIGINT, ForeignKey("orders.id"))
    type = Column(String,nullable=True)
    order = relationship("Orders", back_populates="file")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



class Orders(Base):
    __tablename__ = "orders"
    id = Column(BIGINT, primary_key=True, index=True)
    user_id = Column(BIGINT, ForeignKey("users.id"))
    user = relationship("Users", back_populates="order")
    status = Column(Integer,default=0)
    brend = Column(String,nullable=True)  
    product = Column(String,nullable=True)
    role = Column(String,nullable=True)
    deny_reason = Column(String,nullable=True)
    category_id = Column(BIGINT, ForeignKey("categories.id"))
    category = relationship("Categories", back_populates="order")
    safia_worker = Column(Boolean,nullable=True)
    price = Column(Float,nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    file = relationship("FilesRelations", back_populates="order")



class Branchs(Base):
    __tablename__ = "branchs"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    expanse = relationship("Expanditure", back_populates="branch")
    status = Column(Integer,default=1)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())




class Clients(Base):
    __tablename__ = "clients"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    phone = Column(String,nullable=True)
    status = Column(Integer,default=1)
    expanse = relationship("Expanditure", back_populates="client")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



class ToolParents(Base):
    __tablename__ = "toolparents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    num = Column(String, nullable=True)
    code = Column(String, nullable=True)
    name = Column(String)
    parent_id = Column(UUID(as_uuid=True), nullable=True)
    category = Column(String, nullable=True)
    description = Column(String, nullable=True)


class Tools(Base):
    __tablename__ = "tools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    num = Column(String, nullable=True)
    code = Column(String, nullable=True)
    iikoid = Column(String, unique=True)
    producttype = Column(String, nullable=True)
    price = Column(Float)
    parentid = Column(String)
    mainunit = Column(String, nullable=True)
    expandituretool = relationship("ExpenditureTools", back_populates="tool")
    total_price = Column(Float, nullable=True)
    amount_left = Column(Float, nullable=True)
    sklad_id = Column(ARRAY(UUID(as_uuid=True)), default=[])
    last_update = Column(DateTime(timezone=True))
    department = Column(Integer, nullable=True)
    min_amount = Column(Float, nullable=True)
    max_amount = Column(Float, nullable=True)
    image = Column(String, nullable=True)
    ftime = Column(Float, nullable=True)
    status= Column(Integer, default=1)



class Expanditure(Base):
    __tablename__ = "expanditure"
    id = Column(BIGINT, primary_key=True, index=True)
    client_id = Column(BIGINT, ForeignKey("clients.id"))
    client = relationship("Clients", back_populates="expanse")
    branch_id = Column(BIGINT, ForeignKey("branchs.id"))
    branch = relationship("Branchs", back_populates="expanse")
    comment = Column(String, nullable=True)
    name = Column(String,nullable=True)
    status = Column(Integer,default=0)
    deny_reason = Column(String,nullable=True)
    expendituretool = relationship("ExpenditureTools", back_populates="expenditure")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ExpenditureTools(Base):
    __tablename__ = "expendituretools"
    id = Column(BIGINT, primary_key=True, index=True)
    tool_id = Column(Integer, ForeignKey("tools.id"))
    tool = relationship("Tools", back_populates="expandituretool")
    expenditure_id = Column(BIGINT, ForeignKey("expanditure.id"))
    expenditure = relationship("Expanditure", back_populates="expendituretool")
    amount = Column(Float)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    












