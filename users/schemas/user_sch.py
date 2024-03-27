from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID


class User(BaseModel):
    id:int
    address:Optional[str]=None
    name: Optional[str]=None
    inn: Optional[str]=None
    email: Optional[str]=None
    company_name: Optional[str]=None
    phone: Optional[str]=None
    status: int
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    #username:str
    password:str
    address:Optional[str]=None
    name: Optional[str]=None
    inn: Optional[str]=None
    email: Optional[str]=None
    company_name: Optional[str]=None
    phone: Optional[str]=None
    

class UserUpdate(BaseModel):
    #username:Optional[str]=None
    password:Optional[str]=None
    address:Optional[str]=None
    name: Optional[str]=None
    inn: Optional[str]=None
    email: Optional[str]=None
    company_name: Optional[str]=None
    phone: Optional[str]=None


class UserVerify(BaseModel):
    phone_number:Optional[str]=None
    otp:str
    email: Optional[str]=None

class ResetPhone(BaseModel):
    phone_number:Optional[str]=None
    email: Optional[str]=None


class ResetPassword(BaseModel):
    password:str




