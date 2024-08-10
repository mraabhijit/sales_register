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
# from utils.models import Users, UserAddress, Sales
from utils.enums import States
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from utils.database import SessionLocal, engine
from .auth import get_current_user
# from datetime import datetime, timedelta
# from jose import jwt, JWTError

from utils.utils import get_db

# load environment variables
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')



router = APIRouter(
    prefix="/address",
    tags=["address"],
    responses={401: {"user": "Not authorized"}}
)



@router.post('/address',) #response_class=HTMLResponse)
async def add_user_information(request:Request,
                        address: str,
                        pincode: str,
                        city: str,
                        state: States,
                        alternate_phone: str,
                        db: Session = Depends(get_db)):
    try:
        user = await get_current_user(request=request)

        validation = db.query(models.UserAddress) \
                        .filter(models.UserAddress.user_id == user.get('user_id')) \
                        .first()
        

        if validation is not None:
            msg = "User Information Exists"
            return msg

        address_model = models.UserAddress()
        address_model.address = address
        address_model.pincode = pincode
        address_model.city = city
        address_model.state = state
        address_model.alternate_phone = alternate_phone
        address_model.user_id = user.get('user_id')

        db.add(address_model)
        db.commit()

        msg = "User Information Added"

        return msg
    
    except Exception as e:
        print(f"Error occurred: {e}")