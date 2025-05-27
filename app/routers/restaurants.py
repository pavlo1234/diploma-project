from bson import ObjectId
from datetime import datetime


from ..db import db
from ..models.restaurants import Restaurant, RestaurantsRepository
from ..dependencies.auth import get_user_by_token


from fastapi import APIRouter, Depends, Query

repo = RestaurantsRepository(db)

router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
    dependencies=[Depends(get_user_by_token)]
)

@router.get("/{id}")
async def get_restaurant_by_id(id: str) -> Restaurant:
    restaurant = repo.find_one_by_id(ObjectId(id))
    return restaurant

@router.get("/")
async def get_restaurants(cuisines: list[str] = Query(default=None), 
                          city: str | None = None, 
                          min_average_cost: int = 0, 
                          max_average_cost: int | None = None, 
                          aggregate_rating: float | None = None, 
                          limit: int = 10, 
                          skip: int = 0) -> list[Restaurant]:
    query = dict()
    query['average_cost'] = {
        '$gte' : min_average_cost
    }
    if(city != None):
        query['city'] = city
    if(max_average_cost != None):
        query['average_cost']['$lte'] = max_average_cost
    if(aggregate_rating != None):
        query['aggregate_rating'] = aggregate_rating
    if(cuisines != None):
        query['cuisines'] = {'$all' : cuisines} 

    accomodations = list(repo.find_by(query, skip=skip, limit=limit))
    return accomodations