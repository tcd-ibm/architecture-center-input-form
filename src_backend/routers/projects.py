from typing import Union
from fastapi import APIRouter, Depends, Form, HTTPException, Response, status, UploadFile
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.sql import and_
from datetime import datetime
from dateutil import parser as dateparser
from uuid import UUID, uuid4

from db import get_session
#from api import get_current_user, is_admin, DEFAULT_PAGE, DEFAULT_PAGE_SIZE, get_current_time
from api import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, get_current_time
from utils.auth import get_current_user, is_admin, require_admin, require_authenticated
from utils.data import is_valid_iso_date, is_valid_uuid, patch_object, set_count_headers
from utils.FileStorageManager import file_storage
from utils.sql import get_all, get_one, get_some
from models import Category, Project, ProjectContent, ProjectContentAdditional, \
    ProjectContentAdditionalAdmin, ProjectInfo, ProjectInfoAdditionalAdmin, Tag, User


router = APIRouter(prefix='/projects', tags=['projects'])


# TODO finish refactoring
@router.get('', response_model=Union[list[ProjectInfoAdditionalAdmin], list[ProjectInfo]])
async def query_projects(response: Response,
                         start_date: datetime = datetime.min,
                         end_date: datetime = Depends(get_current_time),
                         per_page: int = DEFAULT_PAGE_SIZE,
                         page: int = DEFAULT_PAGE,
                         keyword: str = "",
                         tags: str = "",
                         additional_info: bool = False,
                         session: AsyncSession = Depends(get_session),
                         current_user: User | None = Depends(get_current_user)):
    
    if additional_info:
        await require_admin(current_user)

    conditions = []

    if tags:
        try:
            tag_ids = [int(tag) for tag in tags.split(',')]
        except ValueError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid tag id")

        tag_instances = await get_all(session,
            select(Tag)
            .options(joinedload(Tag.category))
            .filter(Tag.tagId.in_(tag_ids))                     
        )
        tag_instances_ids = [ instance.tagId for instance in tag_instances ]

        for tag_id in tag_ids:
            if tag_id not in tag_instances_ids:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid tag id")

        num_categories = await get_one(session, select(func.count(Category.categoryId)))

        # TODO refactor
        tag_ids_by_category = [[
            tag.tagId for tag in tag_instances
            if tag.categoryId == categoryId
        ] for categoryId in range(1, num_categories + 1)]

        for i, tag_list in enumerate(tag_ids_by_category):
            if tag_list:
                conditions.append(
                    Project.tags.any(
                        and_(
                            Tag.categoryId == (i + 1), 
                            Project.tags.any(Tag.tagId.in_(tag_list))
                        )
                    )
                )

    query = select(
        func.count(Project.id)
    ).filter(
        Project.title.like(f'%{keyword}%'), 
        Project.date >= start_date,
        Project.date <= end_date
    )
    if not additional_info:
        query = query.filter(Project.is_live == True)
        query = query.filter(Project.is_featured == False)
    query = query.filter(and_(*conditions)) if conditions else query

    count = await get_one(session, query)
    set_count_headers(response, count, per_page)

    query = select(
        Project
    ).filter(
        Project.title.like(f'%{keyword}%'),
        Project.date >= start_date, 
        Project.date <= end_date
    ).options(
        selectinload(Project.user), 
        selectinload(Project.tags)
    ).order_by(
        Project.date.desc()
    )
    if not additional_info:
        query = query.filter(Project.is_live == True)
        query = query.filter(Project.is_featured == False)
    query = query.filter(and_(*conditions)) if conditions else query

    data = await get_some(session, page, per_page, query)
    data = [ vars(instance) for instance in data ]

    if additional_info:
        return [ ProjectInfoAdditionalAdmin(**item) for item in data ]
    
    return [ ProjectInfo(**item) for item in data ]


@router.get('/featured', response_model=list[ProjectInfo])
async def get_featured_projects(session: AsyncSession = Depends(get_session)):
    instances = await get_all(session,
        select(Project)
        .options(selectinload(Project.tags))
        .where(Project.is_featured == True,
               Project.is_live == True)                          
    )
    return instances


@router.get('/{id}', response_model=Union[ProjectContentAdditionalAdmin, ProjectContentAdditional, ProjectContent])
async def get_project(id: str,
                      additional_info: bool = False,
                      session: AsyncSession = Depends(get_session),
                      current_user: User | None = Depends(get_current_user)):
    
    if additional_info:
        await require_authenticated(current_user)
    
    instance = await get_project_by_id(session, id)

    if additional_info:
        ensure_admin_or_self(current_user, str(instance.user.id))
    
    if not instance.is_live:
        await require_authenticated(current_user)
        ensure_admin_or_self(current_user, str(instance.user.id))
    
    data = vars(instance)

    if additional_info and is_admin(current_user):
        return ProjectContentAdditionalAdmin(**data)
    elif additional_info:
        return ProjectContentAdditional(**data)
    else:
        return ProjectContent(**data)


@router.post('', response_model=ProjectContentAdditional)
async def create_project(title: str = Form(),
                         link: str = Form(regex=r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'),
                         completionDate: str = Form(),
                         description: str = Form(),
                         content: str = Form(),
                         tags: str = Form(""),
                         imageFile: UploadFile | None = None,
                         session: AsyncSession = Depends(get_session),
                         current_user: User = Depends(require_authenticated)):
    

    if not is_valid_iso_date(completionDate):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid date")

    data = {
        "title": title,
        "link": link,
        "date": dateparser.parse(completionDate) if completionDate else None,
        "description": description,
        "content": content,
        "tags": await get_tags(session, tags) if tags else []
    }

    new_project = Project(
        **data,
        id=str(uuid4()),
        user_id=current_user.id,
        user=current_user
    )

    if imageFile:
        contents = imageFile.file.read()
        file_storage.write(f'images/{str(new_project.id)}.png', contents)
        # tempFilePath = "./database/content/images/temp-" + str(
        #     new_project.id) + "-" + imageFile.filename
        # try:
        #     contents = imageFile.file.read()
        #     with open(tempFilePath, 'wb') as f:
        #         f.write(contents)
        # except Exception:
        #     raise HTTPException(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # finally:
        #     imageFile.file.close()

        # try:
        #     im = Image.open(tempFilePath)
        #     im.verify()
        # except Exception:
        #     if os.path.exists(tempFilePath):
        #         os.remove(tempFilePath)
        #     raise HTTPException(
        #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        #         detail="Invalid image file format")
        # finally:
        #     im.close()

        # filePath = "./database/content/images/" + str(new_project.id) + ".png"
        # try:
        #     im = Image.open(tempFilePath)
        #     im.save(filePath)
        # except Exception:
        #     raise HTTPException(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # finally:
        #     im.close()
        #     if os.path.exists(tempFilePath):
        #         os.remove(tempFilePath)

    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)

    # needed for adding tags to the response
    # TODO research whether it can be avoided
    new_project = await get_one(session,
        select(Project)
        .options(selectinload(Project.user),
                 selectinload(Project.tags))
        .where(Project.id == new_project.id)                     
    )

    return new_project


# TODO image handling
@router.patch('/{id}', response_model=ProjectContentAdditional)
async def modify_project(id: str,
                         title: str | None = Form(None),
                         link: str | None = Form(default=None, regex=r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'),
                         completionDate: str | None = Form(None),
                         description: str | None = Form(None),
                         content: str | None = Form(None),
                         tags: str | None = Form(None),
                         is_live: bool | None = Form(None),
                         is_featured: bool | None = Form(None),
                         imageFile: UploadFile | None = None,
                         session: AsyncSession = Depends(get_session),
                         current_user: User = Depends(require_authenticated)):
    
    if completionDate and not is_valid_iso_date(completionDate):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid date")

    instance = await get_project_by_id(session, id)

    if is_live:
        await require_admin(current_user)

    ensure_admin_or_self(current_user, str(instance.user.id))

    data = {
        "title": title,
        "link": link,
        "date": dateparser.parse(completionDate) if completionDate else None,
        "description": description,
        "content": content,
        "is_live": is_live,
        "is_featured": is_featured,
        "tags": await get_tags(session, tags) if tags else []
    }

    if len(data["tags"]) == 0:
        data["tags"] = None

    patch_object(instance, data)

    session.add(instance)
    await session.commit()
    await session.refresh(instance)

    instance = await get_one(session,
        select(Project)
        .options(selectinload(Project.user),
                 selectinload(Project.tags))
        .where(Project.id == id)                     
    )

    return instance


@router.delete("/{id}")
async def delete_project(id: str,
                         session: AsyncSession = Depends(get_session),
                         current_user: User = Depends(require_authenticated)):

    instance = await get_project_by_id(session, id)
    
    ensure_admin_or_self(current_user, str(instance.user.id))

    await session.delete(instance)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# TODO ensure that project is live
@router.get('/{id}/image')
async def get_project_image(id: str):

    filePath = f'images/{id}.png'
    image_bytes = file_storage.read_if_exists(filePath)

    if image_bytes:
        return Response(content=image_bytes, media_type="image/png")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project image not found")


async def get_project_by_id(session: AsyncSession, id: str):
    if not is_valid_uuid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Project not found')
    
    instance = await get_one(session,
        select(Project)
        .options(selectinload(Project.user),
                 selectinload(Project.tags))
        .where(Project.id == UUID(id))                     
    )

    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Project not found')
    
    return instance

def ensure_admin_or_self(user: User, userId: str) -> None:
    if not is_admin(user) and str(user.id) != userId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Non-admin user can only access self.")
    
async def get_tags(session: AsyncSession, tag_ids: str) -> list[Tag]:
    try:
        tag_ids = [int(tag) for tag in tag_ids.split(',')]
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid tag id")
    
    tags = []

    for tag_id in tag_ids:
        tag = await get_one(session,
            select(Tag).where(Tag.tagId == tag_id)      
        )
        if not tag:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid tag id")
        
        tags.append(tag)

    return tags
