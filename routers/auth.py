import sys
sys.path.append("..")


from starlette.responses import RedirectResponse

from fastapi import (Depends, HTTPException, status, 
                     APIRouter, Request, Response, Form)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from pydantic import BaseModel
from typing import Optional
from utils.models import Users, UserAddress, Sales
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from utils.database import SessionLocal, engine
from datetime import datetime, timedelta
from jose import jwt, JWTError

from utils.utils import get_db