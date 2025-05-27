from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId

from pydantic_mongo import AbstractRepository, PydanticObjectId

class Flight(BaseModel):
    id: PydanticObjectId | None = None
    flight_number: str
    price: int
    dep_time: str
    arr_time: str
    elapsed_time: str
    f_date: datetime
    origin_city: str
    dest_city: str
    distance: int
    
class FlightsRepository(AbstractRepository[Flight]):
    class Meta:
        collection_name = 'flights'