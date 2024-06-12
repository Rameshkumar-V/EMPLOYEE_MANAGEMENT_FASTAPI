from fastapi import APIRouter

from pydantic import BaseModel

class login(BaseModel):
    username : str
    password : str


db : list = [
    {
        'username' : 'ramesh',
        'password' : 'password'
    }
]


login_router = APIRouter(tags=["login"])


@login_router.post("/login")
def login_route(request : login):
    
    for user in db:
        if user['username'] == request.username and user['password']== request.password:
            
            return {
                'status' : 'user found'
            }
    else:
      
        return {
            'status' : 'user not found'
        }
    
@login_router.post("/add")
def add_user(request : login):
    
    data = request.dict()
    db.append(data)
    return {
        'status' : 'success'
    }
