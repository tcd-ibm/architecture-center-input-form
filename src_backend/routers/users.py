import asyncio
from typing import List, Union
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func

from api import _create_token, ACCESS_TOKEN_EXPIRE_MINUTES, DEFAULT_PAGE, DEFAULT_PAGE_SIZE, \
    get_password_hash, get_user_projects_count_by_id, is_admin, SALT, get_current_user, MAX_PAGE_SIZE
from db import get_session
from utils.auth import require_admin, require_authenticated
from utils.data import is_empty, is_valid_uuid, patch_object, set_count_headers
from utils.sql import get_one, get_some
from models import Token, User, UserInfo, UserResponse, UserSignup, UserUpdate, \
    ProjectInfoAdditional, ProjectInfoAdditionalAdmin, Project


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
    
    ensure_admin_or_self(user, id)

    instance = await get_user_by_id(session, id)

    return instance


@router.post("", response_model=Token)
async def create_user(user: UserSignup,
                      session: AsyncSession = Depends(get_session)):

    await ensure_email_not_used(session, user.email)

    now = datetime.utcnow()

    new_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password + SALT),
        created_at=now,
        updated_at=now,
        password_version=0,
        id=str(uuid4())
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # TODO refactor auth code
    token = _create_token(
        data={
            "sub": user.username,
            "password_version": 0,
            "role": 0
        },
        expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    response = {
        "access_token": token,
        "token_type": "bearer",
        "email": user.email,
        "role": 0,
        "expires_at": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    return response

@router.patch("/{id}", response_model=UserResponse)
async def update_user(user_patch: UserUpdate,
                      id: str,
                      session: AsyncSession = Depends(get_session),
                      current_user: User = Depends(require_authenticated)):
    
    ensure_admin_or_self(current_user, id)

    if is_empty(user_patch):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Patch body cannot be empty.")

    if hasattr(user_patch, 'role'):
        await require_admin(current_user)

    instance = await get_user_by_id(session, id)

    patch_object(instance, user_patch)

    instance.updated_at = datetime.utcnow()

    session.add(instance)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete('/{id}')
async def delete_user(id: str,
                      user: User = Depends(require_authenticated),
                      session: AsyncSession = Depends(get_session)):
    
    ensure_admin_or_self(user, id)

    instance = await get_user_by_id(session, id)

    await session.delete(instance)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{id}/projects", response_model=Union[list[ProjectInfoAdditionalAdmin], list[ProjectInfoAdditional]], tags=['projects'])
async def get_projects_by_user_id(response: Response,
                                  id: str,
                                  per_page: int = DEFAULT_PAGE_SIZE,
                                  page: int = DEFAULT_PAGE,
                                  session: AsyncSession = Depends(get_session),
                                  current_user: User = Depends(require_authenticated)):

    if not is_valid_uuid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found.')
    
    ensure_admin_or_self(current_user, id)

    await get_user_by_id(session, id) # ensures that the requested user exists
    
    count = await get_one(session, 
        select(func.count(Project.id))
        .where(Project.user_id == id)     
    )
    set_count_headers(response, count, per_page)

    results = await get_some(session, page, per_page,
        select(Project)
        .options(selectinload(Project.user),
                 selectinload(Project.tags))
        .where(Project.user_id == id)         
    )

    data = [ vars(instance) for instance in results ]

    if is_admin(current_user):
        return [ ProjectInfoAdditionalAdmin(**item) for item in data ]

    return [ ProjectInfoAdditional(**item) for item in data ]


def ensure_admin_or_self(user: User, userId: str) -> None:
    if not is_admin(user) and str(user.id) != userId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Non-admin user can only access self.")
    
async def ensure_email_not_used(session: AsyncSession, email: str) -> None:
    instance = await get_one(session,
        select(User).where(User.email == email)       
    )
    if instance:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Email already registered.")

async def get_user_by_id(session: AsyncSession, id: str) -> User:
    if not is_valid_uuid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found.')

    instance = await get_one(session,
        select(User)
        .where(User.id == UUID(id))
    )
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found.")
    return instance