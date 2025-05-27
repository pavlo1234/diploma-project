from pydantic import BaseModel

class Duration(BaseModel):
    hours: float | None = None
    minutes: float | None = None

class Itinerary(BaseModel):
    start: str
    end: str | None = None

class Place(BaseModel):
    name: str
    desc: str
    duration: Duration

class Location(BaseModel):
    country: str 
    region: str | None = None
    city: str | None = None

class Activity(BaseModel):
    id: int
    title: str
    location: Location
    duration: Duration
    price_per_person: float
    overview: str
    included: list[str] | None = None
    not_included: list[str] | None = None
    itinerary: Itinerary
    expectations: list[Place] | None = None
    additional_info: list[str] | None = None
    images_url: list[str]