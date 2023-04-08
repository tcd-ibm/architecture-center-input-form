from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from utils.data import patch_object
from utils.auth import require_admin
from models import Category, CategoryCreate

router = APIRouter(prefix='/categories', tags=['categories'], dependencies=[Depends(require_admin)])

@router.post('', response_model=Category)
async def create_category(new_category: CategoryCreate,
                          session: AsyncSession = Depends(get_session)):
    
    r = await session.execute(
        select(Category).where(
            Category.categoryName == new_category.categoryName))
    if r.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail='Category already exists.')

    new_category_instance = Category(categoryName=new_category.categoryName)

    session.add(new_category_instance)
    await session.commit()
    await session.refresh(new_category_instance)
    return new_category_instance


@router.patch('/{id}', response_model=Category)
async def patch_category(id: int,
                          category_patch: CategoryCreate,
                          session: AsyncSession = Depends(get_session)):

    r = await session.execute(
        select(Category).where(Category.categoryId == id))
    original_instance = r.scalar_one_or_none()

    if not original_instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Category not found.')

    patch_object(original_instance, category_patch)

    session.add(original_instance)
    await session.commit()
    await session.refresh(original_instance)
    return original_instance


@router.delete('/{id}')
async def delete_category(id: int,
                          session: AsyncSession = Depends(get_session)):

    r = await session.execute(
        select(Category).where(Category.categoryId == id))
    original_instance = r.scalar_one_or_none()

    if not original_instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Category not found.')

    await session.delete(original_instance)
    await session.commit()
    await session.flush()
    return Response(status_code=status.HTTP_204_NO_CONTENT)