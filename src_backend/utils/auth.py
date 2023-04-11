from fastapi import Depends, HTTPException, status

from api import get_current_user, is_admin
from models import User


async def require_authenticated(user: User | None = Depends(get_current_user)) -> User:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authenticated")
    return user

async def require_admin(user: User = Depends(require_authenticated)) -> User:
    if not is_admin(user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Admin privileges required.")
    return user
