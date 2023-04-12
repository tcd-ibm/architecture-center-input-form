from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError
from uuid import UUID

from api import API_PREFIX
from db import get_session
from utils.sql import get_one
from models import User

# TODO move to env
SECRET_KEY = "d8e632e42229356dbbcd5fdc366a05e9bfaca0193ba016e4fd6cf03307d90241"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl=API_PREFIX + "/user/token", auto_error=False)


def AuthenticationError(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail=detail,
                         headers={"WWW-Authenticate": "Bearer"})


def is_admin(user: User) -> bool:
    return True if user.role else False


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_token(data: dict, expires: timedelta = timedelta(minutes=15)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise AuthenticationError("Could not validate credentials")


async def get_current_user(token: str = Depends(oauth2_bearer),
                           session: AsyncSession = Depends(get_session)) -> User | None:
    
    payload = decode_token(token=token)

    # TODO is it not verified automatically?
    expires = payload.get("exp")
    if expires < int(datetime.utcnow().timestamp()):
        raise AuthenticationError("Token expired")

    user_id = payload.get("sub")
    user = await get_one(session,
        select(User).where(User.id == UUID(user_id))
    )

    return user


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
