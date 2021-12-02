
from fastapi import Depends
from fastapi.exceptions import HTTPException
from starlette import status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.cleanings import get_cleaning_by_id_from_path
from app.api.dependencies.database import get_repository
from app.api.dependencies.offers import get_offer_for_cleaning_from_user_by_path
from app.api.dependencies.users import get_user_by_username_from_path
from app.db.repositories.evaluations import EvaluationsRepository
from app.models.cleaning import CleaningInDB
from app.models.offer import OfferInDB
from app.models.user import UserInDB


async def check_evaluation_create_permissions(
    current_user: UserInDB = Depends(get_current_active_user),
    cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
    cleaner: UserInDB = Depends(get_user_by_username_from_path),
    offer: OfferInDB = Depends(get_offer_for_cleaning_from_user_by_path),
    evals_repo: EvaluationsRepository = Depends(
        get_repository(EvaluationsRepository))
) -> None:
    if cleaning.owner != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Users are unable to leave evaluations for cleaning jobs they do not own."
        )

    if offer.status != "accepted":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only users with accepted offers can be evaluated"
        )

    if offer.user_id != cleaner.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not authorized to leave an evaluation for this user."
        )
