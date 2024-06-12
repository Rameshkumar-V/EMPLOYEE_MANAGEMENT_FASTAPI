from sqlalchemy import *
from databases.database import Base



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String)
    hashed_password = Column(String)
    




