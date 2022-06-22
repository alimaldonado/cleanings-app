from typing import List
from urllib import response
from pkg_resources import resource_isdir

import pytest

from httpx import AsyncClient
from fastapi import FastAPI, status

from app.models.cleaning import CleaningInDB
from tests.conftest import test_list_of_cleanings_with_evaluated_offer

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
    
    async def test_cleaning_fed_response_is_ordered_correctly(
        self,
        *,
        app: FastAPI,
        elliots_authorized_client: AsyncClient,
        test_list_of_new_and_updated_cleanings: List[CleaningInDB]
    ) -> None:
        response = await elliots_authorized_client.get(app.url_path_for("feed:get-cleaning-feed-for-user"))

        assert response.status_code == status.HTTP_200_OK
        cleaning_feed = response.json()

        for feed_item in cleaning_feed[:13]:
            assert feed_item["event_type"] == "is_update"
        for feed_item in cleaning_feed[13:]:
            assert feed_item["event_type"] == "is_create"


    async def test_cleaning_feed_can_paginate_correctly(
        self,
        *, 
        app: FastAPI,
        elliots_authorized_client: AsyncClient,
        test_list_of_new_and_updated_cleanings: List[CleaningInDB],
    ) -> None:

        res_page_1 =  await elliots_authorized_client.get(app.url_path_for("feed:get-cleaning-feed-for-user"))
        assert res_page_1.status_code ==  status.HTTP_200_OK
        cleaning_feed_page_1 = res_page_1.json()
        assert len(cleaning_feed_page_1) == 20
        ids_page_1 = set(feed_item["id"] for feed_item in cleaning_feed_page_1)

        new_starting_date = cleaning_feed_page_1[-1]["event_timestamp"]

        res_page_2 =  await elliots_authorized_client.get(
            app.url_path_for("feed:get-cleaning-feed-for-user"),
            params={ "starting_date": new_starting_date, "page_chunk_size": 20 }
        )
        assert res_page_2.status_code ==  status.HTTP_200_OK
        cleaning_feed_page_2 = res_page_2.json()
        assert len(cleaning_feed_page_2) == 20
        ids_page_2 = set(feed_item["id"] for feed_item in cleaning_feed_page_2)

        assert ids_page_1 != ids_page_2

 

