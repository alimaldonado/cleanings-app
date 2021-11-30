import re
from typing import List
from fastapi import APIRouter

from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from fastapi import APIRouter, Body, Depends, HTTPException, Path

from app.models.cleaning import CleaningCreate, CleaningInDB, CleaningPublic, CleaningUpdate
from app.models.user import UserInDB
from app.db.repositories.cleanings import CleaningsRepository

from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.cleanings import get_cleaning_by_id_from_path, check_cleaning_modification_permissions


router = APIRouter()


@router.get("/{cleaning_id}/", response_model=CleaningPublic, name="cleanings:get-cleaning-by-id")
async def get_cleaning_by_id(
    cleaning_id: str = Path(...),
    current_user: UserInDB = Depends(get_current_active_user),
    cleanings_repo: CleaningsRepository = Depends(
        get_repository(CleaningsRepository))
) -> CleaningPublic:
    cleaning = await cleanings_repo.get_cleaning_by_id(id=cleaning_id, requesting_user=current_user)

    if not cleaning:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="No cleaning found with that id.")
    return cleaning


@router.post("/", response_model=CleaningPublic, name="cleanings:create-cleaning", status_code=HTTP_201_CREATED)
async def create_new_cleaning(
    new_cleaning: CleaningCreate = Body(..., embed=False),
    current_user: UserInDB = Depends(get_current_active_user),
    cleanings_repo: CleaningsRepository = Depends(
        get_repository(CleaningsRepository)),
) -> CleaningPublic:
    created_cleaning = await cleanings_repo.create_cleaning(
        new_cleaning=new_cleaning,
        requesting_user=current_user
    )
    return created_cleaning


@router.get("/", response_model=List[CleaningPublic], name="cleanings:list-all-user-cleanings")
async def get_all_cleanings(
    current_user: UserInDB = Depends(get_current_active_user),
    cleanings_repo: CleaningsRepository = Depends(
        get_repository(CleaningsRepository))
) -> List[CleaningPublic]:
    return await cleanings_repo.list_all_user_cleanings(
        requesting_user=current_user
    )


@router.put(
    "/{cleaning_id}/",
    response_model=CleaningPublic,
    name="cleanings:update-cleaning-by-id",
    dependencies=[Depends(check_cleaning_modification_permissions)],
)
async def update_cleaning_by_id(
    cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
    cleaning_update: CleaningUpdate = Body(..., embed=False),
    cleanings_repo: CleaningsRepository = Depends(
        get_repository(CleaningsRepository)),
) -> CleaningPublic:
    updated_cleaning = await cleanings_repo.update_cleaning(
        cleaning=cleaning, cleaning_update=cleaning_update
    )

    if not updated_cleaning:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No cleaning found with that id.",
        )
    return updated_cleaning


@router.delete(
    "/{cleaning_id}/",
    response_model=str,
    name="cleanings:delete-cleaning-by-id",
    dependencies=[Depends(check_cleaning_modification_permissions)]
)
async def delete_cleaning_by_id(
    cleaning_id: str = Path(..., title="The ID of the cleaning to delete."),
    current_user: UserInDB = Depends(get_current_active_user),
    cleanings_repo: CleaningsRepository = Depends(
        get_repository(CleaningsRepository)),
) -> str:
    return await cleanings_repo.delete_cleaning_by_id(id=cleaning_id, requesting_user=current_user)
