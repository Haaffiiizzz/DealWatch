from .database import Base
from sqlalchemy import Column, String, Integer, JSON, TIMESTAMP, text, Boolean

# class Amazon(Base):
#     __tablename__ = "Amazon"
#     UserID = Column(Integer, primary_key=True, nullable=False)
    


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'dealwatch'}
    id = Column(Integer, primary_key= True, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String)
    phoneNumber = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    amazon = Column(Boolean)
    bestbuy = Column(Boolean)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, 
                       server_default= text('now()'))
    

# here we create the model for the countries and users table to be used with the db query