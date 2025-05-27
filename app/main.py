

import dotenv
dotenv.load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import activities, flights, accomodations, restaurants, attractions, \
      recommendations, auth, chat


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(auth.router)
app.include_router(recommendations.router)
app.include_router(chat.router)


app.include_router(activities.router)
app.include_router(flights.router)
app.include_router(accomodations.router)
app.include_router(restaurants.router)
app.include_router(attractions.router)


