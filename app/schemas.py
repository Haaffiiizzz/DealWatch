from pydantic import BaseModel, EmailStr
from datetime import datetime


class CreateUser(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    id: int
    createdAt: datetime


    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

