from passlib.context import CryptContext
passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPassword(password: str):
    return passwordContext.hash(password)

def verify(plain, hashed):
    return passwordContext.verify(plain, hashed)

# password hash