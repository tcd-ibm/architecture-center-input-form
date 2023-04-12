from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime

from db import get_session
from utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, AuthenticationError, create_token, verify_password
from utils.sql import get_one
from models import Token, User

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=Token, summary="Get access token")
async def login(form: OAuth2PasswordRequestForm = Depends(),
                session: AsyncSession = Depends(get_session)):
    
    user = await get_one(session,
        select(User).where(User.email == form.username)
    )
    if not user or not verify_password(form.password, user.hashed_password):
        raise AuthenticationError("Incorrect username or password")

    token = create_token(
        data = {
            "sub": str(user.id),
            "password_version": user.password_version,
            "role": user.role
        },
        expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    response = {
        "id": user.id,
        "access_token": token,
        "token_type": "bearer",
        "email": user.email,
        "role": user.role,
        "expires_at": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return response