from typing import List, Callable
import pytest
import uuid
from httpx import AsyncClient
from fastapi import FastAPI, status
from databases import Database

from app.models.cleaning import CleaningCreate, CleaningInDB
from app.models.user import UserInDB
from app.models.offer import OfferCreate, OfferUpdate, OfferInDB, OfferPublic

pytestmark = pytest.mark.asyncio

FAKE_ID = str(uuid.uuid4())


class TestOffersRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        response = await client.post(app.url_path_for("offers:create-offer", cleaning_id=1))
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.get(app.url_path_for("offers:list-offers-for-cleaning", cleaning_id=1))
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.get(app.url_path_for("offers:get-offer-from-user", cleaning_id=1, username="bradpitt"))
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.put(app.url_path_for("offers:accept-offer-from-user", cleaning_id=1, username="braddpit"))
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.put(app.url_path_for("offers:cancel-offer-from-user", cleaning_id=1))
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.delete(app.url_path_for("offers:rescind-offer-from-user", cleaning_id=1))
        assert response.status_code != status.HTTP_404_NOT_FOUND


class TestCreateOffers:
    async def test_user_can_successfully_create_offer_for_other_users_cleaning_job(
        self, app: FastAPI, create_authorized_client: Callable, test_cleaning: CleaningInDB, user_mr_robot: UserInDB,
    ) -> None:
        elliots_authorized_client = create_authorized_client(user=user_mr_robot)

        response = await elliots_authorized_client.post(
            app.url_path_for("offers:create-offer",
                             cleaning_id=test_cleaning.id)
        )
        print(response.json())
        assert response.status_code == status.HTTP_201_CREATED

        offer = OfferPublic(**response.json())
        assert offer.user_id == user_mr_robot.id
        assert offer.cleaning_id == test_cleaning.id
        assert offer.status == "pending"

    async def test_user_cant_create_duplicate_offers(
        self, app: FastAPI, create_authorized_client: Callable, test_cleaning: CleaningInDB, user_tyrell: UserInDB,
    ) -> None:
        elliots_authorized_client = create_authorized_client(user=user_tyrell)

        response = await elliots_authorized_client.post(
            app.url_path_for("offers:create-offer",
                             cleaning_id=test_cleaning.id)
        )
        assert response.status_code == status.HTTP_201_CREATED

        response = await elliots_authorized_client.post(
            app.url_path_for("offers:create-offer",
                             cleaning_id=test_cleaning.id)
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_user_unable_to_create_offer_for_their_own_cleaning_job(
        self, app: FastAPI, elliots_authorized_client: AsyncClient, user_elliot: UserInDB, test_cleaning: CleaningInDB
    ) -> None:
        response = await elliots_authorized_client.post(
            app.url_path_for("offers:create-offer",
                             cleaning_id=test_cleaning.id)
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_unauthenticated_users_cant_create_offers(
        self, app: FastAPI, client: AsyncClient, test_cleaning: CleaningInDB,
    ) -> None:
        response = await client.post(
            app.url_path_for("offers:create-offer",
                             cleaning_id=test_cleaning.id)
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "id, status_code",
        (
            (FAKE_ID, 404),
            (None, 404)
        ),
    )
    async def test_wrong_id_gives_proper_error_status(
        self, app: FastAPI, create_authorized_client: Callable, user_angela: UserInDB, id: str, status_code: int
    ) -> None:
        elliots_authorized_client = create_authorized_client(user=user_angela)

        response = await elliots_authorized_client.post(
            app.url_path_for("offers:create-offer", cleaning_id=id)
        )

        assert response.status_code == status_code
