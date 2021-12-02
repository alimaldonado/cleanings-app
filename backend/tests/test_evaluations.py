from typing import Callable
import pytest
import uuid
from httpx import AsyncClient
from fastapi import FastAPI, status
from app.models.cleaning import CleaningInDB
from app.models.evaluation import EvaluationCreate, EvaluationInDB

from app.models.user import UserInDB

pytestmark = pytest.mark.asyncio

FAKE_ID = str(uuid.uuid4())


class TestEvaluationRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        response = await client.post(app.url_path_for("evaluations:create-evaluation-for-cleaner", cleaning_id=FAKE_ID, username="braddpit"))
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.get(app.url_path_for("evaluations:get-evaluation-for-cleaner", cleaning_id=FAKE_ID,  username="braddpit"))
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.get(app.url_path_for("evaluations:list-evaluations-for-cleaner", username="bradpitt"))
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.get(app.url_path_for("evaluations:get-stats-for-cleaner", username="bradpitt"))
        assert response.status_code != status.HTTP_404_NOT_FOUND


class TestCreateEvaluations:
    async def test_owner_can_leave_evaluation_for_cleaner_and_mark_offer_completed(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        user_darlene: UserInDB,
        user_mr_robot: UserInDB,
        test_cleaning_with_accepted_offer: CleaningInDB,
    ) -> None:
        evaluation_create = EvaluationCreate(
            no_show=False,
            headline="Excellent Job",
            comment=f"""
Really appreciated the hard work and effort they put into this job!
Though the cleaner took their time, I would definitely hire them again for the quality of their work.
            """,
            professionalism=5,
            completeness=5,
            efficiency=4,
            overall_rating=5
        )

        authorized_client = create_authorized_client(user=user_darlene)

        response = await authorized_client.post(
            app.url_path_for(
                "evaluations:create-evaluation-for-cleaner",
                cleaning_id=test_cleaning_with_accepted_offer.id,
                username=user_mr_robot.username
            ),
            json=evaluation_create.dict()
        )
        

        assert response.status_code == status.HTTP_201_CREATED

        evaluation = EvaluationInDB(**response.json())

        assert evaluation.no_show == evaluation_create.no_show
        assert evaluation.headline == evaluation_create.headline
        assert evaluation.overall_rating == evaluation_create.overall_rating

        response = await authorized_client.get(
            app.url_path_for(
                "offers:get-offer-from-user",
                cleaning_id=test_cleaning_with_accepted_offer.id,
                username=user_mr_robot.username
            ),
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "completed"

    async def test_non_owner_cant_leave_evaluation_for(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        user_mr_robot: UserInDB,
        user_tyrell: UserInDB,
        test_cleaning_with_accepted_offer: CleaningInDB,
    ) -> None:

        authorized_client = create_authorized_client(user=user_tyrell)

        response = await authorized_client.post(
            app.url_path_for(
                "evaluations:create-evaluation-for-cleaner",
                cleaning_id=test_cleaning_with_accepted_offer.id,
                username=user_mr_robot.username
            ),
            json={"overall_rating": 2}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_owner_cant_leave_evaluation_for_wrong_user(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        user_darlene: UserInDB,
        user_tyrell: UserInDB,
        test_cleaning_with_accepted_offer: CleaningInDB,
    ) -> None:

        authorized_client = create_authorized_client(user=user_darlene)

        response = await authorized_client.post(
            app.url_path_for(
                "evaluations:create-evaluation-for-cleaner",
                cleaning_id=test_cleaning_with_accepted_offer.id,
                username=user_tyrell.username
            ),
            json={"overall_rating": 2}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_owner_cant_leave_multiple_evaluation(
        self,
        app: FastAPI,
        create_authorized_client: Callable,
        user_darlene: UserInDB,
        user_mr_robot: UserInDB,

        test_cleaning_with_accepted_offer: CleaningInDB,
    ) -> None:

        authorized_client = create_authorized_client(user=user_darlene)

        response = await authorized_client.post(
            app.url_path_for(
                "evaluations:create-evaluation-for-cleaner",
                cleaning_id=test_cleaning_with_accepted_offer.id,
                username=user_mr_robot.username
            ),
            json={"overall_rating": 2}
        )

        assert response.status_code == status.HTTP_201_CREATED


        response = await authorized_client.post(
            app.url_path_for(
                "evaluations:create-evaluation-for-cleaner",
                cleaning_id=test_cleaning_with_accepted_offer.id,
                username=user_mr_robot.username
            ),
            json={"overall_rating": 1}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
