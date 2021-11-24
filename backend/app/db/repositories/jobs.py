from typing import List

from fastapi.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from app.db.repositories.base import BaseRepository
from app.models.job import JobCreate, JobUpdate, JobInDB
from uuid import uuid4


CREATE_JOB_QUERY = """
    INSERT INTO jobs (id, name, description, price, job_type)
    VALUES (:id, :name, :description, :price, :job_type)
    RETURNING id, name, description, price, job_type;
"""

GET_JOB_BY_ID_QUERY = """
    SELECT id, name, description, price, job_type
    FROM jobs
    WHERE id = :id;
"""

GET_ALL_JOBS_QUERY = """
    SELECT id, name, description, price, job_type  
    FROM jobs;  
"""

UPDATE_JOB_BY_ID_QUERY = """
    UPDATE jobs  
    SET name         = :name,  
        description  = :description,  
        price        = :price,  
        job_type = :job_type  
    WHERE id = :id  
    RETURNING id, name, description, price, job_type;  
"""

DELETE_JOB_BY_ID_QUERY = """
    DELETE FROM jobs  
    WHERE id = :id  
    RETURNING id;  
"""


class JobsRepository(BaseRepository):
    """"
    All database actions associated with the Job resource
    """
    async def create_job(self, *, new_job: JobCreate) -> JobInDB:
        query_values = new_job.dict()
        query_values["id"] = str(uuid4())
        job = await self.db.fetch_one(query=CREATE_JOB_QUERY, values=query_values)
        return JobInDB(**job)

    async def get_job_by_id(self, *, id: int) -> JobInDB:
        job = await self.db.fetch_one(query=GET_JOB_BY_ID_QUERY, values={"id": id})
        if not job:
            return None
        return JobInDB(**job)

    async def get_all_jobs(self) -> List[JobInDB]:
        job_records = await self.db.fetch_all(
            query=GET_ALL_JOBS_QUERY,
        )
        return [JobInDB(**l) for l in job_records]

    async def update_job(
        self, *, id: int, job_update: JobUpdate,
    ) -> JobInDB:
        job = await self.get_job_by_id(id=id)
        if not job:
            return None
        job_update_params = job.copy(
            update=job_update.dict(exclude_unset=True),
        )
        if job_update_params.job_type is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid job type. Cannot be None.",
            )

        # TODO: remove try catch and add custom exceptions
        try:
            updated_job = await self.db.fetch_one(
                query=UPDATE_JOB_BY_ID_QUERY,
                values=job_update_params.dict(),
            )
            return JobInDB(**updated_job)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid update params.",
            )

    async def delete_job_by_id(self, *, id: str) -> int:
        job = await self.get_job_by_id(id=id)
        if not job:
            return None
        deleted_id = await self.db.execute(
            query=DELETE_JOB_BY_ID_QUERY,
            values={"id": id},
        )
        return deleted_id
