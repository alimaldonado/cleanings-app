
from typing import List, Dict, Union, Optional
import pytest
import uuid
from httpx import AsyncClient
from fastapi import FastAPI, status
from databases import Database
from sqlalchemy.sql.visitors import traverse
from app.db.repositories.cleanings import cleaningsRepository
from app.models.cleaning import CleaningCreate, CleaningInDB, CleaningPublic
from app.models.user import UserInDB

pytestmark = pytest.mark.asyncio

FAKE_ID = str(uuid.uuid4())


@pytest.fixture
def new_cleaning():
    return CleaningCreate(
        name="test cleaning",
        description="test description",
        price=0.00,
        cleaning_type="spot_clean",
    )


@pytest.fixture
async def test_cleanings_list(db: Database, test_user2: UserInDB) -> List[CleaningInDB]:
    cleaning_repo = cleaningsRepository(db)

    return [
        await cleaning_repo.create_cleaning(
            new_cleaning=CleaningCreate(
                name=f"test cleaning {i}", description="test description", price=20.00, cleaning_type="full_clean"
            ),
            requesting_user=test_user2
        )
        for i in range(5)
    ]


class TestcleaningsRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient, test_cleaning: CleaningInDB) -> None:
        response = await client.post(app.url_path_for("cleanings:create-cleaning"), json={})
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.get(app.url_path_for("cleanings:get-cleaning-by-id", id=test_cleaning.id))
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.get(app.url_path_for("cleanings:list-all-user-cleanings"))
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.put(app.url_path_for("cleanings:update-cleaning-by-id", id=test_cleaning.id))
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.delete(app.url_path_for("cleanings:delete-cleaning-by-id", id=test_cleaning.id))
        assert response.status_code != status.HTTP_404_NOT_FOUND


class TestCreatecleaning:
    async def test_valid_input_creates_cleaning(
        self, app: FastAPI, authorized_client: AsyncClient, new_cleaning: CleaningCreate, test_user: UserInDB
    ) -> None:
        response = await authorized_client.post(
            app.url_path_for("cleanings:create-cleaning"), json=new_cleaning.dict()
        )

        print(response.json())

        assert response.status_code == status.HTTP_201_CREATED

        created_cleaning = CleaningPublic(**response.json())

        assert created_cleaning.name == new_cleaning.name
        assert created_cleaning.price == new_cleaning.price
        assert created_cleaning.cleaning_type == new_cleaning.cleaning_type
        assert created_cleaning.owner == test_user.id

    async def test_unauthorized_user_unable_to_create_cleaning(
        self, app: FastAPI, client: AsyncClient, new_cleaning: CleaningCreate
    ) -> None:
        response = await client.post(
            app.url_path_for("cleanings:create-cleaning"),
            json=new_cleaning.dict()
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
        test_cleaning: CleaningCreate,
        status_code: int
    ) -> None:
        response = await authorized_client.post(
            app.url_path_for("cleanings:create-cleaning"),
            json=invalid_payload
        )

        assert response.status_code == status_code


class TestGetcleaning:
    async def test_get_cleaning_by_id(
        self, app: FastAPI, authorized_client: AsyncClient, test_cleaning: CleaningInDB
    ) -> None:

        response = await authorized_client.get(app.url_path_for("cleanings:get-cleaning-by-id", id=test_cleaning.id))
        assert response.status_code == status.HTTP_200_OK
        cleaning = CleaningInDB(**response.json())
        
        assert cleaning == test_cleaning

    async def test_unauthorized_users_cant_access_cleanings(
        self, app: FastAPI, client: AsyncClient, test_cleaning: CleaningInDB
    ) -> None:
        response = await client.get(
            app.url_path_for("cleanings:get-cleaning-by-id", id=test_cleaning.id)
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
        response = await authorized_client.get(app.url_path_for("cleanings:get-cleaning-by-id", id=id))

        assert response.status_code == status_code

    # async def test_get_all_cleanings_returns_valid_response(
    #     self, app: FastAPI, client: AsyncClient, test_cleaning: CleaningInDB
    # ) -> None:
    #     res = await client.get(app.url_path_for("cleanings:get-all-cleanings"))
    #     print(res.json())
    #     assert res.status_code == status.HTTP_200_OK
    #     assert isinstance(res.json(), list)
    #     assert len(res.json()) > 0
    #     cleanings = [CleaningInDB(**l) for l in res.json()]
    #     assert test_cleaning in cleanings

    async def test_get_all_cleanings_returns_only_user_owned_cleanings(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_user: UserInDB,
        db: Database,
        test_cleaning: CleaningInDB,
        test_cleanings_list: List[CleaningInDB]
    ) -> None:
        response = await authorized_client.get(
            app.url_path_for("cleanings:list-all-user-cleanings")
        )
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0

        cleanings = [CleaningInDB(**l) for l in response.json()]

        assert test_cleaning in cleanings

        for cleaning in cleanings:
            assert cleaning.owner == test_user.id

        assert all(c not in cleanings for c in test_cleanings_list)


class TestUpdatecleaning:
    @pytest.mark.parametrize(
        "attrs_to_change, values",
        (
            (["name"], ["new fake cleaning name"]),
            (["description"], ["new fake cleaning description"]),
            (["price"], [3.14]),
            (["cleaning_type"], ["full_clean"]),
            (
                ["name", "description"],
                [
                    "extra new fake cleaning name",
                    "extra new fake cleaning description",
                ],
            ),
            (["price", "cleaning_type"], [42.00, "dust_up"]),
        ),
    )
    async def test_update_cleaning_with_valid_input(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_cleaning: CleaningInDB,
        attrs_to_change: List[str],
        values: List[str],
    ) -> None:
        cleaning_update = {
            attrs_to_change[i]: values[i] for i in range(len(attrs_to_change))
        }
        res = await authorized_client.put(
            app.url_path_for(
                "cleanings:update-cleaning-by-id",
                id=test_cleaning.id,
            ),
            json=cleaning_update
        )

        assert res.status_code == status.HTTP_200_OK
        updated_cleaning = CleaningInDB(**res.json())
        assert updated_cleaning.id == test_cleaning.id  # make sure it's the same cleaning
        # make sure that any attribute we updated has changed to the correct value
        for i in range(len(attrs_to_change)):
            attr_to_change = getattr(updated_cleaning, attrs_to_change[i])
            assert attr_to_change != getattr(test_cleaning, attrs_to_change[i])
            assert attr_to_change == values[i]
        # make sure that no other attributes' values have changed
        for attr, value in updated_cleaning.dict().items():
            if attr not in attrs_to_change:
                assert getattr(test_cleaning, attr) == value

    async def test_user_receives_error_if_updating_other_users_cleanings(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_cleanings_list: List[CleaningInDB],
    ) -> None:

        response = await authorized_client.put(
            app.url_path_for(
                "cleanings:update-cleaning-by-id",
                id=test_cleanings_list[0].id,
            ),
            json={"price": 99.99}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_user_cant_change_ownership_of_cleaning(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_cleaning: CleaningInDB,
        test_user: UserInDB,
        test_user2: UserInDB
    ) -> None:

        response = await authorized_client.put(
            app.url_path_for(
                "cleanings:update-cleaning-by-id",
                id=test_cleaning.id,
            ),
            json={"owner": test_user2.id}
        )

        assert response.status_code == status.HTTP_200_OK

        cleaning = CleaningPublic(**response.json())

        assert cleaning.owner == test_user.id

    @pytest.mark.parametrize(
        "id, payload, status_code",
        (
            (FAKE_ID, {"name": "test"}, 404),
            (None, None, 422),
            (None, {"cleaning_type": "invalid cleaning type"}, 422),
            (None, {"cleaning_type": None}, 400),
        ),
    )
    async def test_update_cleaning_with_invalid_input_throws_error(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        id: str,
        payload: dict,
        status_code: int,
        test_cleaning: CleaningInDB
    ) -> None:
        # cleaning_update = {payload}
        res = await authorized_client.put(
            app.url_path_for("cleanings:update-cleaning-by-id",
                             id=id if id is not None else test_cleaning.id),
            json=payload
        )
        assert res.status_code == status_code


class TestDeletecleaning:
    async def test_can_delete_cleaning_successfully(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_cleaning: CleaningInDB,
    ) -> None:
        # delete the cleaning
        response = await authorized_client.delete(
            app.url_path_for(
                "cleanings:delete-cleaning-by-id",
                id=test_cleaning.id,
            ),
        )
        print(response.json())
        assert response.status_code == status.HTTP_200_OK
        # ensure that the cleaning no longer exists
        response = await authorized_client.get(
            app.url_path_for(
                "cleanings:get-cleaning-by-id",
                id=test_cleaning.id,
            ),
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_user_cant_delete_other_users_cleaning(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_cleanings_list: List[CleaningInDB],
    ) -> None:
        # delete the cleaning
        response = await authorized_client.delete(
            app.url_path_for(
                "cleanings:delete-cleaning-by-id",
                id=test_cleanings_list[0].id,
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
        test_cleaning: CleaningInDB,
        id: str,
        status_code: int,
    ) -> None:
        res = await authorized_client.delete(
            app.url_path_for("cleanings:delete-cleaning-by-id", id=id),
        )
        print(res.json())
        assert res.status_code == status_code
