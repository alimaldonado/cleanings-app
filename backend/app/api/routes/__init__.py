from fastapi import APIRouter
from app.api.routes.jobs import router as jobs_router

router = APIRouter()

router.include_router(
    jobs_router,
    prefix="/jobs",
    tags=["jobs"]
)
