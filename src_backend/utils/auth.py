from fastapi import Depends, HTTPException, status

from api import get_current_user, is_admin
from models import User

async def require_admin(current_user: User = Depends(get_current_user)) -> None:
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")
    if not is_admin(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Admin privileges required.")