from typing import Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Select


async def get_one(session: AsyncSession, statement: Select) -> Any:
    r = await session.execute(statement)
    return r.scalar_one_or_none()

async def get_all(session: AsyncSession, statement: Select) -> List[Any]:
    r = await session.execute(statement)
    return r.scalars().all()