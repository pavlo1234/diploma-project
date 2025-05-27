from bson import ObjectId
from datetime import datetime


from ..db import db
from ..models.flights import Flight, FlightsRepository
from ..dependencies.auth import get_user_by_token


from fastapi import APIRouter, Depends

repo = FlightsRepository(db)

router = APIRouter(
    prefix="/flights",
    tags=["flights"],
    dependencies=[Depends(get_user_by_token)]
)

@router.get("/{id}")
async def get_flight_by_id(id: str) -> Flight:
    flight = repo.find_one_by_id(ObjectId(id))
    return flight

@router.get("/")
async def get_flights(f_date: datetime | None = None, origin_city: str | None = None, dest_city: str | None = None, limit: int = 10, skip: int = 0) -> list[Flight]:
    query = dict()
    if(f_date != None):
        query['f_date'] = f_date
    if(origin_city != None):
        query['origin_city'] = origin_city
    if(dest_city != None):
        query['dest_city'] = dest_city

    flights = list(repo.find_by(query, skip=skip, limit=limit))
    return flights