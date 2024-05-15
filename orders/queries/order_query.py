from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from services import find_hierarchy
from uuid import UUID
from orders.models.orders import Orders, Categories, Branchs, Clients, ToolParents,Tools,Expanditure,ExpenditureTools
from orders.schemas import order_sch

timezonetash = pytz.timezone("Asia/Tashkent")   

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
    return query.order_by(Orders.id.desc()).all()


def update_order(db: Session, order: order_sch.OrderUpdate):
    db_order = db.query(Orders).filter(Orders.id == order.id).first()
    if order.status is not None:
        db_order.status = order.status
    db.commit()
    db.refresh(db_order)
    return db_order



from sqlalchemy.exc import SQLAlchemyError
def commitdata(db: Session, item):
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError as e:
        db.rollback()
        return False



def synchgroups(db: Session, groups):
    # here first is arc second is inventory
    group_list = [[],[]]
    arc_data = find_hierarchy(groups,'1b55d7e1-6946-4bbc-bf93-542bfdb2b584')


    for line in arc_data:
        group_list[1].append(line["id"])
        item = ToolParents(
            id=line["id"],
            num=line["num"],
            code=line["code"],
            name=line["name"],
            category=line["category"],
            description=line["description"],
            parent_id=line["parent"],
        )
        commitdata(db, item)
    return group_list




def get_or_update(db:Session,price,name,num,id,code,producttype,mainunit,department,parent_id):
    query = db.query(Tools).filter(Tools.iikoid==id).first()
    if query:
        query.department=department
        query.last_update=datetime.now(timezonetash)
        db.commit()
        db.refresh(query)
        return query
    else:
        toolsmod = Tools(
            price=price,
            iikoid=id,
            name=name,
            num=num,
            code=code,
            producttype=producttype,
            mainunit=mainunit,
            department=department,
            parentid=parent_id

        )
        commitdata(db, toolsmod)
    return query


def synchproducts(db: Session, grouplist, products):
    for i in products:
        parentId = i["parent"]
        name = i["name"]
        num = i["num"]
        code = i["code"]
        producttype = i["type"]
        mainunit = i["mainUnit"]
        id = i["id"]
        price = i["defaultSalePrice"]
        get_or_update(db,price,name,num,id,code,producttype,mainunit,1,parentId)
        
    return True


def getarchtools(db: Session,parent_id):
    query = db.query(ToolParents)
    query = query.filter(ToolParents.parent_id==parent_id)
    return query.all()


def tools_query_iarch(db: Session, parent_id,name):
    query = db.query(Tools)
    if parent_id is not None:
        query = query.filter(Tools.parentid == str(parent_id)).filter(Tools.status==1)
        if name is not None:
            query = query.filter(Tools.name.ilike(f"%{name}%"))
        query = query.all()
    else:
        return []
    return query



def searchtools(db: Session,name,id):
    query = db.query(Tools)
    if name is not None:
        query = query.filter(Tools.name.ilike(f"%{name}%")).filter(Tools.status==1)
    if id is not None:
        query = query.filter(Tools.id == id)
    return query.all()


def get_branchs(db: Session,name,status,id):
    query = db.query(Branchs)
    if name is not None:
        query = query.filter(Branchs.name.ilike(f"%{name}%"))
    if status is not None:
        query = query.filter(Branchs.status == status)
    if id is not None:
        query = query.filter(Branchs.id == id)
    return query.order_by(Branchs.name.desc()).all()


def check_data_exist(db: Session, name: str):
    return (
        db.query(Branchs).filter(Branchs.name == name).first()
    )


def insert_fillials(db: Session, items):
    for item in items:
        existing_item = check_data_exist(db, name=item[0])
        if existing_item:
            continue
        new_item = Branchs(
             name=item[0], status=1
        )
        commitdata(db, new_item)
    return True


def create_expanditure(db: Session, expanditure: order_sch.ExpanditureCreate):
    db_expanditure = Expanditure(
        client_id=expanditure.client_id,
        branch_id=expanditure.branch_id,
        comment=expanditure.comment
    )
    db.add(db_expanditure)
    db.commit()
    db.refresh(db_expanditure)
    for key, value in expanditure.tools.items():
        tool = db.query(Tools).filter(Tools.id == key).first()
        if tool:
            db_expenditure_tool = ExpenditureTools(
                tool_id=tool.id,
                expenditure_id=db_expanditure.id,
                amount=value
            )
            db.add(db_expenditure_tool)
            db.commit()
           
    return db_expanditure.id


def get_expanditure(db: Session, id,client_id,branch_id,status):
    query = db.query(Expanditure)
    if id is not None:
        query = query.filter(Expanditure.id == id)
    if client_id is not None:
        query = query.filter(Expanditure.client_id==client_id)
    if branch_id is not None:
        query = query.filter(Expanditure.branch_id==branch_id)
    if status is not None:
        query = query.filter(Expanditure.status == status)
    return query.order_by(Expanditure.id.desc()).all()

def update_expanditure(db:Session,form_data:order_sch.ExpanditureUpdate):
    query  = db.query(Expanditure).filter(Expanditure.id == form_data.id).first()
    if form_data.tools is not None:
        # querydelete = db.query(ExpenditureTools).filter(ExpenditureTools.expenditure_id==query.id).delete()
        # db.commit()
        for key, value in form_data.tools.items():
            tool = db.query(Tools).filter(Tools.id == key).first()
            if tool:
                db_expenditure_tool = ExpenditureTools(
                    tool_id=tool.id,
                    expenditure_id=query.id,
                    amount=value
                )
                db.add(db_expenditure_tool)
                db.commit()

    return query


def get_clients(db: Session, name, status, id):
    query = db.query(Clients)
    if name is not None:
        query = query.filter(Clients.name.ilike(f"%{name}%"))
    if status is not None:
        query = query.filter(Clients.status == status)
    if id is not None:
        query = query.filter(Clients.id == id)
    return query.order_by(Clients.name.desc()).all()


def update_clients(db:Session,form_data:order_sch.UpdateClients):
    query = db.query(Clients).filter(Clients.id==form_data.id).first()
    if query:
        if form_data.name is not None:
            query.name = form_data.name
        if form_data.status is not None:
            query.status = form_data.status
        db.commit()
        db.refresh(query)
    return query


def delate_card_item(db:Session,form_data:order_sch.DeleteCartItems):
    query = db.query(ExpenditureTools).filter(ExpenditureTools.id==form_data.id).delete()
    db.commit()
    return query


def update_expanditure_tools(db:Session,form_data:order_sch.ExpanditureTools):
    query = db.query(ExpenditureTools).filter(ExpenditureTools.id==form_data.id).first()
    if query:
        if form_data.amount is not None:
            query.amount = form_data.amount
        db.commit()
        db.refresh(query)
    return query