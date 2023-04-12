from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta, datetime

from db import get_session
from utils.auth import require_admin
from utils.sql import get_one
from models import Project, project_tags, Tag, TagCount


router = APIRouter(prefix='/statistics', tags=['statistics'], dependencies=[Depends(require_admin)])


@router.get("/visits")
async def get_total_projects_visit(session: AsyncSession = Depends(get_session)):

    count = (await session.execute(select(func.sum(Project.visit_count))
                                   )).scalar_one_or_none()
    
    count = await get_one(session, 
        select(func.sum(Project.visit_count))
    )

    if not count:
        count = 0

    return { "total": count }


# TODO refactor
@router.get("/projectupdates/count")
async def get_count_projects_updated_over_last_n_days(num_days: int = 7, session: AsyncSession = Depends(get_session)):

    if num_days < 1:
        num_days = 7
    
    # Calculate the start date for the query
    n_days_ago = datetime.utcnow() - timedelta(days=num_days - 1)

    # Define a subquery to group the projects by date and count the number of projects
    subquery = (select(
        func.date(Project.date).label('date'),
        func.count(Project.id).label('count')).where(
            Project.date >= n_days_ago).group_by(func.date(
                Project.date)).alias())

    # Select the counts of projects updated on each day in the last n days
    query = (select(subquery.c.date,
                    func.coalesce(subquery.c.count,
                                  0).label("count")).order_by(subquery.c.date.desc()))

    # Execute the query and get the results
    r = await session.execute(query)

    results = [{"date": row[0], "count": row[1]} for row in r]
    dates = [result["date"] for result in results]

    for date in range(num_days):
        date = (n_days_ago + timedelta(days=date)).strftime("%Y-%m-%d")
        if date not in dates:
            results.append({"date": date, "count": 0})

    results.sort(key=lambda x: x["date"])
    return results


# TODO refactor
@router.get("/tags/popular", response_model=list[TagCount])
async def get_top_n_popular_tags(n: int, session: AsyncSession = Depends(get_session)):
    
    # get the count of each tag
    subquery = (select(project_tags.tag_id,
                       func.count(
                           project_tags.tag_id).label('count')).group_by(
                               project_tags.tag_id).alias('subquery'))
    # select the top 10 most used tags
    query = (select(subquery.c.tag_id, subquery.c.count).order_by(
        subquery.c.count.desc()).limit(n))

    r = await session.execute(query)

    sub_results = [(row[0], row[1]) for row in r]
    results = []
    for sub_result in sub_results:
        r = await session.execute(
            select(Tag).where(Tag.tagId == sub_result[0]))
        tag = r.scalar_one_or_none()
        results.append(TagCount(tag=tag, count=sub_result[1]))

    return results