from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session



# database
from databases.database import *

# models
from models import *

#schema
from schemas import *
# security
from security import *






emp_router = APIRouter(
    prefix='/api',
    tags=["Employee"],
    route_class=VerifyRoute
)

@emp_router.get("/employee")
def employee_show(db: Session = Depends(get_db)):
    
    # SHOWING ALL EMPLOYEE RECORDS  
    
    
    try:
        emp_data= db.query(m_employee.Employee).all()
        print("test 1 : passed")
        
        
        emp_data = [s_employee.EmployeeShow.from_orm(emp) for emp in emp_data]
        print("test 2 : passed")
        print('employee data is : ',emp_data)
        
        return {
            'status' : 'success',
            'data' : emp_data
        }
    except Exception as e:
        print("error is : ",e)
        
        return {
            'status' : 'failed',
            'msg' : f"{e}"
        }

# schemas.EmployeeShow.parse_obj()

@emp_router.post("/employee")
def create_employee(request : s_employee.Employee, db: Session = Depends(get_db)):
    # ADDING EMPLOYEE
    
    try:
        
        employee = m_employee.Employee(**request.dict())
        
        db.add(employee)
        db.commit()
        
        return {
            'status' : 'Employee Added',
            'data'   : employee
        }
    except Exception as e:
        
        return {
            'status' : 'failed',
            'msg' : 'Unable to Add',
            'error': f'{e}'
        }
