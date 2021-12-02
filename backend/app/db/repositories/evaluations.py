

from databases.core import Database
from app.db.repositories.base import BaseRepository
from app.db.repositories.offers import OffersRepository
from app.models.cleaning import CleaningInDB
from app.models.evaluation import EvaluationCreate, EvaluationInDB
from app.models.user import UserInDB

CREATE_OWNER_EVALUATION_FOR_CLEANER_QUERY = """
    INSERT INTO cleaning_to_cleaner_evaluations (
        cleaning_id,
        cleaner_id,
        no_show,
        headline,
        comment,
        professionalism,
        completeness,
        efficiency,
        overall_rating
    )
    VALUES (
        :cleaning_id,
        :cleaner_id,
        :no_show,
        :headline,
        :comment,
        :professionalism,
        :completeness,
        :efficiency,
        :overall_rating
    )
    RETURNING no_show,
              cleaning_id,
              cleaner_id,
              headline,
              comment,
              professionalism,
              completeness,
              efficiency,
              overall_rating,
              created_at,
              updated_at;
"""


class EvaluationsRepository(BaseRepository):
    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self.offers_repo = OffersRepository(db)

    async def create_evaluation_for_cleaner(
        self, *, evaluation_create: EvaluationCreate, cleaner: CleaningInDB, cleaning: UserInDB
    ) -> EvaluationInDB:
        async with self.db.transaction():
            created_eval = await self.db.fetch_one(
                query=CREATE_OWNER_EVALUATION_FOR_CLEANER_QUERY,
                values={
                    **evaluation_create.dict(),
                    "cleaning_id": cleaning.id,
                    "cleaner_id": cleaner.id
                }
            )

            await self.offers_repo.mark_as_completed(
                cleaning=cleaning,
                cleaner=cleaner
            )

            return EvaluationInDB(**created_eval)
