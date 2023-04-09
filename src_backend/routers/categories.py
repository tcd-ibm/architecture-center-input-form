from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from utils.auth import require_admin
from utils.data import patch_object
from utils.sql import get_one
from models import Category, CategoryCreate


router = APIRouter(prefix='/categories', tags=['categories'], dependencies=[Depends(require_admin)])

@router.post('', response_model=Category)
async def create_category(new_category: CategoryCreate,
                          session: AsyncSession = Depends(get_session)):
    
    await ensure_category_name_not_used(session, new_category.categoryName)

    instance = Category(categoryName=new_category.categoryName)

    session.add(instance)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.patch('/{id}', response_model=Category)
async def patch_category(id: int,
                          category_patch: CategoryCreate,
                          session: AsyncSession = Depends(get_session)):

    instance = await get_category_by_id(session, id)

    patch_object(instance, category_patch)

    session.add(instance)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete('/{id}')
async def delete_category(id: int,
                          session: AsyncSession = Depends(get_session)):

    instance = await get_category_by_id(session, id)

    await session.delete(instance)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def ensure_category_name_not_used(session: AsyncSession, categoryName: str) -> None:
    instance = await get_one(session,
        select(Category)
        .where(Category.categoryName == categoryName)                   
    )
    if instance:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail='Category already exists.')

async def get_category_by_id(session: AsyncSession, id: int) -> Category:
    instance = await get_one(session,
        select(Category)
        .where(Category.categoryId == id)                         
    )
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Category not found.')
    return instance