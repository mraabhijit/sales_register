import sys
sys.path.append("..")
import os
from dotenv import load_dotenv

from starlette.responses import RedirectResponse

from fastapi import (Depends, HTTPException, status, 
                     APIRouter, Request, Response, Form)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from pydantic import BaseModel
from typing import Optional
from utils import models
from utils.models import Users, UserAddress, Sales
from utils.enums import States
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from utils.database import SessionLocal, engine
from datetime import datetime, timedelta
from jose import jwt, JWTError

from utils.utils import get_db

# load environment variables
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')



router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.phone_number: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.phone_number = form.get('phone_number')
        self.password = form.get('password')


def get_password_hash(password: str):
    return bcrypt_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt_context.verify(plain_password, hashed_password)

def authenticate_user(phone_number: str, password: str, db):
    user = db.query(models.Users) \
             .filter(models.Users.phone_number == phone_number) \
             .first()
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(phone_number: str, user_id: int, 
                        expires_delta: Optional[timedelta] = None,
                        SECRET_KEY: str = SECRET_KEY,
                        ALGORITHM: str = ALGORITHM):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    encode = {
        "sub": phone_number,
        "id": user_id,
        "exp": expire
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

### Check from here

async def get_current_user(request: Request, SECRET_KEY: str = SECRET_KEY, ALGORITHM: str = ALGORITHM):
    try:
        token = request.cookies.get('access_token')
        if not token:
            return None
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone_number: str = payload.get("sub")
        user_id: int = payload.get("id")
        if phone_number is None or user_id is None:
            logout(request)
        return {"phone_number": phone_number, "id": user_id}
    except JWTError:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
    )

@router.post("/token")
async def login_for_access_token(response: Response,
                                form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.phone_number, form_data.password, db)
    if not user:
        return False
    token_expires = timedelta(minutes=60)
    token = create_access_token(user.phone_number,
                                user.id,
                                expires_delta=token_expires)
    
    response.set_cookie(key="access_token", 
                        value=token,
                        httponly=True)
    return True

# @router.get('/', response_class=HTMLResponse)
# async def authentication_page(request: Request):
#     return templates.TemplateResponse(
#         "login.html",
#         {'request': request}
#     )


# @router.post('/', response_class=HTMLResponse)
# async def login(request: Request,
#                 db: Session = Depends(get_db)):
#     try: 
#         form = LoginForm(request)
#         await form.create_oauth_form()
#         response = RedirectResponse(
#             url='/todos',
#             status_code=status.HTTP_302_FOUND
#         )

#         validate_user_cookie = await login_for_access_token(response=response, 
#                                                             form_data=form,
#                                                             db=db)
        
#         if not validate_user_cookie:
#             msg = "Incorrect phone_number or Password"
#             return templates.TemplateResponse(
#                 "login.html",
#                 {"request": request,
#                  "msg": msg}
#             )
#         return response
#     except HTTPException:
#         msg = "Unknown error"
#         return templates.TemplateResponse(
#             "login.html",
#             {"request": request,
#              "msg": msg}
#         )


# @router.get('/logout')
# async def logout(request: Request):
#     msg = "Logout Successful"
#     response = templates.TemplateResponse(
#         "login.html", 
#         {"request": request,
#          "msg": msg}
#     )
#     response.delete_cookie(key='access_token')
#     return response


# @router.get('/register', response_class=HTMLResponse)
# async def register(request: Request):
#     return templates.TemplateResponse(
#         "register.html",
#         {'request': request}
#     )


@router.post('/register') 
async def register_user(request:Request,
                        email: str, 
                        business_name: str,
                        phone_number: str,
                        password: str,
                        password2: str,
                        db: Session = Depends(get_db)
                        ):
    try:
        validation1 = db.query(models.Users) \
                        .filter(models.Users.phone_number == phone_number) \
                        .first()
        
        validation2 = db.query(models.Users) \
                        .filter(models.Users.email == email) \
                        .first()

        if password != password2 or validation1 is not None or validation2 is not None:
            msg = "Invalid Registration Request"
            # return templates.TemplateResponse(
            #     "register.html",
            return {"request": request, 
                "msg": msg}
            # )
        
        user_model = models.Users()
        user_model.email = email
        user_model.phone_number = phone_number
        user_model.business_name = business_name
        user_model.hashed_password = get_password_hash(password=password)

        db.add(user_model)
        db.commit()


        msg = "User Successfully Created"
        # return templates.TemplateResponse(
        #     "login.html",
        return {"request": request, 
            "msg": msg}
        # )
    except Exception as e:
        # Log the error for debugging
        print(f"Error occurred: {e}")
        msg = "Internal Server Error"
        return {"request": request, "msg": msg}