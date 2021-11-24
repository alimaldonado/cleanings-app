from typing import List, Union
import uuid
import pytest
from httpx import AsyncClient
from fastapi import FastAPI

from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
)

from app.models.job import JobCreate, JobInDB


pytestmark = pytest.mark.asyncio

FAKE_ID = str(uuid.uuid4())


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
            (FAKE_ID, 404),
            (None, 404),
        ),
    )
    async def test_wrong_id_returns_error(
        self, app: FastAPI, client: AsyncClient, id: str, status_code: int
    ) -> None:
        res = await client.get(app.url_path_for("jobs:get-job-by-id", id=id))

        assert res.status_code == status_code

    async def test_get_all_jobs_returns_valid_response(
        self, app: FastAPI, client: AsyncClient, test_job: JobInDB
    ) -> None:
        res = await client.get(app.url_path_for("jobs:get-all-jobs"))
        print(res.json())
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        jobs = [JobInDB(**l) for l in res.json()]
        assert test_job in jobs


class TestUpdateJob:
    @pytest.mark.parametrize(
        "attrs_to_change, values",
        (
            (["name"], ["new fake job name"]),
            (["description"], ["new fake job description"]),
            (["price"], [3.14]),
            (["job_type"], ["full_clean"]),
            (
                ["name", "description"],
                [
                    "extra new fake job name",
                    "extra new fake job description",
                ],
            ),
            (["price", "job_type"], [42.00, "dust_up"]),
        ),
    )
    async def test_update_job_with_valid_input(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_job: JobInDB,
        attrs_to_change: List[str],
        values: List[str],
    ) -> None:
        job_update = {
            attrs_to_change[i]: values[i] for i in range(len(attrs_to_change))
        }
        res = await client.put(
            app.url_path_for(
                "jobs:update-job-by-id",
                id=test_job.id,
            ),
            json=job_update
        )
        print(res.json())
        assert res.status_code == HTTP_200_OK
        updated_job = JobInDB(**res.json())
        assert updated_job.id == test_job.id  # make sure it's the same job
        # make sure that any attribute we updated has changed to the correct value
        for i in range(len(attrs_to_change)):
            attr_to_change = getattr(updated_job, attrs_to_change[i])
            assert attr_to_change != getattr(test_job, attrs_to_change[i])
            assert attr_to_change == values[i]
        # make sure that no other attributes' values have changed
        for attr, value in updated_job.dict().items():
            if attr not in attrs_to_change:
                assert getattr(test_job, attr) == value

    @pytest.mark.parametrize(
        "id, payload, status_code",
        (
            (FAKE_ID, {"name": "test"}, 404),
            (None, None, 422),
            (None, {"job_type": "invalid job type"}, 422),
            (None, {"job_type": None}, 400),
        ),
    )
    async def test_update_job_with_invalid_input_throws_error(
        self,
        app: FastAPI,
        client: AsyncClient,
        id: str,
        payload: dict,
        status_code: int,
        test_job: JobInDB
    ) -> None:
        # job_update = {payload}
        res = await client.put(
            app.url_path_for("jobs:update-job-by-id",
                             id=id if id is not None else test_job.id),
            json=payload
        )
        assert res.status_code == status_code


class TestDeleteJob:
    async def test_can_delete_job_successfully(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_job: JobInDB,
    ) -> None:
        # delete the job
        res = await client.delete(
            app.url_path_for(
                "jobs:delete-job-by-id",
                id=test_job.id,
            ),
        )
        assert res.status_code == HTTP_200_OK
        # ensure that the job no longer exists
        res = await client.get(
            app.url_path_for(
                "jobs:get-job-by-id",
                id=test_job.id,
            ),
        )
        assert res.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        "id, status_code",
        (
            (FAKE_ID, 404),
            (None, 404),
        ),
    )
    async def test_delete_job_with_invalid_input_throws_error(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_job: JobInDB,
        id: str,
        status_code: int,
    ) -> None:
        res = await client.delete(
            app.url_path_for("jobs:delete-job-by-id", id=id),
        )
        print(res.json())
        assert res.status_code == status_code
