from typing import Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Select


MAX_PAGE_SIZE = 50

async def get_one(session: AsyncSession, statement: Select) -> Any:
    r = await session.execute(statement)
    return r.scalar_one_or_none()

async def get_all(session: AsyncSession, statement: Select) -> List[Any]:
    r = await session.execute(statement)
    return r.scalars().all()

async def get_some(session: AsyncSession, 
                   page: int, per_page: int, statement: Select) -> List[Any]:
    r = await session.execute(
        statement
        .offset(max((page - 1) * per_page, 0))
        .limit(max(min(per_page, MAX_PAGE_SIZE), 0))
    )
    return r.scalars().all()