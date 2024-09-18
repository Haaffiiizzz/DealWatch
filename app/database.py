from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



DATABASE_URL = "postgresql://u31ds03jcv80cp:p0cbfd4154e29cbb52ac3eaeda5783e7a25c602e5e6a7f6a5a674116cf0adebb8@cb5ajfjosdpmil.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d44ms2fjvucl0l"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

Base = declarative_base()

def get_db():
    db = SessionLocal()
    
    try:
        yield db
        
    finally:
        db.close()
        
#  need a commit