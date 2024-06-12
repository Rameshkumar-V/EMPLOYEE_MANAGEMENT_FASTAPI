from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from pydantic import *
import os
# database
from databases.database import *
#model
from models import *
#schema
from schemas import *

#security
from security import VerifyRoute

splitadd = APIRouter(
    route_class=VerifyRoute)





@splitadd.post("/api/allinput")
def create_employee_t(request : s_employee.EmployeeAdd, db: Session = Depends(get_db)):
    """
    TASK : Getting all input from one area and split up and deliver the data to their native.
    """
    
    try:

        emp = s_employee.Employee(**request.dict())
        emp = m_employee.Employee(**emp.dict())
        
        
        project = s_project.Project(**request.dict().get('project'))
        project = m_project.Project(**project.dict())
        
        stack = s_project.Stack(**request.dict().get('project').get('stack'))
        stack= m_project.Stack(**stack.dict())
        
        db.add(emp)
        db.add(project)
        db.add(stack)
        db.flush()
        
        
        project.emp_id = emp.id
        stack.project_id = project.id
        


        
        
        return {
            'status' : 'Employee Added',
            
        }
    except Exception as e:
        db.rollback()
        
        return {
            'status' : 'failed',
            'msg' : f"{e}"
        }
    finally:
        db.commit()
        