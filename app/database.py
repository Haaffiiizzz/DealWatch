from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



DATABASE_URL = f'postgresql+psycopg2://postgres:bucketWater1@localhost:5432/{"DealWatch"}'

# remember to use local postgres
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
