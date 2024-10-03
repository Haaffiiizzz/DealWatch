from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..models import User
from ..utils import verify
from ..oauth2 import createToken

router = APIRouter(tags = ["Authentication"])


@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    accessToken = createToken(data = {"user_id": user.id})
    return {"access_token": accessToken, "token_type": "bearer"}