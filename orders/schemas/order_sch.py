from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from users.schemas import user_sch



class CategoryCreate(BaseModel):
    name_uz: str
    name_ru: str
    status: Optional[int] = 1
    class Config:
        orm_mode = True



class CategoryUpdate(BaseModel):
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    status: Optional[int] = None
    id:int
    class Config:
        orm_mode = True

class GetCategory(BaseModel):
    id:int
    name_uz: str
    name_ru: str
    status: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        orm_mode = True



class GetOrders(BaseModel):
    id:int
    user_id: int
    status: int
    brend: Optional[str] = None
    product: Optional[str] = None
    role: Optional[str] = None
    sertificate: Optional[str] = None
    brochure: Optional[str] = None
    category_id: int
    category: Optional[GetCategory] = None
    safia_worker: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user:Optional[user_sch.User] = None
    class Config:
        orm_mode = True

#test


class OrderUpdate(BaseModel):
    id:int
    status: Optional[int] = None
