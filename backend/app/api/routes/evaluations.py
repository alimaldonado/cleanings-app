from re import M
from typing import List
from fastapi import APIRouter, Path, Body, status, HTTPException
from fastapi.param_functions import Depends

from app.models.evaluation import EvaluationAggregate, EvaluationCreate, EvaluationUpdate, EvaluationInDB, EvaluationPublic
from app.models.cleaning import CleaningInDB
from app.models.user import UserInDB

from app.api.dependencies.database import get_repository
from app.api.dependencies.cleanings import get_cleaning_by_id_from_path
from app.api.dependencies.users import get_user_by_username_from_path

from app.db.repositories.evaluations import EvaluationsRepository
from app.api.dependencies.evaluations import check_evaluation_create_permissions


router = APIRouter()


@router.post(
    "/{cleaning_id}",
    response_model=EvaluationPublic,
    name="evaluations:create-evaluation-for-cleaner",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(check_evaluation_create_permissions)]
)
async def create_evaluation_for_cleaner(
    evaluation_create: EvaluationCreate = Body(..., embed=False),
    cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
    cleaner: UserInDB = Depends(get_user_by_username_from_path),
    eval_repo: EvaluationsRepository = Depends(
        get_repository(EvaluationsRepository))
) -> EvaluationPublic:
    return await eval_repo.create_evaluation_for_cleaner(
        evaluation_create=evaluation_create, cleaner=cleaner, cleaning=cleaning
    )


@router.get(
    "/",
    response_model=List[EvaluationPublic],
    name="evaluations:list-evaluations-for-cleaner",
    status_code=status.HTTP_200_OK
)
async def list_evaluation_for_cleaning() -> List[EvaluationPublic]:
    return None


@router.get(
    "/stats",
    response_model=EvaluationAggregate,
    name="evaluations:get-stats-for-cleaner",
    status_code=status.HTTP_200_OK
)
async def get_evaluation_from_user() -> EvaluationPublic:
    return None


@router.get(
    "/{cleaning_id}",
    response_model=EvaluationPublic,
    name="evaluations:get-evaluation-for-cleaner",
    status_code=status.HTTP_200_OK
)
async def create_evaluation_for_cleaner() -> EvaluationPublic:
    return None
