from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from users.models.users import Users,Permissions,Accesses,ParentPermissions,Roles
from users.schemas import user_sch


class CommitDb():
    def insert_data(self,db:Session,data):
        try:
            db.add(data)
            db.commit()
            db.refresh(data)
            return data
        except Exception as e:
            db.rollback()
            return False

    def update_data(self,db:Session,data):
        try:
            db.commit()
            db.refresh(data)
            return data
        except:
            db.rollback()
            return False

    def delete_data(self,db:Session,data):

        try:
            db.delete(data)
            db.commit()
            return data
        except:
            db.rollback()
            return False

    def get_data(self,db:Session,data):
        try:
            return data
        except:
            return False
        finally:
            #db.close()
            return True





def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")

def get_user(db: Session, username: str):
    username = username.replace("+", "")
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
        role_id=user.role_id
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



def users_update_body(db:Session,form_data:user_sch.UserUpdate):
    db_user = db.query(Users).filter(Users.id == form_data.id).first()
    if db_user:
        if form_data.name is not None:
            db_user.name = form_data.name
        if form_data.address is not None:
            db_user.address = form_data.address
        if form_data.email is not None:
            db_user.email = form_data.email
        if form_data.inn is not None:
            db_user.inn = form_data.inn
        if form_data.company_name is not None:
            db_user.company_name = form_data.company_name
        if form_data.phone is not None:
            db_user.phone = form_data.phone
        if form_data.role_id is not None:
            db_user.role_id = form_data.role_id
        if form_data.status is not None:
            db_user.status = form_data.status
        db = CommitDb().update_data(db,db_user)
    return db_user




def create_roles(db:Session,form_data:user_sch.RoleCreate):
    query = Roles(name=form_data.name,description=form_data.description,status=form_data.status)
    query = CommitDb().insert_data(db,query)
    for access in form_data.accesses:
        add_access = Accesses(role_id=query.id,permission_id=access)
        CommitDb().insert_data(db,add_access)

    return query


def update_roles(db:Session,form_data:user_sch.RoleUpdate):
    query = db.query(Roles).filter(Roles.id == form_data.id).first()
    if query:
        query.name = form_data.name
        query.description = form_data.description
        query.status = form_data.status
        query = CommitDb().update_data(db,query)

        if form_data.accesses is not None:
            delete_access = db.query(Accesses).filter(Accesses.role_id == form_data.id).delete()
            db.commit()
            for access in form_data.accesses:
                add_access = Accesses(role_id=query.id,permission_id=access)
                CommitDb().insert_data(db,add_access)

    return query



def get_roles(db:Session,id:Optional[int]=None):
    query = db.query(Roles)
    if id is not None:
        query = query.filter(Roles.id == id)
    return query.all()



def get_users(db:Session,id:Optional[int]=None):
    query = db.query(Users)
    if id is not None:
        query = query.filter(Users.id == id)
    return query.all()



def get_permissions(db:Session):
    query = db.query(Permissions)

    return query.all()


def get_purchasers(db:Session):
    query = db.query(Users).join(Roles).filter(Roles.name.ilike("%Закупщик%")) #.filter(Roles.name.ilib ke("%Закупщик%"))

    return query.all()

