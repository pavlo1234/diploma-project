from ..db import db
from ..models.activities import Activity
from ..dependencies.auth import get_user_by_token

from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/activities",
    tags=["activities"],
    dependencies=[Depends(get_user_by_token)]
)

@router.get("/{id}")
async def get_activity(id: int) -> Activity:
    activity = db['activities'].find_one({'id' : id})
    return activity

@router.get("/")
async def get_activities() -> list[Activity]:
    return db['activities'].find()