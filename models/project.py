from sqlalchemy import (
    Column,
    text,
    Integer,
    String,
    Text,
    ForeignKey,
    Boolean,
    Date

    
)


from sqlalchemy.orm import (relationship)

from databases.database import *

class Project(Base):
    
    __tablename__ = 'project'
    
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String)
    description = Column(String)
    status = Column(Boolean,  default = True)
    
    start_date = Column(Date, server_default = text("CURRENT_TIMESTAMP"))       
    end_date = Column(Date, server_default = text("CURRENT_TIMESTAMP"))
    
    # Relationship for Employee
       
    emp_id = Column(Integer ,ForeignKey("employee.id") )
    employee = relationship("Employee",back_populates="project")
    
    # Relationship for Stack
    
    stack =   relationship("Stack",back_populates="project")


