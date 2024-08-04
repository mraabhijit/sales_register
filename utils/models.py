from sqlalchemy import Column, Integer, Float, Enum, String
from sqlalchemy import ForeignKey, Date, Time, func
# from sqlalchemy.orm import relationship
from utils.database import Base
from utils.enums import States 


class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)


class UserAddress(Base):
    __tablename__ = "address"

    address_id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    pincode = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    state = Column(Enum(States), nullable=False)
    alternate_phone = Column(String)
    user_id = Column(Integer, ForeignKey("users.user_id"))


class Sales(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    cash_amount = Column(Float)
    upi_amount = Column(Float)
    date = Column(Date, default=func.current_date())
    time = Column(Time, default=func.current_time())
    paid_to = Column(String(length=255))
    upi_ref = Column(String(length=255))
    comments = Column(String(length=255))
    user_id = Column(Integer, ForeignKey("users.user_id"))