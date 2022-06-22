from typing import List
import datetime
from app.db.repositories.base import BaseRepository
from app.models.feed import CleaningFeedItem

FETCH_CLEANING_JOBS_FOR_FEED_QUERY = """
    SELECT
        id,
        name, 
        description,
        price,
        cleaning_type,
        owner,
        created_at,
        updated_at,
        CASE
            WHEN created_at = updated_at THEN 'is_create'
            ELSE 'is_update'
        END AS event_type,
        GREATEST(created_at, updated_at) AS event_timestamp,
        ROW_NUMBER() OVER ( ORDER BY created_at DESC ) AS row_number
    FROM cleanings
    WHERE GREATEST(created_at, updated_at) < :starting_date
    ORDER BY GREATEST(created_at, updated_at) DESC
    LIMIT :page_chunk_size;
"""


class FeedRepository(BaseRepository):
    async def fetch_cleaning_jobs_feed(
            self, *, page_chunk_size: int = 20, starting_date: datetime.datetime,
    ) -> List[CleaningFeedItem]:
        cleaning_feed_item_records = await self.db.fetch_all(
            query=FETCH_CLEANING_JOBS_FOR_FEED_QUERY,
            values={
                "page_chunk_size": page_chunk_size,
                "starting_date": starting_date
            }
        )

        return [CleaningFeedItem(**item) for item in cleaning_feed_item_records]
