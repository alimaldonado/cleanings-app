from pydantic import EmailStr
from fastapi import HTTPException, status
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.repositories.base import BaseRepository
from app.models.user import UserCreate, UserUpdate, UserInDB

GET_USER_BY_EMAIL_QUERY = """
    SELECT id, username, email, email_verified, password, salt, is_active, is_superuser, created_at, updated_at
    FROM users
    WHERE email = :email;
"""
GET_USER_BY_USERNAME_QUERY = """
    SELECT id, username, email, email_verified, password, salt, is_active, is_superuser, created_at, updated_at
    FROM users
    WHERE username = :username;
"""
REGISTER_NEW_USER_QUERY = """
    INSERT INTO users (username, email, password, salt)
    VALUES (:username, :email, :password, :salt)
    RETURNING id, username, email, email_verified, password, salt, is_active, is_superuser, created_at, updated_at;
"""


class UsersRepository(BaseRepository):
    async def get_user_by_email(self, *, email: EmailStr) -> UserInDB:
        user_record = await self.db.fetch_one(query=GET_USER_BY_EMAIL_QUERY, values={"email": email})

        if not user_record:
            return None

        return UserInDB(**user_record)

    async def get_user_by_username(self, *, username: str) -> UserInDB:
        user_record = await self.db.fetch_one(query=GET_USER_BY_USERNAME_QUERY, values={"username": username})

        if not user_record:
            return None

        return UserInDB(**user_record)

    async def register_new_user(self, *, new_user: UserCreate) -> UserInDB:
        if await self.get_user_by_email(email=new_user.email) is not None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="That email is already taken. Please try another one."
            )

        if await self.get_user_by_username(username=new_user.username) is not None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="That username is already taken. Please try another one."
            )

        # TODO: Encrypt password
        created_user = await self.db.fetch_one(query=REGISTER_NEW_USER_QUERY, values={**new_user.dict(), "salt": "123"})

        return UserInDB(**created_user)
