from fastapi import APIRouter, Depends, Form, HTTPException, Response, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from dateutil import parser as dateparser
from uuid import uuid4

from db import get_session
from api import get_current_user, is_admin
from utils.auth import require_admin, require_authenticated
from utils.data import is_valid_iso_date, is_valid_uuid, patch_object
from utils.FileStorageManager import file_storage
from utils.sql import get_one
from models import Project, ProjectContent, ProjectContentAdditional, ProjectContentAdditionalAdmin, Tag, User


router = APIRouter(prefix='/projects', tags=['projects'])


@router.get('/{id}')
async def get_project(id: str,
                      additional_info: bool = False,
                      session: AsyncSession = Depends(get_session),
                      current_user: User | None = Depends(get_current_user)):
    
    if additional_info:
        await require_authenticated(current_user)
    
    if not is_valid_uuid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Project not found')
    
    instance = await get_one(session,
        select(Project)
        .options(selectinload(Project.user),
                 selectinload(Project.tags))
        .where(Project.id == id)                     
    )

    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Project not found')
    
    if not instance.is_live:
        await require_authenticated(current_user)
        if not is_admin(current_user) and instance.user.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Non-admin user can only access their projects.")

    if additional_info and not is_admin(current_user) and instance.user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Non-admin user can only access their projects.")
    
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
    
    # if not current_user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail="Unauthorized")

    if not is_valid_iso_date(completionDate):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid date")

    data = {
        "title": title,
        "link": link,
        "date": dateparser.parse(completionDate) if completionDate else None,
        "description": description,
        "content": content,
        "tags": [int(tagId) for tagId in tags.split(",")] if tags else []
    }
    tags = []
    for tagId in data["tags"]:
        if not isinstance(tagId, int):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Tag must be an integer")
        r = await session.execute(select(Tag).where(Tag.tagId == tagId))
        tag = r.scalar_one_or_none()
        if not tag:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Tag with ID {tagId} not found")
        tags.append(tag)

    data["tags"] = tags
    new_project = Project(**data,
                          id=str(uuid4()),
                          user_id=current_user.id,
                          #date=datetime.utcnow(),
                          user=current_user)

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
    # TODO can it be avoided?
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
                         imageFile: UploadFile | None = None,
                         session: AsyncSession = Depends(get_session),
                         current_user: User = Depends(require_authenticated)):
    
    if completionDate and not is_valid_iso_date(completionDate):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid date")
    
    # if not current_user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail="Unauthorized")

    if not is_valid_uuid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Project not found')
    
    instance = await get_one(session,
        select(Project)
        .options(selectinload(Project.user),
                 selectinload(Project.tags))
        .where(Project.id == id)                     
    )

    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Project not found')

    # r = await session.execute(
    #     select(Project).options(selectinload(Project.user),
    #                             selectinload(
    #                                 Project.tags)).where(Project.id == id))
    # originalProject = r.scalar_one_or_none()

    # if not originalProject:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail=f"Project with ID {id} not found")

    if not is_admin(current_user) and instance.user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Non-admin user can only access their projects.")

    # if originalProject.user.id != current_user.id and not is_admin(
    #         current_user):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail="Unauthorized")

    if is_live:
        await require_admin(current_user)

    #data = project.dict(exclude_unset=True)
    # for k, v in data.items():
    #     if v is not None:
    #         if k == "is_live":
    #             if not is_admin(current_user):
    #                 raise HTTPException(
    #                     status_code=status.HTTP_401_UNAUTHORIZED,
    #                     detail="Unauthorized")
    #             setattr(originalProject, k, v)
    #         elif k == "tags":
    #             tags = []
    #             for tagId in v:
    #                 if not isinstance(tagId, int):
    #                     raise HTTPException(
    #                         status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail=f"TagId {tagId} must be an integer")
    #                 r = await session.execute(
    #                     select(Tag).where(Tag.tagId == tagId))
    #                 tag = r.scalar_one_or_none()
    #                 if not tag:
    #                     raise HTTPException(
    #                         status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail=f"Tag with ID {tagId} not found")
    #                 tags.append(tag)
    #             setattr(originalProject, k, tags)
    #         else:
    #             setattr(originalProject, k, v)

    data = {
        "title": title,
        "link": link,
        "date": dateparser.parse(completionDate) if completionDate else None,
        "description": description,
        "content": content,
        "is_live": is_live,
        "tags": [int(tagId) for tagId in tags.split(",")] if tags else []
    }
    tags = []
    for tagId in data["tags"]:
        if not isinstance(tagId, int):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Tag must be an integer")
        r = await session.execute(select(Tag).where(Tag.tagId == tagId))
        tag = r.scalar_one_or_none()
        if not tag:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Tag with ID {tagId} not found")
        tags.append(tag)

    data["tags"] = tags
    if len(tags) == 0:
        data["tags"] = None

    patch_object(instance, data)

    session.add(instance)
    await session.commit()
    await session.refresh(instance)
    return instance


@router.delete("/{id}")
async def delete_project(id: str,
                         session: AsyncSession = Depends(get_session),
                         current_user: User = Depends(require_authenticated)):
    # if not current_user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail="Unauthorized")

    if not is_valid_uuid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Project not found')

    instance = await get_one(session,
        select(Project)
        .options(selectinload(Project.user),
                 selectinload(Project.tags))
        .where(Project.id == id)                     
    )

    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Project not found')

    # r = await session.execute(
    #     select(Project).options(selectinload(Project.user),
    #                             selectinload(
    #                                 Project.tags)).where(Project.id == id))
    # originalProject = r.scalar_one_or_none()

    # if not originalProject:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail=f"Project with ID {id} not found")

    # if not is_admin(
    #         current_user) and originalProject.user.id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail="Unauthorized")
    
    if not is_admin(current_user) and instance.user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Non-admin user can only access their projects.")

    await session.delete(instance)
    await session.commit()
    #await session.flush()
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
