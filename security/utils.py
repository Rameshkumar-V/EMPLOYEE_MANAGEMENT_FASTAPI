from fastapi import HTTPException, status
from jose import jwt, JWTError
from datetime import timedelta, datetime
from typing import Dict

from .config import *

async def get_current_user(token: str) -> Dict[str, str]:
    """
    Get the current user from the JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate user.'
            )
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user.'
        )
