from app.db.repositories.base import BaseRepository
from app.models.job import JobCreate, JobUpdate, JobInDB
from uuid import  uuid4


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

