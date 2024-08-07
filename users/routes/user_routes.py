from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi_pagination import paginate, Page, add_pagination
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uuid import UUID
import random
from services import (
    create_access_token,
    create_refresh_token,
    get_db,
    get_current_user,
    verify_password,
    verify_refresh_token,
    send_sms,
    send_email
)
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import engine, SessionLocal

from dotenv import load_dotenv
import os
load_dotenv()
from users.queries import query
from users.schemas import user_sch


user_router = APIRouter()



@user_router.post("/login", summary="Create access and refresh tokens for user",tags=["User"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    db: Session = Depends(get_db),
):
    user = query.get_user(db, form_data.username)
    if user is None or user.status == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password or user is inactive",
        )


    hashed_pass = user.hashed_password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }



@user_router.post("/refresh",response_model=user_sch.User, summary="Refresh access token",tags=["User"])
async def refresh(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    username = verify_refresh_token(refresh_token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid refresh token",
        )
    return {"access_token": create_access_token(username)}



@user_router.post("/register",response_model=user_sch.User, summary="Register a new user",tags=["User"])
async def register(
    form_data: user_sch.UserCreate,
    db: Session = Depends(get_db)):
    #get_user = query.get_user_byphone(db, email=form_data.email,phone_number=form_data.phone)
    #if get_user:
    if form_data.phone is None and form_data.email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data",
        )
    try:
        user = query.user_create(db=db, user=form_data)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="already have an account",
        )
    randomnumber = random.randint(100000,999999)
    query.user_update(db=db,id=user.id,otp=randomnumber,status=0)

    if user.phone is not None:
        send_sms(user.phone,f"Код подтверждения для сайта Safia Purchase: {randomnumber}")
    elif user.email is not None:
        send_email(user.email,randomnumber)
    #current_user: user_sch.User = Depends(get_current_user)
    return user

@user_router.get("/me", response_model=user_sch.User, summary="Get current user",tags=["User"])
async def current_user(db:Session=Depends(get_db),current_user: user_sch.User = Depends(get_current_user)):

    if current_user is not None and current_user.role :
        permission_dict = {str(permission.permission_id): True for permission in current_user.role.access}
        current_user.permissions = permission_dict

    return current_user





@user_router.post('/verify', summary="Verify user", tags=["User"])
async def verify_user(
    form_data:user_sch.UserVerify,
    db: Session = Depends(get_db)
):
    if form_data.phone_number is not None and form_data.email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data",
        )
    user = query.get_user_byphone(db, phone_number=form_data.phone_number,email=form_data.email)
    if user:
        if user.otp == form_data.otp:
            if user.status!=2:
                query.user_update(db=db,id=user.id,status=1)
            tokens = {
                "access_token": create_access_token(user.username),
                "refresh_token": create_refresh_token(user.username),
            }
            #this isc comment
            return tokens
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect OTP",
            )
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found",
            )





@user_router.post('/forgot',summary="Forgot password",tags=["User"])
async def forgot_password(
    form_data:user_sch.ResetPhone,
    db: Session = Depends(get_db)
):
    if form_data.phone_number is not None:
        form_data.phone_number = form_data.phone_number.replace('+','')
    user = query.get_user_byphone(db, phone_number=form_data.phone_number,email=form_data.email)
    if user:
        randomnumber = random.randint(100000,999999)
        if user.status!=2:
            query.user_update(db=db,id=user.id,otp=randomnumber,status=0)
        else:
            query.user_update(db=db,id=user.id,otp=randomnumber)
        if form_data.phone_number is not None:
            send_sms(user.phone,f"Код подтверждения для сайта Safia Purchase: {randomnumber}")
        if form_data.email is not None:
            send_email(form_data.email, randomnumber)
        return {"message":"OTP sent"}
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found",
            )




@user_router.post('/reset',summary="Reset password",tags=["User"])
async def reset_password(
    form_data:user_sch.ResetPassword,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    query.user_update(db=db,id=current_user.id,password=form_data.password)
    return {"message":"Password reset successfully",'success':True}


@user_router.post('/role',summary="Create role",tags=["User"])
async def create_role(
    form_data:user_sch.RoleCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):

    role = query.create_roles(db=db,form_data=form_data)
    return role


@user_router.put('/role',summary="Update role",tags=["User"])
async def update_role(
    form_data:user_sch.RoleUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    role = query.update_roles(db=db,form_data=form_data)
    return role

@user_router.get('/roles',summary="Get roles",tags=["User"])
async def get_roles(
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    roles = query.get_roles(db)

    return roles

@user_router.get('/roles/{id}',summary="Get role",tags=["User"],response_model=user_sch.Roles)
async def get_role(
    id:int,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    role = query.get_roles(db,id=id)
    if role:
        return role[0]
    else:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role not found",
            )

@user_router.get('/permissions',summary="Get permissions",tags=["User"])
async def get_permissions(
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    permissions = query.get_permissions(db)

    return permissions




@user_router.get('/users',summary="Get users",tags=["User"],response_model=Page[user_sch.GetUsers])
async def get_users(
        id: Optional[int] = None,
    current_user: user_sch.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    users = query.get_users(db,id=id)
    return paginate(users)



@user_router.post('/users',summary="Create user",tags=["User"],response_model=user_sch.GetUsers)
async def create_user(
    form_data:user_sch.UserCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    user = query.user_create(db=db,user=form_data)
    return user


@user_router.put('/users',summary="Update user",tags=["User"],response_model=user_sch.GetUsers)
async def update_user(
    form_data:user_sch.UserUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    user = query.users_update_body(db=db,form_data=form_data)
    return user


@user_router.get('/purchasers',summary="Get Purchasers",tags=["User"],response_model=Page[user_sch.PurchasersGet])
async def get_purchasers(
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    users = query.get_purchasers(db)
    return paginate(users)

