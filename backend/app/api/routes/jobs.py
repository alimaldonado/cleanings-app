from typing import List
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_all_jobs() -> List[dict]:
    jobs = [
        {"id": 1, "name": "Night Dress", "type": "full", "price": 29.99},
        {"id": 2, "name": "Night Dress", "type": "full", "price": 29.99}
    ]

    return jobs