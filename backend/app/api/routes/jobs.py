from typing import List
from fastapi import APIRouter


from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED
from app.models.job import JobCreate, JobPublic
from app.db.repositories.jobs import JobsRepository
from app.api.dependencies.database import get_repository


router = APIRouter()


@router.get("/")
async def get_all_jobs() -> List[dict]:
    jobs = [
        {"id": 1, "name": "Night Dress", "type": "full", "price": 29.99},
        {"id": 2, "name": "Night Dress", "type": "full", "price": 29.99}
    ]

    return jobs


@router.post("/", response_model=JobPublic, name="jobs:create-job", status_code=HTTP_201_CREATED)
async def create_new_job(
    new_job: JobCreate = Body(..., embed=False),
    jobs_repo: JobsRepository = Depends(get_repository(JobsRepository)),
) -> JobPublic:
    created_job = await jobs_repo.create_job(new_job=new_job)
    return created_job
