from pydantic import BaseModel
from typing import Optional,List

from datetime import datetime

# PYDANTIC VALIDATION.
import pydantic as validation

# stack
from .stack_s import Stackshow,StackAdd


# Project
class Project(BaseModel):
    name : str
    emp_id : Optional[int] = None
    status : Optional[bool] = None
    description : Optional[str] = None
    start_date : Optional[datetime] = None
    end_date : Optional[datetime] = None
    
    class Config:
        from_attributes=True
       
# Deleting Project
class DeleteProject(Project):
    id : int


   
# project showing
class ProjectShow(BaseModel):
    name : str
    status : bool

    description : str
    start_date : datetime
    end_date : datetime
    stack : List[Stackshow] = []
    
    class Config():
        from_attributes = True

# Project Adding
class ProjectAdd(BaseModel):
    
    name : str
    status : bool
    description : str
    start_date : datetime
    end_date : datetime
    stack : StackAdd
    class Config:
        from_attributes=True



