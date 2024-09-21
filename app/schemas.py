from pydantic import BaseModel, EmailStr
from datetime import datetime


class CreateUser(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phoneNumber: str
    password: str
    amazon: bool = False
    bestbuy: bool = False

class UserResponse(BaseModel):
    email: EmailStr
    firstName: str
    lastName: str
    phoneNumber: str
    amazon: bool
    bestbuy: bool
    createdAt: datetime
    


    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    phoneNumber: str = None
    password: str

