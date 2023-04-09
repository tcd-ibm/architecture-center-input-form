from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session


router = APIRouter(prefix='/projects', tags=['projects'])


