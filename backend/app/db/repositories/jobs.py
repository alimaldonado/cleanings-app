from typing import List

from fastapi.exceptions import HTTPException
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from app.db.repositories.base import BaseRepository
from app.models.job import JobCreate, JobUpdate, JobInDB
from uuid import uuid4

from app.models.user import UserInDB


CREATE_JOB_QUERY = """
    INSERT INTO jobs (id, name, description, price, job_type, owner)
    VALUES (:id, :name, :description, :price, :job_type, :owner)
    RETURNING id, name, description, price, job_type, owner, created_at ,updated_at;
"""

GET_JOB_BY_ID_QUERY = """
    SELECT id, name, description, price, job_type, owner, created_at, updated_at
    FROM jobs
    WHERE id = :id;
"""

GET_ALL_JOBS_QUERY = """
    SELECT id, name, description, price, job_type  
    FROM jobs;  
"""

LIST_ALL_USER_JOBS_QUERY = """
    SELECT id, name, description, price, job_type, owner, created_at, updated_at
    FROM jobs
    WHERE owner = :owner;
"""

UPDATE_JOB_BY_ID_QUERY = """
    UPDATE jobs  
    SET name         = :name,  
        description  = :description,  
        price        = :price,  
        job_type = :job_type  
    WHERE id = :id  AND owner = :owner
    RETURNING id, name, description, price, job_type, owner, created_at, updated_at;  
"""

DELETE_JOB_BY_ID_QUERY = """
    DELETE FROM jobs  
    WHERE id = :id AND owner = :owner
    RETURNING id;  
"""


class JobsRepository(BaseRepository):
    """"
    All database actions associated with the Job resource
    """
    async def create_job(self, *, new_job: JobCreate, requesting_user: UserInDB) -> JobInDB:

        job = await self.db.fetch_one(
            query=CREATE_JOB_QUERY,
            values={
                **new_job.dict(),
                "id": str(uuid4()),
                "owner": requesting_user.id
            }
        )
        return JobInDB(**job)

    async def get_job_by_id(self, *, id: int, requesting_user: UserInDB) -> JobInDB:
        job = await self.db.fetch_one(query=GET_JOB_BY_ID_QUERY, values={"id": id})
        if not job:
            return None
        return JobInDB(**job)

    async def list_all_user_jobs(self, requesting_user: UserInDB) -> List[JobInDB]:
        jobs_records = await self.db.fetch_all(
            query=LIST_ALL_USER_JOBS_QUERY, values={
                "owner": requesting_user.id}
        )

        return [JobInDB(**l) for l in jobs_records]

    async def get_all_jobs(self) -> List[JobInDB]:
        job_records = await self.db.fetch_all(
            query=GET_ALL_JOBS_QUERY,
        )
        return [JobInDB(**l) for l in job_records]

    async def update_job(
        self, *, id: int, job_update: JobUpdate, requesting_user: UserInDB
    ) -> JobInDB:
        job = await self.get_job_by_id(id=id, requesting_user=requesting_user)

        if not job:
            return None

        if job.owner != requesting_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Users are only able to  update jobs that they created.",
            )

        job_update_params = job.copy(
            update=job_update.dict(exclude_unset=True),
        )

        if job_update_params.job_type is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid job type. Cannot be None.",
            )

        updated_job = await self.db.fetch_one(
            query=UPDATE_JOB_BY_ID_QUERY,
            values={
                **job_update_params.dict(exclude={"created_at", "updated_at"}),
                "owner": requesting_user.id
            },
        )
        return JobInDB(**updated_job)

    async def delete_job_by_id(self, *, id: str, requesting_user: UserInDB) -> int:
        job = await self.get_job_by_id(id=id, requesting_user=requesting_user)

        if not job:
            return None

        if job.owner != requesting_user.id:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Users are only able to delete jobs that they created.",
            )

        deleted_id = await self.db.execute(
            query=DELETE_JOB_BY_ID_QUERY,
            values={"id": id, "owner": requesting_user.id},
        )

        return deleted_id
