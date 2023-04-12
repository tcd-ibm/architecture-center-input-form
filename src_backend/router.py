from fastapi import APIRouter

from routers import categories, tags, users, projects, statistics


API_PREFIX = "/api/v1"
router = APIRouter(prefix=API_PREFIX)

router.include_router(categories.router)
router.include_router(tags.router)
router.include_router(users.router)
router.include_router(projects.router)
router.include_router(statistics.router)