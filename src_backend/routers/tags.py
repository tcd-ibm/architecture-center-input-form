from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db import get_session
from models import Category, CategoryWithTags, Tag

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