import re
from typing import List
from fastapi import APIRouter

from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from fastapi import APIRouter, Body, Depends, HTTPException, Path

from app.models.job import JobCreate, JobPublic, JobUpdate
from app.db.repositories.jobs import JobsRepository
from app.api.dependencies.database import get_repository
from app.models.user import UserInDB
from app.api.dependencies.auth import get_current_active_user


router = APIRouter()


@router.get("/{id}/", response_model=JobPublic, name="jobs:get-job-by-id")
async def get_job_by_id(
    id: str = Path(...),
    current_user: UserInDB = Depends(get_current_active_user),
    jobs_repo: JobsRepository = Depends(get_repository(JobsRepository))
) -> JobPublic:
    job = await jobs_repo.get_job_by_id(id=id, requesting_user=current_user)

    if not job:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="No job found with that id.")
    return job


@router.post("/", response_model=JobPublic, name="jobs:create-job", status_code=HTTP_201_CREATED)
async def create_new_job(
    new_job: JobCreate = Body(..., embed=False),
    current_user: UserInDB = Depends(get_current_active_user),
    jobs_repo: JobsRepository = Depends(get_repository(JobsRepository)),
) -> JobPublic:
    created_job = await jobs_repo.create_job(
        new_job=new_job,
        requesting_user=current_user
    )
    return created_job


@router.get("/", response_model=List[JobPublic], name="jobs:list-all-user-jobs")
async def get_all_jobs(
    current_user: UserInDB = Depends(get_current_active_user),
    jobs_repo: JobsRepository = Depends(get_repository(JobsRepository))
) -> List[JobPublic]:
    return await jobs_repo.list_all_user_jobs(
        requesting_user=current_user
    )


@router.put(
    "/{id}/",
    response_model=JobPublic,
    name="jobs:update-job-by-id",
)
async def update_job_by_id(
    id: str = Path(..., title="The ID of the job to update."),
    job_update: JobUpdate = Body(..., embed=False),
    current_user: UserInDB = Depends(get_current_active_user),
    jobs_repo: JobsRepository = Depends(get_repository(JobsRepository)),
) -> JobPublic:
    updated_job = await jobs_repo.update_job(
        id=id, job_update=job_update, requesting_user=current_user
    )

    if not updated_job:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No job found with that id.",
        )
    return updated_job


@router.delete("/{id}/", response_model=str, name="jobs:delete-job-by-id")
async def delete_job_by_id(
    id: str = Path(..., title="The ID of the job to delete."),
    current_user: UserInDB = Depends(get_current_active_user),
    jobs_repo: JobsRepository = Depends(get_repository(JobsRepository)),
) -> str:
    deleted_id = await jobs_repo.delete_job_by_id(id=id, requesting_user=current_user)

    if not deleted_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No job found with that id.",
        )

    return deleted_id
