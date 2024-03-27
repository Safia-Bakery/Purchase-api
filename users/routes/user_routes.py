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
    send_sms
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
    user = query.user_create(db=db, user=form_data)
    randomnumber = random.randint(100000,999999)
    query.user_update(db=db,id=user.id,otp="1234")
    send_sms(user.phone,randomnumber)
    #current_user: user_sch.User = Depends(get_current_user)
    return user

@user_router.get("/me", response_model=user_sch.User, summary="Get current user",tags=["User"])
async def current_user(db:Session=Depends(get_db),current_user: user_sch.User = Depends(get_current_user)):
    return current_user


@user_router.post('/verify',summary="Verify user",tags=["User"])
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
            query.user_update(db=db,id=user.id,status=1)
            tokens = {
                "access_token": create_access_token(user.username),
                "refresh_token": create_refresh_token(user.username),
            }
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
    user = query.get_user_byphone(db, phone_number=form_data.phone_number.replace('+',''),email=form_data.email)
    if user:
        randomnumber = random.randint(100000,999999)
        query.user_update(db=db,id=user.id,otp="1234",status=0)
        send_sms(user.phone,randomnumber)
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




