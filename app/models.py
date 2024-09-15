from database import Base
from sqlalchemy import Column, String, Integer, JSON, TIMESTAMP, text, Boolean

# class Amazon(Base):
#     __tablename__ = "Amazon"
#     UserID = Column(Integer, primary_key=True, nullable=False)
    

# class BestBuy(Base):
#     __tablename__ = "BestBuy"
#     country = Column(String, primary_key=True, unique=True)
#     items = Column(JSON)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    amazon = Column(Boolean, server_default = 'False')
    bestbuy = Column(Boolean, server_default = 'False')
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, 
                       server_default= text('now()'))
    

# here we create the model for the countries and users table to be used with the db query