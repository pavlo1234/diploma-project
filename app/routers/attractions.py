from bson import ObjectId

from ..db import db
from ..models.attractions import Attraction, AttractionRepository
from ..dependencies.auth import get_user_by_token


from fastapi import APIRouter, Depends

repo = AttractionRepository(db)

router = APIRouter(
    prefix="/attractions",
    tags=["attractions"],
    dependencies=[Depends(get_user_by_token)]
)

@router.get("/{id}")
async def get_attraction_by_id(id: str) -> Attraction:
    flight = repo.find_one_by_id(ObjectId(id))
    return flight

@router.get("/")
async def get_attractions(city: str | None = None, limit: int = 10, skip: int = 0) -> list[Attraction]:
    query = dict()
    
    if(city != None):
        query['city'] = city

    attractions = list(repo.find_by(query, skip = skip, limit=limit))
    return attractions