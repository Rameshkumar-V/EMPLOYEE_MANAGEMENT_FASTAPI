from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# database
from databases.database import *
#model
from models import *
#schema
from schemas import *
#security
from security import VerifyRoute
stack_router = APIRouter(
    prefix="/api",
    tags=["Stack"],
    route_class=VerifyRoute
)



@stack_router.get("/api/stack")
def stack_show(db : Session = Depends(get_db)):
    
    # Getting all stack
    
    stack = db.query(m_stack.Stack).all()
    
    if stack:
        return {
            'status' : 'success',
            'msg': 'Successfully Stack Added',
            'data' : stack
        }
    else:
        return {
            'status' : 'failed',
            'msg' : 'Empty Stack'
        }


# CUSTOM RESPONSE
@stack_router.post("/api/stack",response_model=s_stack.Stackcustom)
def creating_stack(req : s_stack.Stack,db : Session = Depends(get_db)):
    
    # Addting Stack with custom response
    
    try:
    
        stack = m_stack.Stack(**req.dict())
        
        db.add(stack)
        db.commit()
        
        return stack
    except:
        return {
            'error' : 'error '
        }
    