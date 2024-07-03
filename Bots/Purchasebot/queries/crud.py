from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz

from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from orders.models import orders







def get_client(db:Session,id):
    query = db.query(orders.Clients).filter(orders.Clients.id==id).first()
    return query


def create_user(db:Session,name,id,phone_number):
    query = orders.Clients(id=id,name=name,phone=phone_number)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def get_orders(db:Session,id:Optional[int]=None,client_id:Optional[int]=None):
    query = db.query(orders.Expanditure)
    if id is not None:
        query = query.filter(orders.Expanditure.id==id)
    if client_id is not None:
        query = query.filter(orders.Expanditure.client_id==client_id)
    return query.all()







