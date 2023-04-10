from fastapi import APIRouter, Depends, Form, HTTPException, Response, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import uuid4

from db import get_session
from utils.auth import require_authenticated
from utils.FileStorageManager import file_storage
from models import Project, Tag, User


router = APIRouter(prefix='/projects', tags=['projects'])


@router.post('')
async def create_project(title: str = Form(),
                         link: str = Form(),
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

    data = {
        "title": title,
        "link": link,
        "date": completionDate,
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
    return new_project

@router.get('/{id}/image')
async def get_project_image(id: str):

    filePath = f'images/{id}.png'
    image_bytes = file_storage.read_if_exists(filePath)

    if image_bytes:
        return Response(content=image_bytes, media_type="image/png")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project image not found")
