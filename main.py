from fastapi import (
    FastAPI
    
)




# ROUTERS
from routers import *
from security import *
from security.auth import router as auth_router

app = FastAPI()


# Creating Tables using Object help of ORM
Base.metadata.create_all(engine)

@app.get("/")
def index():
    # WELCOME PAGE
    
    return {
        "status" : "FastApi now Working "
    }


"""
SECTION : EMPLOYEE
"""
app.include_router(emp_router)



"""
SECTION : PROJECT
"""
app.include_router(project_router)


"""
SECTION : STACK
"""
app.include_router(stack_router)

"""
SECTION : ALL INPUT FROM ONE FORM
"""
app.include_router(splitadd)


"""
SECTION :  security
"""
app.include_router(auth_router)



# from login import login_router

# app.include_router(login_router)




             
