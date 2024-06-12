from fastapi import Request, Response, Depends, HTTPException
from fastapi.routing import APIRoute
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Callable
from urllib.parse import parse_qs
from starlette.responses import JSONResponse

# Assuming these constants are defined in your config
SECRET_KEY = "your_secret_key"  # replace with your actual secret key
ALGORITHM = "HS256"  # replace with your actual algorithm

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

class VerifyRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def verify_token_middleware(request: Request):
            if request.url.path in ['/auth/login', '/auth/']:
                return await original_route_handler(request)

            auth_header = request.headers.get('Authorization')
            if auth_header is None or not auth_header.startswith("Bearer "):
                return JSONResponse(status_code=401, content={'detail': 'Unauthorized'})

            # token = auth_header[len("Bearer "):]
            token =await OAuth2PasswordBearer(tokenUrl='login')(request=request)
            print('token is : ',token)
            
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username: str = payload.get('sub')
                user_id: int = payload.get('id')
                
                if username is None or user_id is None:
                    raise JWTError()
            except JWTError:
                return JSONResponse(status_code=401, content={'detail': 'Unauthorized'})

            request.state.username = username
            request.state.user_id = user_id

            return await original_route_handler(request)

        return verify_token_middleware
