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
    vat: Optional[float] = None
    class Config:
        orm_mode = True

#test

#newtest
class OrderUpdate(BaseModel):
    id:int
    status: Optional[int] = None



class Branchs(BaseModel):
    id: int
    name: str
    status: Optional[int] = 1
    class Config:
        orm_mode = True




class Clients(BaseModel):
    id: int
    name: Optional[str]=None
    phone: Optional[str] = None
    status: Optional[int] = 1
    class Config:
        orm_mode = True



class Tools(BaseModel):
    id: int
    name: str
    status: Optional[int] = 1
    iiko_id: Optional[str] = None
    price: Optional[float]=None
    class Config:
        orm_mode = True


class ExpanditureCreate(BaseModel):
    client_id: int
    branch_id: int
    comment: Optional[str] = None
    tools: Dict[str, int]



class ExpanditureToolGet(BaseModel):
    id: int
    tool_id: int
    tool: Optional[Tools] = None
    amount: int
    class Config:
        orm_mode = True
    


class Expanditure(BaseModel):
    id: int
    client_id: int
    client: Optional[Clients] = None
    branch: Optional[Branchs] = None
    branch_id: int
    status: Optional[int] = None
    comment: Optional[str] = None
    name:Optional[str]=None
    expendituretool: Optional[list[ExpanditureToolGet]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        orm_mode = True



class ExpanditureUpdate(BaseModel):
    id: int
    status: Optional[int] = None
    comment: Optional[str] = None
    tools: Optional[Dict[str, int]]=None
    class Config:
        orm_mode = True


class UpdateClients(BaseModel):
    id:int
    status:Optional[int]=None
    name:Optional[str]=None


class DeleteCartItems(BaseModel):
    id:int



class ExpanditureTools(BaseModel):
    id: int
    amount: int
    class Config:
        orm_mode = True
