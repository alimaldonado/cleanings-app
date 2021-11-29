from typing import List, Callable
import pytest
from httpx import AsyncClient
from fastapi import FastAPI, status
from databases import Database

from app.models.cleaning import CleaningCreate, CleaningInDB
from app.models.user import UserInDB
from app.models.offer import OfferCreate, OfferUpdate, OfferInDB, OfferPublic

pytestmark = pytest.mark.asyncio


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
        
