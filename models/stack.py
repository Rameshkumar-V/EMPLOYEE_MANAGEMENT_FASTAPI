from sqlalchemy import (
    Integer,String,Column ,ForeignKey 
)

from sqlalchemy.orm import (
    relationship
)

from databases.database import *



class Stack(Base):
    __tablename__ = 'stack'
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String)
    project_id = Column(Integer ,ForeignKey("project.id") )
    project = relationship("Project",back_populates="stack")