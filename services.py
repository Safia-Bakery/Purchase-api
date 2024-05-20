from datetime import datetime, timedelta
import pytz
from jose import jwt
from passlib.context import CryptContext
import bcrypt
import random
import string

from sqlalchemy.orm import Session
from typing import Union, Any
from fastapi import (
    Depends,
    HTTPException,
    status,
)
from orders.queries.order_query import tools_query_iarch
import pandas as pd
import smtplib
from database import engine, SessionLocal
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordBearer
import xml.etree.ElementTree as ET
import os
from users.schemas import user_sch
#from schemas import user_schema
#from queries import user_query as crud
from dotenv import load_dotenv
import requests
from users.queries import query

load_dotenv()

LOGIN_IIKO = os.environ.get("LOGIN_IIKO")
PASSWORD_IIKO = os.environ.get("PASSWORD_IIKO")
BASE_URL = os.environ.get("BASE_URL")


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")  # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY") # should be kept secret
ALGORITHM = os.environ.get("ALGORITHM")


ESKIZ_BASE_URL = os.getenv("ESKIZ_BASE_URL")
ESKIZ_LOGIN = os.getenv("ESKIZ_LOGIN")
ESKIZ_PASSWORD = os.getenv("ESKIZ_PASSWORD")


SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_USERNAME=os.getenv('SMTP_USERNAME')
FROM_EMAIL = os.getenv('FROM_EMAIL')

smtp_port = 587


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt



async def get_current_user(
    token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)
) -> user_sch.User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        expire_date = payload.get("exp")
        sub = payload.get("sub")
        if datetime.fromtimestamp(expire_date) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user: Union[dict[str, Any], None] = query.get_user(db, sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user

def verify_refresh_token(refresh_token: str) -> Union[str, None]:
    try:
        payload = jwt.decode(refresh_token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        expire_date = payload.get("exp")
        sub = payload.get("sub")
        if datetime.fromtimestamp(expire_date) < datetime.now():
            return None
    except (jwt.JWTError, ValidationError):
        return None
    return sub


def generate_random_filename(length=30):
    # Define the characters you want to use in the random filename
    characters = string.ascii_letters + string.digits

    # Generate a random filename of the specified length
    random_filename = "".join(random.choice(characters) for _ in range(length))

    return random_filename






def get_token():
    url = f"{ESKIZ_BASE_URL}/api/auth/login"
    data = {
        "email": ESKIZ_LOGIN,
        "password": ESKIZ_PASSWORD
    }
    response = requests.post(url, data=data)
    return response.json()['data']['token']





def send_sms(phone,message):
    token = get_token()
    url = f"{ESKIZ_BASE_URL}/api/message/sms/send"

    data = {
        "mobile_phone": phone,
        "message": message,
        'from':4546
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, data=data, headers=headers)
    return response.json()







def send_email(to_email,body):
    smtp_server = 'smtp.gmail.com'
    message = f'Subject: Authentication\n\n{body}'
    with smtplib.SMTP(smtp_server, 587) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.sendmail(FROM_EMAIL, to_email, message)


def authiiko():
    data = requests.get(
        f"{BASE_URL}/resto/api/auth?login={LOGIN_IIKO}&pass={PASSWORD_IIKO}"
    )

    key = data.text
    return key



def list_departments(key):
    departments = requests.get(
        f"{BASE_URL}/resto/api/corporation/departments?key={key}"
    )

    root = ET.fromstring(departments.content)
    corporate_item_dtos = root.findall("corporateItemDto")

    names = [
        [item.find("name").text, item.find("id").text] for item in corporate_item_dtos
    ]
    return names



def getgroups(key):
    groups = requests.get(
        f"{BASE_URL}/resto/api/v2/entities/products/group/list?key={key}"
    ).json()
    return groups



def getproducts(key):
    products = requests.get(
        f"{BASE_URL}/resto/api/v2/entities/products/list?key={key}"
    ).json()

    return products




    


def list_departments(key):
    departments = requests.get(
        f"{BASE_URL}/resto/api/corporation/departments?key={key}"
    )

    root = ET.fromstring(departments.content)
    corporate_item_dtos = root.findall("corporateItemDto")

    names = [
        [item.find("name").text, item.find("id").text] for item in corporate_item_dtos
    ]
    return names


def generate_excell(data,db):
    inseting_data = {"Наименование": [], "Группа": [], "Ед. изм.": [], "Цена, шт": [],'Количество':[], 'Сумма':[]}
    for i in data:
        tool_name = str(i.tool.name)
        group_name = str(tools_query_iarch(db=db,parent_id=i.tool.parentid,name=None)[0].name)

        tool_price = i.tool.price
        tool_amount = i.amount
        tool_mainunit = i.tool.mainunit
        tool_totalprice = i.amount*i.tool.price
        inseting_data["Наименование"].append(tool_name)
        inseting_data["Группа"].append(group_name)
        inseting_data["Ед. изм."].append(tool_mainunit)
        inseting_data["Цена, шт"].append(tool_price)
        inseting_data["Количество"].append(tool_amount)

        if i.amount is None:
            i.amount = 0
        inseting_data["Сумма"].append(tool_totalprice)
    df = pd.DataFrame(inseting_data)

    df.to_excel("files/output.xlsx", index=False)
    return "files/output.xlsx"