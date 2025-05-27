from pydantic import BaseModel

from pydantic_mongo import AbstractRepository, PydanticObjectId

class Accomodation(BaseModel):
    id: PydanticObjectId | None = None
    name: str 
    room_type: str
    price: int
    minimum_nights: int
    review_rate_number: int
    house_rules: str | None = None
    maximum_occupancy: int
    city: str
    

class AccomodationsRepository(AbstractRepository[Accomodation]):
    class Meta:
        collection_name = 'accomodations'