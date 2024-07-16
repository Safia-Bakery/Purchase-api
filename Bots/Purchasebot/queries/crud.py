from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz

from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from orders.models import orders


from Bots.Purchasebot.database import SessionLocal




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




def get_client(id):
    with SessionLocal() as db:
        query = db.query(orders.Clients).filter(orders.Clients.id==id).first()
        return query


def create_user(name,id,phone_number):
    with SessionLocal() as db:
        query = orders.Clients(id=id,name=name,phone=phone_number)
        CommitDb().insert_data(db,query)
        return query



def get_orders(id:Optional[int]=None,client_id:Optional[int]=None):
    db = SessionLocal()
    query = db.query(orders.Expanditure)
    if id is not None:
        query = query.filter(orders.Expanditure.id==id)
    if client_id is not None:
        query = query.filter(orders.Expanditure.client_id==client_id)
    return query.all()








