from typing import Any, Generator

import pytest

from fastapi import Depends, FastAPI
from httpx import AsyncClient
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select


import api
from routers import categories
from api import get_current_user, oauth2_bearer
from models import SQLModel, User
from db import get_session


API_PREFIX = '/api/v1'

def start_application() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["POST", "GET", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Total-Count", "X-Total-Pages"]
    )
    api.router.include_router(categories.router)
    app.include_router(api.router)
    return app

SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./test_db.test.db'
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def add_users_data() -> None:
    connection = await engine.connect()
    transaction = await connection.begin()
    session = SessionTesting(bind=connection)
    admin_user = User(email='admin@admin.com', role=1, id='170b76ca-9cdb-4d3b-af35-f3c0202d7357')
    regular_user = User(email='user@user.com', id='ec33e02c-ec82-4f4d-88be-23b2cdb6f097')
    session.add_all([admin_user, regular_user])
    await session.commit()
    await transaction.commit()
    await connection.close()

@pytest.fixture()
async def app() -> Generator[FastAPI, Any, None]:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        _app = start_application()
        await add_users_data()
        yield _app
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest.fixture()
async def db_test_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = await engine.connect()
    transaction = await connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    await session.close()
    await transaction.rollback()
    await connection.close()

@pytest.fixture()
def dependency_override(app: FastAPI, db_test_session: SessionTesting) -> None:

    def _get_db_test_session():
        try:
            yield db_test_session
        finally:
            pass

    async def _get_user(token: str | None = Depends(oauth2_bearer)):
        if token == 'admintoken':
            result = await db_test_session.execute(select(User).where(User.email == 'admin@admin.com'))
            return result.scalar_one_or_none()
        if token == 'usertoken':
            result = await db_test_session.execute(select(User).where(User.email == 'user@user.com'))
            return result.scalar_one_or_none()
        return None

    app.dependency_overrides[get_session] = _get_db_test_session
    app.dependency_overrides[get_current_user] = _get_user

@pytest.fixture()
async def client(app: FastAPI, dependency_override) -> Generator[AsyncClient, Any, None]:
    async with AsyncClient(app=app, base_url='http://testserver' + API_PREFIX) as client:
        yield client

@pytest.fixture()
async def userClient(app: FastAPI, dependency_override) -> Generator[AsyncClient, Any, None]:
    headers = { 'Authorization': 'Bearer usertoken' } 
    async with AsyncClient(app=app, base_url='http://testserver' + API_PREFIX, headers=headers) as client:
        yield client

@pytest.fixture()
async def adminClient(app: FastAPI, dependency_override) -> Generator[AsyncClient, Any, None]:
    headers = { 'Authorization': 'Bearer admintoken' } 
    async with AsyncClient(app=app, base_url='http://testserver' + API_PREFIX, headers=headers) as client:
        yield client

@pytest.fixture
def anyio_backend():
    return 'asyncio'