from fastapi import APIRouter, Depends
from ..schemas import CreateUser
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import hashPassword
from ..models import User

router = APIRouter(tags= ["User"])

@router.post("/createuser")
def Create_User(user: CreateUser, db: Session = Depends(get_db)):
    # hash the password then add the edited input (user) to the database
    hashedPassword = hashPassword(user.password)
    user.password = hashedPassword
    newUser = User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser
