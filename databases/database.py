# Import necessary attributes from SQLAlchemy
from sqlalchemy import String
from sqlalchemy import MetaData

# Import necessary modules for creating a connection to the database
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


DATABASE_URL = "sqlite:///emp.db"

# CREATING A ENGINE
engine = create_engine(DATABASE_URL, echo=True)


# BASE USED FOR MODELS
Base = declarative_base()


# FOR DATABASE CONNECTIVITY
SessionLocal = sessionmaker(bind=engine)


def get_db():
    
    try:
        db = SessionLocal()
        yield db
    except:
        db.close()
    
