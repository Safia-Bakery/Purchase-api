from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from orders.models.orders import Orders, Categories
from orders.schemas import order_sch

def create_category(db: Session, category: order_sch.CategoryCreate):
    db_category = Categories(
        name_uz=category.name_uz,
        name_ru=category.name_ru,
        status=category.status
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session,name,status,id):
    query = db.query(Categories)
    if name is not None:
        query = query.filter(or_(Categories.name_uz == name, Categories.name_ru == name))
    if status is not None:
        query = query.filter(Categories.status == status)
    if id is not None:
        query = query.filter(Categories.id == id)
    return query.order_by(Categories.name_uz.desc()).all()


def update_category(db: Session, category: order_sch.CategoryUpdate):
    db_category = db.query(Categories).filter(Categories.id == category.id).first()
    if category.name_uz is not None:
        db_category.name_uz = category.name_uz
    if category.name_ru is not None:
        db_category.name_ru = category.name_ru
    if category.status is not None:
        db_category.status = category.status
    db.commit()
    db.refresh(db_category)
    return db_category 


def create_order(db: Session,user_id,brend,product,role,sertificate,brochure,category_id,safia_worker):
    db_order = Orders(
        user_id=user_id,
        brend=brend,
        product=product,
        role=role,
        sertificate=sertificate,
        brochure=brochure,
        category_id=category_id,
        safia_worker=safia_worker
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session,user_id,status,id):
    query = db.query(Orders)
    if user_id is not None:
        query = query.filter(Orders.user_id == user_id)
    if status is not None:
        query = query.filter(Orders.status == status)
    if id is not None:
        query = query.filter(Orders.id == id)
    return query.all()


def update_order(db: Session, order: order_sch.OrderUpdate):
    db_order = db.query(Orders).filter(Orders.id == order.id).first()
    if order.status is not None:
        db_order.status = order.status
    db.commit()
    db.refresh(db_order)
    return db_order



