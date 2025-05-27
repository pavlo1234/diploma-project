
from pydantic import BaseModel

from pydantic_mongo import AbstractRepository, PydanticObjectId

class Restaurant(BaseModel):
    id: PydanticObjectId | None = None
    name: str
    city: str
    cuisines: list[str]
    average_cost: float
    aggregate_rating: float
    


class RestaurantsRepository(AbstractRepository[Restaurant]):
    class Meta:
        collection_name = 'restaurants'