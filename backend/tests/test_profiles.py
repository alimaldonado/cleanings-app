import pytest

from databases import Database

from fastapi import FastAPI, status
from httpx import AsyncClient
from starlette.status import HTTP_200_OK

from app.models.user import UserInDB, UserPublic
from app.models.profile import ProfileInDB, ProfilePublic
from app.db.repositories.profiles import ProfilesRepository

pytestmark = pytest.mark.asyncio


class TestProfileRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient, test_user: UserInDB) -> None:
        response = await client.get(app.url_path_for("profiles:get-profile-by-username", username=test_user.username))
        assert response.status_code != status.HTTP_404_NOT_FOUND

        response = await client.put(app.url_path_for("profiles:update-own-profile"), json={})
        assert response.status_code != status.HTTP_404_NOT_FOUND


class TestProfileCreate:
    async def test_profile_created_for_new_users(self, app: FastAPI, client: AsyncClient, db: Database) -> None:
        profiles_repo = ProfilesRepository(db)

        new_user = {"email": "dwayne@johnson.io",
                    "username": "therock", "password": "dwaynetherockjohnson"}
        response = await client.post(app.url_path_for("users:register-new-user"), json=new_user)
        assert response.status_code == status.HTTP_201_CREATED

        created_user = UserPublic(**response.json())
        user_profile = await profiles_repo.get_profile_by_user_id(user_id=created_user.id)
        assert user_profile is not None
        assert isinstance(user_profile, ProfileInDB)


class TestProfileView:
    async def test_authenticated_user_can_view_other_users_profile(
        self, app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB, test_user2: UserInDB
    ) -> None:
        response = await authorized_client.get(
            app.url_path_for("profiles:get-profile-by-username",
                             username=test_user2.username)
        )
        assert response.status_code == HTTP_200_OK
        profile = ProfilePublic(**response.json())
        assert profile.username == test_user2.username

    async def test_unregistered_users_cannot_access_other_users_profile(
        self, app: FastAPI, client: AsyncClient, test_user2: UserInDB
    ) -> None:
        response = await client.get(
            app.url_path_for("profiles:get-profile-by-username",
                             username=test_user2.username)
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_no_profile_is_returned_when_username_matches_no_user(
        self, app: FastAPI, authorized_client: AsyncClient
    ) -> None:
        response = await authorized_client.get(
            app.url_path_for("profiles:get-profile-by-username",
                             username="username_doesnt_match")
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestProfileManagement:
    @pytest.mark.parametrize(
        "attr,value",
        (
            ("full_name", "Lebron James"),
            ("phone_number", "555-333-1000"),
            ("bio", "This is a test bio"),
            ("image", "http://testimages.com/testimage"),
        )
    )
    async def test_user_can_update_own_profile(
        self, app: FastAPI, authorized_client: AsyncClient, test_user: UserInDB, attr: str, value: str
    ) -> None:
        assert getattr(test_user.profile, attr) != value

        response = await authorized_client.put(
            app.url_path_for("profiles:update-own-profile"),
            json={attr: value},
        )

        assert response.status_code == status.HTTP_200_OK

        profile = ProfilePublic(**response.json())

        assert getattr(profile, attr) == value

    @pytest.mark.parametrize(
        "attr, value, status_code",
        (
            ("full_name", [], 422),
            ("bio", {}, 422),
            ("image", "./image-string.png", 422),
            ("image", 5, 422),
        ),
    )
    async def test_user_receives_error_for_invalid_update_params(
        self,
        app: FastAPI,
        authorized_client: AsyncClient,
        test_user: UserInDB,
        attr: str,
        value: str,
        status_code: int,
    ) -> None:
        response = await authorized_client.put(
            app.url_path_for("profiles:update-own-profile"),
            json={attr: value}
        )

        assert response.status_code == status_code
