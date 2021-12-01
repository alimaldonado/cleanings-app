from typing import List
from fastapi import APIRouter, Path, Body, status, HTTPException
from fastapi.param_functions import Depends

from app.models.offer import OfferCreate, OfferUpdate, OfferInDB, OfferPublic
from app.models.cleaning import CleaningInDB
from app.models.user import UserInDB

from app.api.dependencies.cleanings import get_cleaning_by_id_from_path
from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.database import get_repository
from app.api.dependencies.offers import check_offer_create_permissions, check_offer_get_permissions, check_offer_list_permissions, get_offer_for_cleaning_from_user_by_path, list_offers_for_cleaning_by_id_from_path

from app.db.repositories.offers import OffersRepository


router = APIRouter()


@router.post(
    "/",
    response_model=OfferPublic,
    name="offers:create-offer",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(check_offer_create_permissions)]
)
async def create_offer(
    cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
    current_user: UserInDB = Depends(get_current_active_user),
    offers_repo: OffersRepository = Depends(get_repository(OffersRepository))
) -> OfferPublic:
    return await offers_repo.create_offer_for_cleaning(
        new_offer=OfferCreate(cleaning_id=cleaning.id, user_id=current_user.id)
    )


@router.get(
    "/",
    response_model=List[OfferPublic],
    name="offers:list-offers-for-cleaning",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_offer_list_permissions)]
)
async def list_offer_for_cleaning(
    offers: List[OfferInDB] = Depends(list_offers_for_cleaning_by_id_from_path)
) -> List[OfferPublic]:
    return offers


@router.get(
    "/{username}",
    response_model=OfferPublic,
    name="offers:get-offer-from-user",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_offer_get_permissions)]
)
async def get_offer_from_user(
    offer: OfferInDB = Depends(get_offer_for_cleaning_from_user_by_path)
) -> OfferPublic:
    return offer


@router.put("/{username}", response_model=OfferPublic, name="offers:accept-offer-from-user", status_code=status.HTTP_200_OK)
async def accept_offer_from_user(username: str = Path(..., min_length=3)) -> OfferPublic:
    return None


@router.put("/", response_model=OfferPublic, name="offers:cancel-offer-from-user", status_code=status.HTTP_200_OK)
async def cancel_offer_from_user() -> OfferPublic:
    return None


@router.delete("/", response_model=OfferPublic, name="offers:rescind-offer-from-user", status_code=status.HTTP_200_OK)
async def rescind_offer_from_user() -> OfferPublic:
    return None
