from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, PydanticObjectId

class Attraction(BaseModel):
    id: PydanticObjectId | None = None
    name: str
    latitude: float
    longitude: float
    address: str
    phone: str
    website: str
    city: str
    

class AttractionRepository(AbstractRepository[Attraction]):
    class Meta:
        collection_name = 'attractions'