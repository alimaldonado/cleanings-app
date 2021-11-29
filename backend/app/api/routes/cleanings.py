import re
from typing import List
from fastapi import APIRouter

from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from fastapi import APIRouter, Body, Depends, HTTPException, Path

from app.models.cleaning import cleaningCreate, cleaningPublic, cleaningUpdate
from app.db.repositories.cleanings import cleaningsRepository
from app.api.dependencies.database import get_repository
from app.models.user import UserInDB
from app.api.dependencies.auth import get_current_active_user


router = APIRouter()


@router.get("/{id}/", response_model=cleaningPublic, name="cleanings:get-cleaning-by-id")
async def get_cleaning_by_id(
    id: str = Path(...),
    current_user: UserInDB = Depends(get_current_active_user),
    cleanings_repo: cleaningsRepository = Depends(get_repository(cleaningsRepository))
) -> cleaningPublic:
    cleaning = await cleanings_repo.get_cleaning_by_id(id=id, requesting_user=current_user)

    if not cleaning:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail="No cleaning found with that id.")
    return cleaning


@router.post("/", response_model=cleaningPublic, name="cleanings:create-cleaning", status_code=HTTP_201_CREATED)
async def create_new_cleaning(
    new_cleaning: cleaningCreate = Body(..., embed=False),
    current_user: UserInDB = Depends(get_current_active_user),
    cleanings_repo: cleaningsRepository = Depends(get_repository(cleaningsRepository)),
) -> cleaningPublic:
    created_cleaning = await cleanings_repo.create_cleaning(
        new_cleaning=new_cleaning,
        requesting_user=current_user
    )
    return created_cleaning


@router.get("/", response_model=List[cleaningPublic], name="cleanings:list-all-user-cleanings")
async def get_all_cleanings(
    current_user: UserInDB = Depends(get_current_active_user),
    cleanings_repo: cleaningsRepository = Depends(get_repository(cleaningsRepository))
) -> List[cleaningPublic]:
    return await cleanings_repo.list_all_user_cleanings(
        requesting_user=current_user
    )


@router.put(
    "/{id}/",
    response_model=cleaningPublic,
    name="cleanings:update-cleaning-by-id",
)
async def update_cleaning_by_id(
    id: str = Path(..., title="The ID of the cleaning to update."),
    cleaning_update: cleaningUpdate = Body(..., embed=False),
    current_user: UserInDB = Depends(get_current_active_user),
    cleanings_repo: cleaningsRepository = Depends(get_repository(cleaningsRepository)),
) -> cleaningPublic:
    updated_cleaning = await cleanings_repo.update_cleaning(
        id=id, cleaning_update=cleaning_update, requesting_user=current_user
    )

    if not updated_cleaning:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No cleaning found with that id.",
        )
    return updated_cleaning


@router.delete("/{id}/", response_model=str, name="cleanings:delete-cleaning-by-id")
async def delete_cleaning_by_id(
    id: str = Path(..., title="The ID of the cleaning to delete."),
    current_user: UserInDB = Depends(get_current_active_user),
    cleanings_repo: cleaningsRepository = Depends(get_repository(cleaningsRepository)),
) -> str:
    deleted_id = await cleanings_repo.delete_cleaning_by_id(id=id, requesting_user=current_user)

    if not deleted_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No cleaning found with that id.",
        )

    return deleted_id
