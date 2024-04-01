from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from users.models.users import Users  
from users.schemas import user_sch


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")

def get_user(db: Session, username: str):
    return db.query(Users).filter(Users.username == username).first()

def get_user_byphone(db: Session, phone_number:Optional[str]=None, email:Optional[str]=None):
    query = db.query(Users)
    if phone_number is not None:

        query = query.filter(Users.username == phone_number.replace("+", ""))
    if email is not None:
        query = query.filter(Users.username == email)
    return query.first()

def user_create(db: Session, user: user_sch.UserCreate):
    hashed_password = hash_password(user.password)
    if user.phone is not None:
        user.phone = user.phone.replace("+", "")
        username = user.phone
    elif user.email is not None:
        username = user.email

    db_user = Users(
        username=username,
        hashed_password=hashed_password,
        address=user.address,
        name=user.name,
        inn=user.inn,
        email=user.email,
        company_name=user.company_name,
        phone=username,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def user_update(db:Session,id:int,status:Optional[int]=None,password:Optional[str]=None,otp:Optional[str]=None):
    db_user = db.query(Users).filter(Users.id == id).first()
    if status is not None:
        db_user.status = status
    if password is not None:
        db_user.hashed_password = hash_password(password)
    if otp is not None:
        db_user.otp = otp
    db.commit()
    db.refresh(db_user)
    return db_user

