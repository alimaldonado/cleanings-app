from typing import List
import json

import pytest

from httpx import AsyncClient
from fastapi import FastAPI, status

from app.models.cleaning import CleaningInDB

pytestmark = pytest.mark.asyncio


class TestFeedRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        response = await client.get(
            app.url_path_for("feed:get-cleaning-feed-for-user")
        )
        assert response.status_code != status.HTTP_404_NOT_FOUND


class TestCleaningFeed:
    async def test_cleaning_feed_returns_valid_response(
        self,
        *,
        app: FastAPI,
        elliots_authorized_client: AsyncClient,
        test_list_of_new_and_updated_cleanings: List[CleaningInDB]
    ) -> None:
        cleaning_ids = [
            cleaning.id for cleaning in test_list_of_new_and_updated_cleanings]

        response = await elliots_authorized_client.get(
            app.url_path_for("feed:get-cleaning-feed-for-user")
        )

        assert response.status_code == status.HTTP_200_OK

        cleaning_feed = response.json()

        assert isinstance(cleaning_feed, list)
        assert len(cleaning_feed) == 20
        assert set(feed_item["id"] for feed_item in cleaning_feed).issubset(
            set(cleaning_ids))

    async def test_cleaning_feed_response_is_ordered_correctly(
        self,
        *,
        app: FastAPI,
        elliots_authorized_client: AsyncClient,
        test_list_of_new_and_updated_cleanings: List[CleaningInDB],
    ) -> None:
        response = await elliots_authorized_client.get(
            app.url_path_for("feed:get-cleaning-feed-for-user")
        )


        assert response.status_code == status.HTTP_200_OK

        cleaning_feed = response.json()

        # TODO: feed is not ordering by event type
        for feed_item in cleaning_feed[:13]:
            assert feed_item["event_type"] == "is_update"

        for feed_item in cleaning_feed[13:]:
            assert feed_item["event_type"] == "is_create"
