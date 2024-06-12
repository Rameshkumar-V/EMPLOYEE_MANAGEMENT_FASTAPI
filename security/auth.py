from datetime import timedelta, datetime
from typing import Annotated,Dict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
# orm
from sqlalchemy.orm import Session
from starlette import status
# database
from databases.database import *
#model
from models import *
# hashing
from passlib.context import CryptContext
#security always want form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# jwt
from jose import jwt, JWTError
# schema
from schemas.security import *

# customclass
from .utils import get_current_user
from .customroute import VerifyRoute
# rest of the code remains the same
#config
from .config import *

#model
from models.security import *


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    route_class=VerifyRoute
)

@router.get("/hi")
async def index():
    return {"message": "Welcome to the FastAPI application"}

# Bearer
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

# HASHING AND DE-HASHING
"""
NOTE :
 * bcryptcontext provide two functions:
 
        1) hash(value)
        
        2) verify(original password, hashed pashword)
"""
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
"""
NOTE :
 * db_dependency is first Depends the get_db they satisfied then check its type match
 to session and they checked by annotated .
 
 * using annotated for more readability.
 """
db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/")
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    """
    -> CREATING USER
    
    -> IF VALID WITH SHCEMA THEN HASHING PASSWORD
    -> ADDING USER TO DB
    """
    create_user_model = User(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password)  # password hashed
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    
    return {
        'status': 'Added user Successfully',
        'data': create_user_model
    }

def authenticate_user(username: str, password: str, db: Session):
    print("2) ATHENTICATION USER SECTION PASSED")
    #AUTHENTICATING USER
    """
    -> Get user with help of username got first record from db.
    
    -> if user found then verify their original and hashed password where match.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):  # Verify hashed password
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    # CREATING ACCESS TOKEN
    """
    ->  Getting parameters
    
    -> and update the dict
    
    -> encode that data with SECRET_KEY and ALGORITHM
    
    -> Response that data
    """
    encode = {"sub": username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    # LOGIN with TOKEN to access protected routes.
    """
    -> STEP 1 :  authenticating user
    
    -> STEP 2 : when user found then creating access token else respond with unauthorized
    """
    
    
    user = authenticate_user(form_data.username, form_data.password, db)
    if user:
        token = create_access_token(user.username, user.id, timedelta(minutes=20))
        return {
            
            'status': "success",
            'data' : [
                {
                    'token_type': 'bearer',
                    "token" : token
                }
                
            ],
            'message' : 'Getted Access Token'
            
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'status' : 'failed',
                'message' : "Unauthorized"
            }
        )

# # Get current user

# async def get_current_user(token: str = Depends(oauth2_bearer)) -> Dict[str, str]:
#     try:
#         print("paload section",token)
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         print("payload is : ",payload)
#         username: str = payload.get('sub')
#         user_id: int = payload.get('id')
#         print("u , id",username,user_id)

#         if username is None or user_id is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail='Could not validate user.'
#             )
#         return {
#             'username': username,
#             'id': user_id
#         }
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail='Could not validate user.'
#         )