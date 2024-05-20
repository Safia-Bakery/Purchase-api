from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status,Form,UploadFile,File
from fastapi_pagination import paginate, Page, add_pagination
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional,Annotated,List
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uuid import UUID
from services import (
    create_access_token,
    create_refresh_token,
    get_db,
    get_current_user,
    verify_password,
    verify_refresh_token,
    generate_random_filename,
    get_token,
    getgroups,
    getproducts,
    authiiko,
    list_departments,
    send_sms,
generate_excell
)
from ..orderservices import get_prices,get_productsmainunit
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
    if current_user.status != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have permission to create category",
        )
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
    if current_user.status != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have permission to create category",
        )
    return order_query.update_category(db, category)


# from here you can create order
@order_router.post("/order", summary="Create order",tags=["Order"],response_model=order_sch.GetOrders)
async def create_order(
    category_id:Annotated[int, Form()],
    brend:Annotated[str, Form()]=None,
    product:Annotated[str, Form()]=None,
    role:Annotated[str, Form()]=None,
    sertificate:UploadFile = None,
    product_images:List[UploadFile] = File(...),
    brochure:UploadFile = None,
    safia_worker:Annotated[bool, Form()]=None,
    price:Annotated[float, Form()]=None,
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

    order_create = order_query.create_order(db=db,price=price, user_id=current_user.id, brend=brend, product=product, role=role, sertificate=sertificate, brochure=brochure, category_id=category_id, safia_worker=safia_worker)
    if product_images is not None:
        images = []
        for image in product_images:
            folder_name = f"files/{generate_random_filename()+image.filename}"
            with open(folder_name, "wb") as buffer:
                while True:
                    chunk = await image.read(1024)
                    if not chunk:
                        break
                    buffer.write(chunk)
            images.append(folder_name)

        order_query.create_images(db=db,order_id=order_create.id,images=images)
    return order_create





# from here you can create a new route for getting orders
@order_router.get("/order", summary="Get orders",tags=["Order"],response_model=Page[order_sch.GetOrders])
async def get_orders(
    user_id: Optional[int] = None,
    status: Optional[int] = None,
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    return paginate(order_query.get_orders(db,user_id= user_id, status=status,id=id))

@order_router.put("/order", summary="Update order",tags=["Order"])
async def update_order(
    order: order_sch.OrderUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    query = order_query.update_order(db, order)
    if order.status is not None:
        if order.status == 1:
            send_sms(query.user.phone_number, f"Уважаемый {query.user.name}, ваша заявка принята в работу, в скором времени с вами свяжется наш менеджер.")
            # send message to user
            pass

        if order.status == 2:
            send_sms(query.user.phone_number, "Ваша заявка обработана. Для дальнейшего обсуждения сотрудничества с вами свяжется менеджер нашего отдела закупок.")
            # send message to user
            pass
        if order.status == 3:
            send_sms(query.user.phone_number, f"К сожалению, ваша заявка была отклонена по причине {query.deny_reason}. С уважением, Отдел закупок, Safia.")
            pass


    return query







#printer hello worlkd in this world




@order_router.get("/synch", summary="Expenditure synch iiko",tags=["Expenditure"])
async def synch_expenditure(
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    key =authiiko()
    groups = getgroups(key=key)
    group_list = order_query.synchgroups(db, groups)
    del groups
    products = getproducts(key=key)
    product_list = order_query.synchproducts(db, grouplist=group_list, products=products)
    del products
    prices = get_prices(key=key,department_id='fe7dce09-c2d4-46b9-bab1-86be331ed641')
    order_query.update_products_price(db=db,prices=prices)
    del prices
    prices = get_prices(key=key,department_id='c39aa435-8cdf-4441-8723-f532797fbeb9')
    order_query.update_products_price(db=db,prices=prices)
    del prices
    mainunits = get_productsmainunit(key=key)
    order_query.update_measure_unit(db=db,measure_units=mainunits)
    del mainunits
    return {"message":"Hello world",'success':True}



@order_router.get("/clients",response_model=Page[order_sch.Clients])
async def get_clients(
    name: Optional[str] = None,
    status: Optional[int] = None,
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
    ):
    return paginate(order_query.get_clients(db,name=name,status=status,id=id))


@order_router.put('/clients',response_model=order_sch.Clients)
async def update_clients(
    form_data:order_sch.UpdateClients,
    db:Session=Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    return order_query.update_clients(db=db,form_data=form_data)
    
@order_router.get("/synch/departments", summary="Expenditure synch iiko",tags=["Expenditure"])
async def synch_departments(
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)):
    key =authiiko()
    
    departments = list_departments(key=key)
    department_list = order_query.insert_fillials(db, departments)
    return {"message":"Hello world"}



@order_router.get("/tool/iarch")
async def toolgroups(
    parent_id: Optional[UUID] = None,
    name:Optional[str]=None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
    ):
    data = {'folders':order_query.getarchtools(db,parent_id),'tools':order_query.tools_query_iarch(db,parent_id=parent_id,name=name)}
    return data



@order_router.get("/tool/search",response_model=Page[order_sch.Tools])
async def searchtools(
    name: Optional[str] = None,
    id: Optional[int] = None,
    db: Session = Depends(get_db)
    ):
    return paginate(order_query.searchtools(db,name=name,id=id))


@order_router.get("/branch",response_model=Page[order_sch.Branchs])
async def get_branchs(
    name: Optional[str] = None,
    status: Optional[int] = None,
    id: Optional[int] = None,
    db: Session = Depends(get_db)
    ):
    return paginate(order_query.get_branchs(db,name=name,status=status,id=id))





@order_router.post("/expanditure", summary="Create expanditure",tags=["Expenditure"])
async def create_expanditure(
    form_data: order_sch.ExpanditureCreate,
    db: Session = Depends(get_db)
):
    return {'success':True,'id':order_query.create_expanditure(db, form_data)}


@order_router.get("/expanditure", summary="Get expanditure",tags=["Expenditure"],response_model=Page[order_sch.Expanditure])
async def get_expanditure_router(
    id: Optional[int] = None,
    client_id: Optional[int] = None,
    branch_id: Optional[int] = None,
    status: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    query = paginate(order_query.get_expanditure(db, id=id,client_id=client_id,branch_id=branch_id,status=status))
    total_sum = 0
    if id is not None:
        for i in query.items[0].expendituretool:
            try:
                total_sum += i.amount * i.tool.price
            except:
                pass
    query.items[0].total_sum = total_sum

    return query



@order_router.put("/expanditure", summary="Update expanditure",tags=["Expenditure"])
async def update_expanditure(
    expanditure: order_sch.ExpanditureUpdate,
    db: Session = Depends(get_db)
):
    return order_query.update_expanditure(db, expanditure)

@order_router.delete('/expanditure/cart',summary='Delete cart items',tags=['Expenditure'] )
async def delete_cart_items(
    form_data:order_sch.DeleteCartItems,
    db:Session = Depends(get_db),
):
    return order_query.delate_card_item(db=db,form_data=form_data)

@order_router.get('/expanditure/mine',summary='get my expanditure',tags=['Expenditure'],response_model=Page[order_sch.Expanditure])
async def get_order_router(
    client_id:int,
    db:Session=Depends(get_db)):

    return paginate(order_query.get_expanditure(db=db,client_id=client_id,id=None))



@order_router.put('/expanditure/cart',summary='get expanditure tools',tags=['Expenditure'])
async def update_expanditure_tools(
    form_data:order_sch.ExpanditureTools,
    db:Session=Depends(get_db)):
    query =order_query.update_expanditure_tools(db=db,form_data=form_data)
    return query



@order_router.get('/expanditure/excell',summary='get excell',tags=['Expenditure'])
async def get_excell(
    id:Optional[int]=None,
    db:Session=Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    query = order_query.get_expanditure(db=db,id=id,client_id=None,branch_id=None,status=None)
    if query:
        file_name = generate_excell(data=query[0].expendituretool,db=db)
        return {'success':True,'file':file_name}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data found",
        )




