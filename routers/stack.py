from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
# database
from databases.database import get_db
# model
from models import m_stack
# schema
from schemas import s_stack
# security
from security import VerifyRoute

stack_router = APIRouter(
    prefix="/api",
    tags=["Stack"],
    route_class=VerifyRoute
)

@stack_router.get("/stack")
def stack_show(db: Session = Depends(get_db)):
    # Getting all stack
    stack = db.query(m_stack.Stack).all()
    
    if stack:
        return {
            'status': 'success',
            'msg': 'Successfully retrieved stack',
            'data': stack
        }
    else:
        return {
            'status': 'failed',
            'msg': 'Empty stack'
        }

# CUSTOM RESPONSE
@stack_router.post("/stack")
def creating_stack(req: s_stack.Stack, db: Session = Depends(get_db)):
    # Adding Stack with custom response
    try:
        stack = m_stack.Stack(**req.dict())
        db.add(stack)
        db.commit()
        db.refresh(stack)  # Refresh the instance to get the updated data
        
        return {
            'status': 'success',
            'msg': 'Successfully added',
            'data': stack.__dict__  # Including the stack data
        }
    except SQLAlchemyError as e:
        db.rollback()  # Rollback the transaction in case of an error
        raise HTTPException(status_code=400, detail=f"Unable to add stack. Error: {str(e)}")
