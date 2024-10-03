from fastapi import APIRouter, Depends, Body, HTTPException
from ..schemas import CreateUser, UserResponse
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import hashPassword
from ..models import User


router = APIRouter(tags= ["User"])

@router.post("/createuser")
def Create_User(user: CreateUser = Body(), db: Session = Depends(get_db)):
    # hash the password then add the edited input (user) to the database 
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashedPassword = hashPassword(user.password)
    user.password = hashedPassword
    
    newUser = User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return UserResponse.from_orm(newUser)
