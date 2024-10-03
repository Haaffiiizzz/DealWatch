from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schemas import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def createToken(data: dict):
    toEncode= data.copy()

    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp": expire})

    encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm = ALGORITHM)
    return encodedJWT
    # here the token is created using the payload(toEncode), secret key and algorithm

def verifyToken(token: str, credentialsException):
    # this function is only called by getcurrent user which is what we call in the other files
    # we dont call this directly in the other files
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if not id:
            raise credentialsException
        
        token_data = TokenData(id=str(id))
    
    except JWTError:
        raise credentialsException
    
    return token_data

def getCurrentUser(token: str = Depends(oauth2_scheme)):
    credentialsException = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials"
      , headers = {"WWW-Authenticate": "Bearer"})
   
    return verifyToken(token, credentialsException)