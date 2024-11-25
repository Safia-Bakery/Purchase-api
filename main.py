from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Form,Header,Request,status
from typing import Optional

from fastapi_pagination import paginate,Page,add_pagination
from fastapi.staticfiles import StaticFiles
from users.models.users import Base
from database import engine
from users.routes.user_routes import user_router
from orders.routes.order_route import order_router
from services import get_current_user_for_docs
#from routes import user_route,product_route

app = FastAPI(swagger_ui_parameters = {"docExpansion":"none"},docs_url=None, redoc_url=None, openapi_url=None)

app.title = "Safia FastApi App"
app.version = "0.0.1"

app.include_router(order_router , tags=["Order"])
app.include_router(user_router, tags=["User"])
#app.include_router(user_router)
Base.metadata.create_all(bind=engine)
app.mount("/files", StaticFiles(directory="files"), name="files")
#app.include_router(user_route.user_router, tags=["User"])
#app.include_router(product_route.product_router, tags=["Product"])
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui(current_user: str = Depends(get_current_user_for_docs)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom Swagger UI")


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(current_user: str = Depends(get_current_user_for_docs)):
    return get_openapi(title="Custom OpenAPI", version="1.0.0", routes=app.routes)


@app.get("/", tags=["Home"])
def message():
    """message get method"""
    return HTMLResponse("<h1>Fuck of man!</h1>")


add_pagination(app)

