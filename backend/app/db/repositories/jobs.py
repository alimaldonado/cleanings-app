from app.db.repositories.base import BaseRepository
from app.models.job import JobCreate, JobUpdate, JobInDB


CREATE_JOB_QUERY = """
    INSERT INTO jobs (name, description, price, job_type)
    VALUES (:name, :description, :price, :job_type)
    RETURNING id, name, description, price, job_type;
"""


class JobsRepository(BaseRepository):
    """"
    All database actions associated with the Job resource
    """
    async def create_job(self, *, new_job: JobCreate) -> JobInDB:
        query_values = new_job.dict()
        job = await self.db.fetch_one(query=CREATE_JOB_QUERY, values=query_values)
        return JobInDB(**job)
