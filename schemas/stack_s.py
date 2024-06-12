from pydantic import BaseModel
from typing import Optional,List

from datetime import datetime

# PYDANTIC VALIDATION.
import pydantic as validation

class Stack(BaseModel):
    project_id : int
    name : str
class Stackshow(BaseModel):
    project_id : int
    name : str
    class Config:
        from_attributes=True


# stack add model
class StackAdd(BaseModel):
    project_id : int 
    name : str
    class Config:
        from_attributes=True






# custom stack show for response model

class Stackcustom(BaseModel):
    
    name : str