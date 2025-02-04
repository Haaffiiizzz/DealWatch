from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

#schemas for data input and return
# class CreateUser(BaseModel):
#     firstName: str
#     lastName: str
#     email: EmailStr
#     phoneNumber: str
#     password: str
#     amazon: bool = False
#     bestbuy: bool = False

# class UserResponse(BaseModel):
#     email: EmailStr
#     firstName: str
#     lastName: str
#     phoneNumber: str
#     amazon: bool
#     bestbuy: bool
#     createdAt: datetime
    


#     class Config:
#         orm_mode = True
#         from_attributes = True

# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     id: Optional[str] = None

class LinkData(BaseModel):
    url: str