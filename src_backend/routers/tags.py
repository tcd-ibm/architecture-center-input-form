from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db import get_session
from utils.auth import require_admin
from utils.data import is_empty, patch_object
from utils.sql import get_all, get_one
from models import Category, CategoryWithTags, Tag, TagCreate, TagUpdate


router = APIRouter(prefix='/tags', tags=['tags'])

@router.get('', response_model=List[CategoryWithTags])
async def fetch_tags(session: AsyncSession = Depends(get_session)):

    instances = await get_all(session,
        select(Category)
        .options(selectinload(Category.tags))
        .order_by(Category.categoryId)           
    )
    
    return instances

@router.get("/{id}", response_model=Tag)
async def fetch_tag(id: int,
                    session: AsyncSession = Depends(get_session)):
    
    instance = await get_one(session,
        select(Tag)
        .where(Tag.tagId == id)
    )

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

    await ensure_category_exists(session, new_tag.categoryId)

    await ensure_no_duplicate_tags_exist(session, new_tag.tagName, new_tag.tagNameShort)

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
                     tag_patch: TagUpdate,
                     session: AsyncSession = Depends(get_session)):

    if is_empty(tag_patch):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Patch body cannot be empty.")
    
    instance = await get_one(session,
        select(Tag)
        .where(Tag.tagId == id)
    )

    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tag not found.")

    if hasattr(tag_patch, 'categoryId') and tag_patch.categoryId:
        await ensure_category_exists(session, tag_patch.categoryId)
    
    await ensure_no_duplicate_tags_exist(session, tag_patch.tagName, tag_patch.tagNameShort)

    patch_object(instance, tag_patch)

    session.add(instance)
    await session.commit()
    await session.refresh(instance)
    return instance

@router.delete('/{id}', dependencies=[Depends(require_admin)])
async def delete_tag(id: int,
                     session: AsyncSession = Depends(get_session)):

    instance = await get_one(session,
        select(Tag)
        .where(Tag.tagId == id)
    )

    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tag not found.")

    await session.delete(instance)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def ensure_category_exists(session: AsyncSession, categoryId: int) -> None:
    category_instance = await get_one(session,
        select(Category)
        .where(Category.categoryId == categoryId)                  
    )

    if not category_instance:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Category not found.")
    
async def ensure_no_duplicate_tags_exist(session: AsyncSession, 
                                         tagName: str | None, tagNameShort: str | None) -> None:
    instance = await get_one(session,
        select(Tag)
        .where((Tag.tagName == tagName) | 
               (Tag.tagNameShort == tagNameShort))
    )

    if instance:
       raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                           detail="Tag with this name exists.")
