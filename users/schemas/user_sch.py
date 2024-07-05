from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID





class UserCreate(BaseModel):
    #username:str
    password:str
    address:Optional[str]=None
    name: Optional[str]=None
    inn: Optional[str]=None
    email: Optional[str]=None
    company_name: Optional[str]=None
    phone: Optional[str]=None
    role_id: Optional[int]=None
    

class UserUpdate(BaseModel):
    #username:Optional[str]=None
    id:int
    password:Optional[str]=None
    address:Optional[str]=None
    name: Optional[str]=None
    inn: Optional[str]=None
    email: Optional[str]=None
    company_name: Optional[str]=None
    phone: Optional[str]=None
    role_id: Optional[int]=None
    status: Optional[int]=None


class UserVerify(BaseModel):
    phone_number:Optional[str]=None
    otp:str
    email: Optional[str]=None

class ResetPhone(BaseModel):
    phone_number:Optional[str]=None
    email: Optional[str]=None


class ResetPassword(BaseModel):
    password:str


class Permissions(BaseModel):
    id:int
    name:Optional[str]=None
    status:Optional[int]=None
    description:Optional[str]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True


class ParentPermissions(BaseModel):
    id:int
    name:Optional[str]=None
    status:Optional[int]=None
    description:Optional[str]=None
    permission:Optional[list[Permissions]]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True


class Accesses(BaseModel):
    id:int
    role_id:int
    permission_id:int
    permission:Optional[Permissions]=None
    status:Optional[int]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True


class Roles(BaseModel):
    id:int
    name:Optional[str]=None
    description:Optional[str]=None
    status:Optional[int]=None
    access:Optional[list[Accesses]]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True


class RoleCreate(BaseModel):
    name:str
    description:Optional[str]=None
    status:Optional[int]=None
    accesses: Optional[list[int]]=None
    class Config:
        orm_mode = True


class RoleUpdate(BaseModel):
    id:int
    name:Optional[str]=None
    description:Optional[str]=None
    status:Optional[int]=None
    accesses: Optional[list[int]]=None
    class Config:
        orm_mode = True


class RoleGet(BaseModel):
    id:int
    name:Optional[str]=None
    description:Optional[str]=None
    status:Optional[int]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True


class User(BaseModel):
    id:int
    address:Optional[str]=None
    name: Optional[str]=None
    inn: Optional[str]=None
    email: Optional[str]=None
    company_name: Optional[str]=None
    phone: Optional[str]=None
    status: int
    permissions: Optional[dict]=None
    #role: Optional[Roles]=None
    class Config:
        orm_mode = True



class GetUsers(BaseModel):
    id:int
    address:Optional[str]=None
    name: Optional[str]=None
    inn: Optional[str]=None
    email: Optional[str]=None
    company_name: Optional[str]=None
    phone: Optional[str]=None
    status: int
    role: Optional[Roles]=None
    class Config:
        orm_mode = True


class PurchasersGet(BaseModel):
    id: int
    address: Optional[str] = None
    name: Optional[str] = None
    inn: Optional[str] = None
    email: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    status: int
    class Config:
        orm_mode = True





