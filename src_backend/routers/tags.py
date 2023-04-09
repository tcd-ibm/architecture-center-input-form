from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db import get_session
from utils.auth import require_admin
from utils.data import is_empty, patch_object
from models import Category, CategoryWithTags, Tag, TagCreate, TagUpdate

router = APIRouter(prefix='/tags', tags=['tags'])

@router.get('', response_model=List[CategoryWithTags])
async def fetch_tags(session: AsyncSession = Depends(get_session)):
    r = await session.execute(
        select(Category)
        .options(selectinload(Category.tags))
        .order_by(Category.categoryId)
    )
    
    return r.scalars().all()

@router.get("/{id}", response_model=Tag)
async def fetch_tag(id: int,
                    session: AsyncSession = Depends(get_session)):
    
    r = await session.execute(
        select(Tag).where(Tag.tagId == id)
    )
    instance = r.scalar_one_or_none()

    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tag not found.")
    return instance

@router.post('', response_model=Tag, dependencies=[Depends(require_admin)])
async def create_tag(new_tag: TagCreate,
                     session: AsyncSession = Depends(get_session)):

    if new_tag.tagNameShort is None:
        new_tag.tagNameShort = new_tag.tagName

    if not new_tag.tagName or not new_tag.tagNameShort:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Tag name and short name are required.")

    r = await session.execute(
        select(Tag)
        .where((Tag.tagName == new_tag.tagName) | 
               (Tag.tagNameShort == new_tag.tagNameShort))
    )
    if r.scalar_one_or_none():
       raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                           detail="Tag with this name exists.") 

    r = await session.execute(
        select(Category)
        .where(Category.categoryId == new_tag.categoryId)
    )
    if not r.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Category not found.")

    instance = Tag(
        tagName=new_tag.tagName,
        tagNameShort=new_tag.tagNameShort,
        categoryId=new_tag.categoryId
    )
    
    session.add(instance)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.patch('/{id}', response_model=Tag, dependencies=[Depends(require_admin)])
async def update_tag(id: int,
                     updated_tag: TagUpdate,
                     session: AsyncSession = Depends(get_session)):

    r = await session.execute(select(Tag).where(Tag.tagId == id))
    original_instance = r.scalar_one_or_none()

    if not original_instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tag not found.")
    
    if is_empty(updated_tag):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Patch body cannot be empty.")

    if hasattr(updated_tag, 'categoryId') and updated_tag.categoryId:
        r = await session.execute(
            select(Category)
            .where(Category.categoryId == updated_tag.categoryId)
        )
        if not r.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Category not found.")
        
    r = await session.execute(
        select(Tag)
        .where((Tag.tagName == updated_tag.tagName) | 
               (Tag.tagNameShort == updated_tag.tagNameShort))
    )
    if r.scalar_one_or_none():
       raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                           detail="Tag with this name exists.")

    patch_object(original_instance, updated_tag)

    session.add(original_instance)
    await session.commit()
    await session.refresh(original_instance)
    return original_instance


@router.delete('/{id}', dependencies=[Depends(require_admin)])
async def delete_tag(id: int,
                     session: AsyncSession = Depends(get_session)):

    r = await session.execute(select(Tag).where(Tag.tagId == id))
    original_instance = r.scalar_one_or_none()

    if not original_instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tag not found.")

    await session.delete(original_instance)
    await session.commit()
    await session.flush()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
