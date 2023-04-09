import asyncio
from typing import List
from datetime import datetime, timedelta
import re
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from api import _create_token, ACCESS_TOKEN_EXPIRE_MINUTES, DEFAULT_PAGE, DEFAULT_PAGE_SIZE, \
    get_current_user, get_password_hash, get_user_projects_count_by_id, get_user_with_email_db, \
    is_admin, MAX_PAGE_SIZE, SALT
from db import get_session
from utils.auth import require_admin, require_authenticated
from utils.data import set_count_headers
from utils.sql import get_all, get_one, get_some
from models import Token, User, UserInfo, UserSignup, UserUpdate


router = APIRouter(prefix='/users', tags=['users'])


@router.get('', response_model=List[UserInfo], dependencies=[Depends(require_admin)])
async def admin_get_all_users(response: Response,
                              per_page: int = DEFAULT_PAGE_SIZE,
                              page: int = DEFAULT_PAGE,
                              session: AsyncSession = Depends(get_session)):

    count = await get_one(session,
        select(func.count(User.id))
    )

    set_count_headers(response, count, per_page)

    users = await get_some(session, page, per_page,
        select(User)       
    )
    
    # TODO research whether these queries can be optimised
    ids = [ user.id for user in users ]
    tasks = [ get_user_projects_count_by_id(id, session) for id in ids ]
    users_projects_counts = await asyncio.gather(*tasks)

    results = [
        UserInfo(id=user.id,
                 created_at=user.created_at,
                 email=user.email,
                 username=user.username if user.username else None,
                 is_active=user.is_active,
                 role=user.role) 
        for user in users
    ]

    for i in range(len(results)):
        results[i].projects_counts = users_projects_counts[i]

    return results


@router.get("/{id}", response_model=UserInfo)
async def get_user(id: str,
                   user: User = Depends(require_authenticated),
                   session: AsyncSession = Depends(get_session)):
    
    if not id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid user id")
    
    ensure_admin_or_self(user, id)

    instance = await get_one(session,
        select(User)
        .where(User.id == id)
    )

    return instance

# TODO refactor
@router.post("", response_model=Token)
async def create_user(user: UserSignup,
                      session: AsyncSession = Depends(get_session)):
    if not user.email or not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email invalid")

    existed_user = await get_user_with_email_db(user.email, session)
    if existed_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email registered already")

    if not user.password or len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password invalid, should be at least 8 characters")

    new_user = User(email=user.email,
                    hashed_password=get_password_hash(user.password + SALT),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    password_version=0,
                    id=str(uuid4()))

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    token = _create_token(
        data={
            "sub": user.username,
            "password_version": 0,
            "role": 0
        },
        expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    response = {
        "access_token":
        token,
        "token_type":
        "bearer",
        "email":
        user.email,
        "role":
        0,
        "expires_at":
        datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return response

# TODO refactor
@router.patch("/{id}", response_model=User)
async def update_user(user: UserUpdate,
                      id: str,
                      session: AsyncSession = Depends(get_session),
                      current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")

    r = await session.execute(select(User).where(User.id == id))
    user_to_update = r.scalar_one_or_none()

    if not user_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    if not is_admin(current_user) and user_to_update.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="non-admin user can only update self")

    data = user.dict(exclude_unset=True)

    for k, v in data.items():
        if v is not None:
            if k == "password":
                if len(v) < 8:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=
                        "Password invalid, should be at least 8 characters")
                if get_password_hash(v +
                                     SALT) == user_to_update.hashed_password:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Password not changed")
                user_to_update.password_version += 1
                k, v = "hashed_password", get_password_hash(v + SALT)
            elif k == "email":
                result = await session.execute(
                    select(User).where(User.email == v))
                searched_user = result.scalar_one_or_none()
                if searched_user and searched_user.id != current_user.id:  # if the queried user with same email is not user self
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"email {v} registered already")

            setattr(user_to_update, k, v)

    user_to_update.updated_at = datetime.utcnow()

    session.add(user_to_update)
    await session.commit(
    )  # flush is actually not needed here since commit will flush automatically
    await session.refresh(user_to_update)
    user_data = user_to_update.__dict__
    user_data.pop("hashed_password")
    return user_data


@router.delete('/{id}')
async def delete_user(id: str,
                      user: User = Depends(require_authenticated),
                      session: AsyncSession = Depends(get_session)):
    if not id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid user id.")
    
    ensure_admin_or_self(user, id)

    instance = await get_one(session,
        select(User)
        .where(User.id == id)
    )

    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found.")

    await session.delete(instance)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def ensure_admin_or_self(user: User, userId: str) -> None:
    if not is_admin(user) and user.id != userId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Non-admin user can only access self.")