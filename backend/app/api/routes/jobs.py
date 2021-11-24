from typing import List
from fastapi import APIRouter


from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
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


@router.get("/{id}/", response_model=JobPublic, name="jobs:get-job-by-id")
async def get_job_by_id(
    id: str, jobs_repo: JobsRepository = Depends(get_repository(JobsRepository))
) -> JobPublic:
    job = await jobs_repo.get_job_by_id(id=id)
    if not job:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="No job found with that id.")
    return job


@router.post("/", response_model=JobPublic, name="jobs:create-job", status_code=HTTP_201_CREATED)
async def create_new_job(
    new_job: JobCreate = Body(..., embed=False),
    jobs_repo: JobsRepository = Depends(get_repository(JobsRepository)),
) -> JobPublic:
    created_job = await jobs_repo.create_job(new_job=new_job)
    return created_job
