from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)

#relationship
from sqlalchemy.orm import (relationship)
# database
from databases.database import *

# project
from .project import Project



class Employee(Base):
    __tablename__ = 'employee'
    
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String)
    status = Column(Boolean)
    
    project = relationship("Project",back_populates="employee")