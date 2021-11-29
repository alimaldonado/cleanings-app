from typing import List
from fastapi import APIRouter, Path, Body, status

from app.models.offer import OfferCreate, OfferUpdate, OfferInDB, OfferPublic

router = APIRouter()

@router.post("/", response_model=OfferPublic,name="offers:create-offer", status_code=status.HTTP_201_CREATED)
async def create_offer(offer_create: OfferCreate = Body(..., embed=False)) -> OfferPublic:
    return None

@router.get("/", response_model=List[OfferPublic],name="offers:list-offers-for-cleaning", status_code=status.HTTP_200_OK)
async def list_offer_for_cleaning() -> List[OfferPublic]:
    return None


@router.get("/{username}", response_model=OfferPublic,name="offers:get-offer-from-user", status_code=status.HTTP_200_OK)
async def get_offer_from_user(username: str = Path(..., min_length=3)) -> OfferPublic:
    return None


@router.put("/{username}", response_model=OfferPublic,name="offers:accept-offer-from-user", status_code=status.HTTP_200_OK)
async def accept_offer_from_user(username: str = Path(..., min_length=3)) -> OfferPublic:
    return None

@router.put("/", response_model=OfferPublic,name="offers:cancel-offer-from-user", status_code=status.HTTP_200_OK)
async def cancel_offer_from_user() -> OfferPublic:
    return None

@router.delete("/", response_model=OfferPublic,name="offers:rescind-offer-from-user", status_code=status.HTTP_200_OK)
async def rescind_offer_from_user() -> OfferPublic:
    return None
