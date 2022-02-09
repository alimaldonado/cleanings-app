from typing import List
from fastapi import APIRouter, Depends
from app.models.feed import CleaningFeedItem
from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.database import get_repository
from app.db.repositories.feed import FeedRepository


router = APIRouter()


@router.get(
    "/cleanings/",
    response_model=List[CleaningFeedItem],
    name="feed:get-cleaning-feed-for-user",
    dependencies=[Depends(get_current_active_user)]
)
async def get_cleaning_feed_for_user(
    feed_repository: FeedRepository = Depends(get_repository(FeedRepository))
) -> List[CleaningFeedItem]:
    return await feed_repository.fetch_cleaning_jobs_feed()
