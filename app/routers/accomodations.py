from bson import ObjectId


from ..db import db
from ..models.accomodations import Accomodation, AccomodationsRepository
from ..dependencies.auth import get_user_by_token


from fastapi import APIRouter, Depends

repo = AccomodationsRepository(db)

router = APIRouter(
    prefix="/accomodations",
    tags=["accomodations"],
    dependencies=[Depends(get_user_by_token)]
)

@router.get("/{id}")
async def get_accomodation_by_id(id: str) -> Accomodation:
    accomodation = repo.find_one_by_id(ObjectId(id))
    return accomodation

@router.get("/")
async def get_accomodations(city: str | None = None, 
                            min_nights: int | None = None, 
                            min_price: int = 0, 
                            max_price: int | None = None, 
                            maximum_occupancy: int | None = None, 
                            limit: int = 10,
                            skip: int = 0) -> list[Accomodation]:
    query = {
        'price' : {
            '$gte' : min_price
        }
    }
    if(city != None):
        query['city'] = city
    if(maximum_occupancy != None):
        query['maximum_occupancy'] = maximum_occupancy
    if(min_nights != None):
        query['minimum_nights'] = min_nights
    if(max_price != None):
        query['price']['$lte'] = max_price

    accomodations = list(repo.find_by(query, skip=skip, limit=limit))
    return accomodations