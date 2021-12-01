from typing import List
from fastapi import HTTPException, Depends, status

from app.models.user import UserInDB
from app.models.cleaning import CleaningInDB
from app.models.offer import OfferInDB

from app.db.repositories.offers import OffersRepository

from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.users import get_user_by_username_from_path
from app.api.dependencies.cleanings import get_cleaning_by_id_from_path


async def get_offer_for_cleaning_from_user(
    *, user: UserInDB, cleaning: CleaningInDB, offers_repo: OffersRepository
) -> OfferInDB:
    offer = await offers_repo.get_offer_for_cleaning_from_user(
        cleaning=cleaning, user=user
    )

    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )

    return offer


async def get_offer_for_cleaning_from_user_by_path(
    user: UserInDB = Depends(get_user_by_username_from_path),
    cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
    offers_repo: OffersRepository = Depends(get_repository(OffersRepository))
) -> OfferInDB:
    return await get_offer_for_cleaning_from_user(
        user=user, cleaning=cleaning, offers_repo=offers_repo
    )


async def list_offers_for_cleaning_by_id_from_path(
    cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
    offers_repo: OffersRepository = Depends(get_repository(OffersRepository))
) -> List[OfferInDB]:
    return await offers_repo.list_offers_for_cleaning(cleaning=cleaning)


async def check_offer_create_permissions(
    current_user: UserInDB = Depends(get_current_active_user),
    cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
    offers_repo: OffersRepository = Depends(get_repository(OffersRepository)),
) -> None:
    if cleaning.owner == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Users are unable to create offers for cleaning jobs they own.",
        )
    if await offers_repo.get_offer_for_cleaning_from_user(cleaning=cleaning, user=current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Users aren't allowed to create more than one offer for a cleaning job."
        )


def check_offer_list_permissions(
    current_user: UserInDB = Depends(get_current_active_user),
    cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path)
) -> None:
    if cleaning.owner != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to access offers."
        )


def check_offer_get_permissions(

    current_user: UserInDB = Depends(get_current_active_user),
    cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
    offer: OfferInDB = Depends(get_offer_for_cleaning_from_user_by_path)
) -> None:
    if cleaning.owner != current_user.id and offer.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to access offer."
        )
