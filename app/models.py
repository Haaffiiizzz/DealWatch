from .database import Base
from sqlalchemy import Column, String, Integer, JSON, TIMESTAMP, text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

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
    
    amazonUser = relationship("Amazon", back_populates="user", cascade="all, delete")
    bestbuyUser = relationship("BestBuy", back_populates="user", cascade="all, delete")   #establishing relationship

class Amazon(Base):
    __tablename__ = "amazon"
    __table_args__ = {'schema': 'dealwatch'}
    
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('dealwatch.users.id'), nullable=False)
    title = Column(String, nullable=False)
    brand = Column(String)
    price = Column(String)
    imageSrc = Column(String)
    
    user = relationship("User", back_populates="amazonUser")   #establishing relationship
    
class BestBuy(Base):
    __tablename__ = "bestbuy"
    __table_args__ = {'schema': 'dealwatch'}
    
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('dealwatch.users.id'), nullable=False)
    title = Column(String, nullable=False)
    brand = Column(String)
    price = Column(String)
    imageSrc = Column(String)
    
    user = relationship("User", back_populates="bestbuyUser")      #establishing relationshipS

