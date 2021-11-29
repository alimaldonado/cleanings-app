
from typing import List, Dict, Union, Optional
import pytest
import uuid
from httpx import AsyncClient
from fastapi import FastAPI, status
from databases import Database
from sqlalchemy.sql.visitors import traverse
from app.db.repositories.jobs import JobsRepository
from app.models.job import JobCreate, JobInDB, JobPublic
from app.models.user import UserInDB

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


@pytest.fixture
async def test_jobs_list(db: Database, test_user2: UserInDB) -> List[JobInDB]:
    job_repo = JobsRepository(db)

    return [
        await job_repo.create_job(
            new_job=JobCreate(
                name=f"test job {i}", description="test description", price=20.00, job_type="full_clean"
            ),
            requesting_user=test_user2
        )
        for i in range(5)
    ]


class TestJobsRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient, test_job: JobInDB) -> None:
        response = await client.post(app.url_path_for("jobs:create-job"), json={})
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.get(app.url_path_for("jobs:get-job-by-id", id=test_job.id))
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.get(app.url_path_for("jobs:list-all-user-jobs"))
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.put(app.url_path_for("jobs:update-job-by-id", id=test_job.id))
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.delete(app.url_path_for("jobs:delete-job-by-id", id=test_job.id))
        assert response.status_code != status.HTTP_404_NOT_FOUND


class TestCreateJob:
    async def test_valid_input_creates_job(
        self, app: FastAPI, authorized_client: AsyncClient, new_job: JobCreate, test_user: UserInDB
    ) -> None:
        response = await authorized_client.post(
            app.url_path_for("jobs:create-job"), json=new_job.dict()
        )

        print(response.json())

        assert response.status_code == status.HTTP_201_CREATED

        created_job = JobPublic(**response.json())

        assert created_job.name == new_job.name
        assert created_job.price == new_job.price
        assert created_job.job_type == new_job.job_type
        assert created_job.owner == test_user.id

    async def test_unauthorized_user_unable_to_create_job(
        self, app: FastAPI, client: AsyncClient, new_job: JobCreate
    ) -> None:
        response = await client.post(
            app.url_path_for("jobs:create-job"),
            json=new_job.dict()
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "invalid_payload, status_code",
        (
            (None, 422),
            ({}, 422),
            ({"name": "test"}, 422),
            ({"price": 10.00}, 422),
            ({"name": "test", "description": "test"}, 422),

        )
    )
    async def test_invalid_input_raises_error(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        invalid_payload: Dict[str, Union[str, float]],
        test_job: JobCreate,
        status_code: int
    ) -> None:
        response = await authorized_client.post(
            app.url_path_for("jobs:create-job"),
            json=invalid_payload
        )

        assert response.status_code == status_code


class TestGetJob:
    async def test_get_job_by_id(
        self, app: FastAPI, authorized_client: AsyncClient, test_job: JobInDB
    ) -> None:

        response = await authorized_client.get(app.url_path_for("jobs:get-job-by-id", id=test_job.id))
        assert response.status_code == status.HTTP_200_OK
        job = JobInDB(**response.json())
        
        assert job == test_job

    async def test_unauthorized_users_cant_access_jobs(
        self, app: FastAPI, client: AsyncClient, test_job: JobInDB
    ) -> None:
        response = await client.get(
            app.url_path_for("jobs:get-job-by-id", id=test_job.id)
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "id, status_code",
        (
            (FAKE_ID, 404),
            (None, 404),
        ),
    )
    async def test_wrong_id_returns_error(
        self, app: FastAPI, authorized_client: AsyncClient, id: str, status_code: int
    ) -> None:
        response = await authorized_client.get(app.url_path_for("jobs:get-job-by-id", id=id))

        assert response.status_code == status_code

    # async def test_get_all_jobs_returns_valid_response(
    #     self, app: FastAPI, client: AsyncClient, test_job: JobInDB
    # ) -> None:
    #     res = await client.get(app.url_path_for("jobs:get-all-jobs"))
    #     print(res.json())
    #     assert res.status_code == status.HTTP_200_OK
    #     assert isinstance(res.json(), list)
    #     assert len(res.json()) > 0
    #     jobs = [JobInDB(**l) for l in res.json()]
    #     assert test_job in jobs

    async def test_get_all_jobs_returns_only_user_owned_jobs(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_user: UserInDB,
        db: Database,
        test_job: JobInDB,
        test_jobs_list: List[JobInDB]
    ) -> None:
        response = await authorized_client.get(
            app.url_path_for("jobs:list-all-user-jobs")
        )
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0

        jobs = [JobInDB(**l) for l in response.json()]

        assert test_job in jobs

        for job in jobs:
            assert job.owner == test_user.id

        assert all(c not in jobs for c in test_jobs_list)


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
        authorized_client: AsyncClient,
        test_job: JobInDB,
        attrs_to_change: List[str],
        values: List[str],
    ) -> None:
        job_update = {
            attrs_to_change[i]: values[i] for i in range(len(attrs_to_change))
        }
        res = await authorized_client.put(
            app.url_path_for(
                "jobs:update-job-by-id",
                id=test_job.id,
            ),
            json=job_update
        )

        assert res.status_code == status.HTTP_200_OK
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

    async def test_user_receives_error_if_updating_other_users_jobs(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_jobs_list: List[JobInDB],
    ) -> None:

        response = await authorized_client.put(
            app.url_path_for(
                "jobs:update-job-by-id",
                id=test_jobs_list[0].id,
            ),
            json={"price": 99.99}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_user_cant_change_ownership_of_job(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_job: JobInDB,
        test_user: UserInDB,
        test_user2: UserInDB
    ) -> None:

        response = await authorized_client.put(
            app.url_path_for(
                "jobs:update-job-by-id",
                id=test_job.id,
            ),
            json={"owner": test_user2.id}
        )

        assert response.status_code == status.HTTP_200_OK

        job = JobPublic(**response.json())

        assert job.owner == test_user.id

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
        authorized_client: AsyncClient,
        id: str,
        payload: dict,
        status_code: int,
        test_job: JobInDB
    ) -> None:
        # job_update = {payload}
        res = await authorized_client.put(
            app.url_path_for("jobs:update-job-by-id",
                             id=id if id is not None else test_job.id),
            json=payload
        )
        assert res.status_code == status_code


class TestDeleteJob:
    async def test_can_delete_job_successfully(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_job: JobInDB,
    ) -> None:
        # delete the job
        response = await authorized_client.delete(
            app.url_path_for(
                "jobs:delete-job-by-id",
                id=test_job.id,
            ),
        )
        print(response.json())
        assert response.status_code == status.HTTP_200_OK
        # ensure that the job no longer exists
        response = await authorized_client.get(
            app.url_path_for(
                "jobs:get-job-by-id",
                id=test_job.id,
            ),
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_user_cant_delete_other_users_job(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_jobs_list: List[JobInDB],
    ) -> None:
        # delete the job
        response = await authorized_client.delete(
            app.url_path_for(
                "jobs:delete-job-by-id",
                id=test_jobs_list[0].id,
            ),
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize(
        "id, status_code",
        (
            (FAKE_ID, 404),
            (None, 404),
        ),
    )
    async def test_wrong_id_throws_error(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_job: JobInDB,
        id: str,
        status_code: int,
    ) -> None:
        res = await authorized_client.delete(
            app.url_path_for("jobs:delete-job-by-id", id=id),
        )
        print(res.json())
        assert res.status_code == status_code
