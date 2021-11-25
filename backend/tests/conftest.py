import warnings
import os
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database
import alembic
from alembic.config import Config

from app.models.job import JobCreate, JobInDB
from app.models.user import UserCreate, UserInDB
from app.db.repositories.users import UsersRepository
from app.db.repositories.jobs import JobsRepository


# Apply migrations at beginning and end of testing session


@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")
# Create a new application for testing


@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.api.server import get_application
    return get_application()
# Grab a reference to our database when needed


@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db
# Make requests in our tests


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"}
        ) as client:
            yield client


@pytest.fixture
async def test_job(db: Database) -> JobInDB:
    job_repo = JobsRepository(db)
    new_job = JobCreate(
        name="fake job name",
        description="fake job description",
        price=9.99,
        job_type="spot_clean",
    )
    return await job_repo.create_job(new_job=new_job)


@pytest.fixture
async def test_user(db: Database) -> UserInDB:
    new_user = UserCreate(
        email="eddie@vedder.io",
        username="eddiev",
        password="evenflow"
    )

    user_repo = UsersRepository(db)

    existing_user = await user_repo.get_user_by_email(email=new_user.email)

    if existing_user:
        return existing_user

    return await user_repo.register_new_user(new_user=new_user)
