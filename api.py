'''API v1 for the database'''
from fastapi import APIRouter, Request, Depends, HTTPException, status
# from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.sql import and_, or_, any_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext
from uuid import uuid4
from jose import jwt, JWTError

from db import get_session, init_db
from models import User, UserSignup, UserUpdate, Token, Announcement, Detail, PA, Product, Solution, Type, Vertical, ProjectBase, Project, Tag, Category, CategoryWithTags, ProjectWithUserAndTags, project_tags

from datetime import timedelta, datetime

from typing import List

import re

# openssl rand -hex 32
SECRET_KEY = "d8e632e42229356dbbcd5fdc366a05e9bfaca0193ba016e4fd6cf03307d90241"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

SALT = "fa3e1b071f78d55d833c2df51a3089e5"

DEFAULT_PAGE = 1

DEFAULT_PAGE_SIZE = 30
MAX_PAGE_SIZE = 50
# templates = Jinja2Templates(directory="templates")

# 这里是 tokenUrl，而不是 token_url，是为了和 OAuth2 规范统一
# tokenUrl 是为了指定 OpenAPI 前端登录时的接口地址
# OAuthPasswordBearer 把 Authorization Header 的 Bearer 取出来，然后传给 tokenUrl
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/user/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


@router.on_event("startup")
async def startup():
    await init_db()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password + SALT, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def unauthorized_error(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail=detail,
                         headers={"WWW-Authenticate": "Bearer"})


def _create_token(
    data: dict, expires: timedelta = timedelta(minutes=15)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def _decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise unauthorized_error("Could not validate credentials")


async def get_all_users_db(session: AsyncSession = Depends(
    get_session)) -> List[User]:
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [User(**user.__dict__) for user in users]


async def get_user_db(
    email: str, session: AsyncSession = Depends(get_session)) -> User:
    result = await session.execute(select(User).where(User.email == email))

    return result.scalar_one_or_none()

    # users = result.scalars().all()
    # return [User(**user.__dict__) for user in users]


async def get_current_user(token: str = Depends(oauth2_bearer),
                           session: AsyncSession = Depends(
                               get_session)) -> User:
    error = unauthorized_error("Could not validate credentials")
    payload = _decode_token(token=token)

    username = payload.get("sub")
    if not username:
        raise error
    expires = payload.get("exp")
    if expires < int(datetime.utcnow().timestamp()):
        raise unauthorized_error("Token expired")

    user = await get_user_db(username, session)
    if user is None:
        raise error
    return user


@router.on_event("startup")
async def on_startup():
    await init_db()


@router.post("/user/signup")
async def add_user(user: UserSignup,
                   session: AsyncSession = Depends(get_session)):
    if not user.email or not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email invalid")

    existed_user = await get_user_db(user.email, session)
    if existed_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email registered already")

    if not user.password or len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password invalid, should be at least 8 characters")

    new_user = User(email=user.email,
                    hashed_password=get_password_hash(user.password + SALT),
                    id=str(uuid4()))

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    token = _create_token(
        data={
            "sub": user.username,
            "role": 0
        },
        expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    response = {"access_token": token, "token_type": "bearer"}
    return response


@router.post("/user/update")
async def modify_user(user: UserUpdate,
                      session: AsyncSession = Depends(get_session),
                      current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")

    data = user.dict(exclude_unset=True)
    for k, v in data.items():
        if v is not None:

            if k == "password":
                k, v = "hashed_password", get_password_hash(v + SALT)
            elif k == "email":
                result = await session.execute(
                    select(User).where(User.email == v))
                searched_user = result.scalar_one_or_none()
                if searched_user and searched_user.id != current_user.id:  # if the queried user with same email is not user self
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"email {v} registered already")

            setattr(current_user, k, v)

    session.add(current_user)
    await session.commit(
    )  # flush is actually not needed here since commit will flush automatically
    await session.flush()
    return True


@router.post('/user/delete')
async def delete_user(session: AsyncSession = Depends(get_session),
                      current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")

    result = await session.execute(
        select(User).where(User.id == current_user.id))
    original_instance = result.scalar_one_or_none()
    if not original_instance:
        raise Exception("User not found")

    await session.delete(original_instance)
    await session.commit()
    await session.flush()
    return True


@router.post('/user/token',
             summary="Create access and refresh tokens for user",
             response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(),
                session: AsyncSession = Depends(get_session)):
    user = await get_user_db(form.username, session)
    if not user or not verify_password(form.password, user.hashed_password):
        raise unauthorized_error("Incorrect username or password")

    token = _create_token(
        data={
            "sub": form.username,
            "role": user.role
        },
        expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    response = {"access_token": token, "token_type": "bearer"}
    return response


# Private Endpoints for test only
@router.get("/user/private")
async def get_private_endpoint(current_user: User = Depends(get_current_user)):
    user_data = current_user.__dict__
    user_data.pop("hashed_password")
    return user_data


@router.get("/user/private/admin")
async def get_private_admin_endpoint(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)):
    if not current_user.role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")
    all_users = await get_all_users_db(session)
    for user in all_users:
        user.__dict__.pop("hashed_password")
    return all_users


@router.post("/user/project")
async def add_project(project: ProjectBase,
                      session: AsyncSession = Depends(get_session),
                      current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")

    data = project.dict(exclude_unset=True)
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
                          user=current_user,
                          email=current_user.email)

    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)
    return True


@router.get("/user/project/{id}")
async def get_user_project(id: str,
                           session: AsyncSession = Depends(get_session),
                           current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")

    r = await session.execute(
        select(Project).where(Project.id == id).options(
            selectinload(Project.user), selectinload(Project.tags)))
    project = r.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found")
    if project.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")

    return project


@router.get("/project/{id}", response_model=ProjectWithUserAndTags)
async def get_project_by_id(
    id: str,
    session: AsyncSession = Depends(get_session),
) -> ProjectWithUserAndTags:
    if not id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Project ID is required")

    r = await session.execute(
        select(Project).where(Project.id == id).options(
            selectinload(Project.user), selectinload(Project.tags)))
    project = r.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Project not found")
    return project


@router.get("/user/projects", response_model=List[ProjectWithUserAndTags])
async def get_user_projects(
    per_page: int = DEFAULT_PAGE_SIZE,
    page: int = DEFAULT_PAGE,
    keyword: str = "",
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> List[ProjectWithUserAndTags]:
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")

    r = await session.execute(
        select(Project).where(Project.email == current_user.email).filter(
            Project.title.like(f'%{keyword}%')).options(
                selectinload(Project.user),
                selectinload(Project.tags)).order_by(Project.id).offset(
                    max((page - 1) * per_page,
                        0)).limit(min(per_page, MAX_PAGE_SIZE)))
    return r.scalars().all()


@router.get("/projects", response_model=List[ProjectWithUserAndTags])
async def get_all_projects(
    per_page: int = DEFAULT_PAGE_SIZE,
    page: int = DEFAULT_PAGE,
    keyword: str = "",
    tags: str = "",
    session: AsyncSession = Depends(get_session),
) -> List[ProjectWithUserAndTags]:

    if tags:
        try:
            tag_ids = [int(tag) for tag in tags.split(',')]

            r = await session.execute(
                select(Tag).options(joinedload(Tag.category)).filter(
                    Tag.tagId.in_(tag_ids)))
            tagInstances = r.scalars().all()
            for tag in tag_ids:
                if tag not in [
                        tagInstance.tagId for tagInstance in tagInstances
                ]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Tag with ID {tag} not found")

            r = await session.execute(select(func.count(Category.categoryId)))
            num_categories = r.scalar_one_or_none()

            tag_ids_by_category = [[
                tag.tagId for tag in tagInstances
                if tag.categoryId == categoryId
            ] for categoryId in range(1, num_categories + 1)]

            conditions = []
            for i, tag_list in enumerate(tag_ids_by_category):
                if tag_list:
                    conditions.append(
                        and_(Project.tags.any(Tag.categoryId == (i + 1)),
                             Project.tags.any(Tag.tagId.in_(tag_list))))

            query = select(Project).group_by(
                    Project.id).filter(
                        Project.title.like(f'%{keyword}%')).options(
                            selectinload(Project.user),
                            selectinload(Project.tags)).order_by(
                                Project.id).offset(
                                    max((page - 1) * per_page,
                                        0)).limit(min(per_page, MAX_PAGE_SIZE))

            query = query.filter(and_(*conditions)) if conditions else query

            r = await session.execute(query)

            return r.scalars().all()
        except ValueError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Tags must be integers")

    r = await session.execute(
        select(Project).filter(Project.title.like(f'%{keyword}%')).options(
            selectinload(Project.user),
            selectinload(Project.tags)).order_by(Project.id).offset(
                max((page - 1) * per_page,
                    0)).limit(min(per_page, MAX_PAGE_SIZE)))
    return r.scalars().all()


@router.get("/announcement/{aid}", response_model=List[Announcement])
async def fetch_announcement(request: Request,
                             session: AsyncSession = Depends(get_session),
                             aid: int = 0) -> List[Announcement]:
    r = await session.execute(
        select(Announcement).filter_by(**request.query_params._dict, aid=aid)
    ) if aid else await session.execute(
        select(Announcement).filter_by(
            **request.query_params._dict).order_by(Announcement.aid))
    return r.scalars().all()


@router.get("/detail/{ppid}", response_model=List[Detail])
async def fetch_detail(request: Request,
                       session: AsyncSession = Depends(get_session),
                       ppid: int = 0) -> List[Detail]:
    r = await session.execute(
        select(Detail).filter_by(**request.query_params._dict, ppid=ppid)
    ) if ppid else await session.execute(
        select(Detail).filter_by(
            **request.query_params._dict).order_by(Detail.ppid))
    return r.scalars().all()


@router.get("/pa/{ppid}", response_model=List[PA])
async def fetch_pa(request: Request,
                   session: AsyncSession = Depends(get_session),
                   ppid: int = 0) -> List[PA]:
    r = await session.execute(
        select(PA).filter_by(**request.query_params._dict, ppid=ppid)
    ) if ppid else await session.execute(
        select(PA).filter_by(**request.query_params._dict).order_by(PA.ppid))
    return r.scalars().all()


@router.get("/tag/{tagId}", response_model=List[Tag])
async def fetch_tag(request: Request,
                    session: AsyncSession = Depends(get_session),
                    tagId: int = 0) -> List[Tag]:
    r = await session.execute(
        select(Tag).filter_by(**request.query_params._dict, tagId=tagId))
    return r.scalars().all()


@router.get("/tags", response_model=List[CategoryWithTags])
async def fetch_tags(session: AsyncSession = Depends(
    get_session)) -> List[CategoryWithTags]:

    r = await session.execute(
        select(Category).options(selectinload(Category.tags)).order_by(
            Category.categoryId))
    return r.scalars().all()


@router.get("/product", response_model=List[Product])
async def fetch_product(
    request: Request, session: AsyncSession = Depends(get_session)
) -> List[Product]:
    r = await session.execute(
        select(Product).filter_by(**request.query_params._dict).order_by(
            Product.pid))
    return r.scalars().all()


@router.get("/solution", response_model=List[Solution])
async def fetch_solution(
    request: Request, session: AsyncSession = Depends(get_session)
) -> List[Solution]:
    r = await session.execute(
        select(Solution).filter_by(**request.query_params._dict).order_by(
            Solution.sid))
    return r.scalars().all()


@router.get("/type", response_model=List[Type])
async def fetch_type(
    request: Request,
    session: AsyncSession = Depends(get_session)) -> List[Type]:
    r = await session.execute(
        select(Type).filter_by(**request.query_params._dict).order_by(Type.tid)
    )
    return r.scalars().all()


@router.get("/vertical", response_model=List[Vertical])
async def fetch_vertical(
    request: Request, session: AsyncSession = Depends(get_session)
) -> List[Vertical]:
    r = await session.execute(
        select(Vertical).filter_by(**request.query_params._dict).order_by(
            Vertical.vid))
    return r.scalars().all()
