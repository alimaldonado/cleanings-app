from fastapi import APIRouter, Path, Body
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from starlette import status

from app.models.profile import ProfileUpdate, ProfilePublic
from app.models.user import UserInDB
from app.api.dependencies.auth import get_current_active_user
from app.db.repositories.profiles import ProfilesRepository
from app.api.dependencies.database import get_repository


router = APIRouter()


@router.get("/{username}", response_model=ProfilePublic, name="profiles:get-profile-by-username")
async def get_profile_by_username(
    *,
    username: str = Path(..., min_length=3, regex="^[a-zA-Z0-9_-]+$"),
    current_user: UserInDB = Depends(get_current_active_user),
    profiles_repo: ProfilesRepository = Depends(
        get_repository(ProfilesRepository)),
) -> ProfilePublic:
    profile = await profiles_repo.get_profile_by_username(username=username)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No profile found with  username '{username}'."
        )

    return profile


@router.put("/me/", response_model=ProfilePublic, name="profiles:update-own-profile")
async def update_own_profile(
    profile_update: ProfileUpdate = Body(..., embed=False),
    current_user: UserInDB = Depends(get_current_active_user),
    profiles_repo: ProfilesRepository = Depends(
        get_repository(ProfilesRepository))
) -> ProfilePublic:
    updated_profile = await profiles_repo.update_profile(profile_update=profile_update, requesting_user=current_user)
    return updated_profile
