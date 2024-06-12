from pydantic import BaseModel
from typing import Optional,List


# DATE TIME
from datetime import datetime

# PYDANTIC VALIDATION.
import pydantic as validation

# project
from .project_s import ProjectAdd,ProjectShow



# Adding Employee    
class EmployeeAdd(BaseModel):
    
    
    name : Optional[str]
    age : Optional[int]
    email : Optional[str]
    status : Optional[bool]
    project : ProjectAdd
    

    
    class Config():
        from_attributes=True


# Employee Show Model
class EmployeeShow(BaseModel):
    
    id : Optional[int]
    name : Optional[str]
    age : Optional[int]
    email : Optional[str]
    status : Optional[bool]
    project : List[ProjectShow] = []
    

    
    class Config():
        from_attributes=True


class Employee(BaseModel):
    
    name : validation.constr(min_length=1,max_length=30)
    age : validation.conint(ge=18 , le=58)
    email : validation.EmailStr
    status : validation.StrictBool
    
    class Config():
        from_attrubutes = True