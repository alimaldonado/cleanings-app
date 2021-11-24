import uuid
import pytest
from httpx import AsyncClient
from fastapi import FastAPI

from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
)

from app.models.job import JobCreate, JobInDB


pytestmark = pytest.mark.asyncio


@pytest.fixture
def new_job():
    return JobCreate(
        name="test job",
        description="test description",
        price=0.00,
        job_type="spot_clean",
    )


class TestJobsRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("jobs:create-job"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("jobs:create-job"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


class TestCreateJob:
    async def test_valid_input_creates_job(
        self, app: FastAPI, client: AsyncClient, new_job: JobCreate
    ) -> None:
        res = await client.post(
            app.url_path_for("jobs:create-job"), json=new_job.dict()
        )
        if res.status_code != HTTP_201_CREATED:
            print(res.json())
        assert res.status_code == HTTP_201_CREATED
        created_job = JobCreate(**res.json())
        assert created_job == new_job


class TestGetJob:
    async def test_get_job_by_id(self, app: FastAPI, client: AsyncClient, test_job: JobInDB) -> None:

        res = await client.get(app.url_path_for("jobs:get-job-by-id", id=test_job.id))
        assert res.status_code == HTTP_200_OK
        job = JobInDB(**res.json())
        assert job.id == test_job.id

    @pytest.mark.parametrize(
        "id, status_code",
        (
            (str(uuid.uuid4()), 404),
            (None, 404),
        ),
    )
    async def test_wrong_id_returns_error(
        self, app: FastAPI, client: AsyncClient, id: str, status_code: int
    ) -> None:
        res = await client.get(app.url_path_for("jobs:get-job-by-id", id=id))

        assert res.status_code == status_code
