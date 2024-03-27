from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status,Form,UploadFile
from fastapi_pagination import paginate, Page, add_pagination
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional,Annotated
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uuid import UUID
from services import (
    create_access_token,
    create_refresh_token,
    get_db,
    get_current_user,
    verify_password,
    verify_refresh_token,
    generate_random_filename
)
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import engine, SessionLocal
from orders.queries import order_query
from orders.schemas import order_sch   
from users.schemas import user_sch 
from dotenv import load_dotenv
import os
load_dotenv()


order_router = APIRouter()



@order_router.post("/category", summary="Create category",tags=["Order"])
async def create_category(
    category: order_sch.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    return order_query.create_category(db, category)

@order_router.get("/category", summary="Get categories",tags=["Order"],response_model=Page[order_sch.GetCategory])
async def get_categories(
    name: Optional[str] = None,
    status: Optional[int] = None,
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    return paginate(order_query.get_categories(db, name, status, id))

@order_router.put("/category", summary="Update category",tags=["Order"])
async def update_category(
    category: order_sch.CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    return order_query.update_category(db, category)



@order_router.post("/order", summary="Create order",tags=["Order"])
async def create_order(
    brend:Annotated[str, Form()]=None,
    product:Annotated[str, Form()]=None,
    role:Annotated[str, Form()]=None,
    sertificate:UploadFile = None,
    brochure:UploadFile = None,
    category_id:Annotated[int, Form()]=None,
    safia_worker:Annotated[bool, Form()]=None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    if sertificate is not None:
        # for file in image:
        folder_name = f"files/{generate_random_filename()+sertificate.filename}"
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await sertificate.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        sertificate = folder_name
    else:
        sertificate = None
    if brochure is not None:
        # for file in image:
        folder_name = f"files/{generate_random_filename()+brochure.filename}"
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await brochure.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        brochure = folder_name
    else:
        brochure = None
    return order_query.create_order(db=db, user_id=current_user.id, brend=brend, product=product, role=role, sertificate=sertificate, brochure=brochure, category_id=category_id, safia_worker=safia_worker)



@order_router.get("/order", summary="Get orders",tags=["Order"],response_model=Page[order_sch.GetOrders])
async def get_orders(
    user_id: Optional[int] = None,
    status: Optional[int] = None,
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    return paginate(order_query.get_orders(db,user_id= user_id, status=status,id=id))

@order_router.put("/order", summary="Update order",tags=["Order"])
async def update_order(
    order: order_sch.OrderUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    return order_query.update_order(db, order)


