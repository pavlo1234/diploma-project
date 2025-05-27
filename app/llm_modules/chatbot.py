import datetime
from typing import Annotated

from langchain_core.tools import tool

from langgraph.prebuilt import create_react_agent

from langgraph.checkpoint.memory import InMemorySaver

from ..db import db


@tool
def search_flights(org: Annotated[str, "current city in the plan"], 
                   dest: Annotated[str, "next city in the plan"], 
                   f_date: Annotated[str, "departure date in the current day (format to YYYY-MM-DD)"]):
    "Search for flights from given city to next in the plan with the desired departure date"

    date = datetime.datetime.strptime(f_date, "%Y-%m-%d")

    return db['flights'].find({'origin_city': org, 'dest_city': dest, 'f_date': date}).to_list()


@tool
def search_attractions(city: Annotated[str, "city, where to search"]):
    "Search for attractions in the given city. Also it gives their description (address, phone, website)"

    return db['attractions'].find({'city' : city}).to_list()

@tool
def search_restaurants(city: Annotated[str, "city, where to search"]):
    "Search for restaurants in the given city. Also it gives their description (cuisines, average rating, cost)"

    return db['restaurants'].find({'city' : city}).to_list()

@tool
def search_accomodations(city: Annotated[str, "city, where to search"]):
    "Search for accomodations in the given city. Also it gives their description (room type, price, rules, occupancy)"

    return db['accomodations'].find({'city' : city}).to_list()

memory = InMemorySaver()
tools = [search_flights, search_attractions, search_restaurants, search_accomodations]

prompt='''
You are Travel Assistant.
You gives detailed information about restaurants, accomodations, flights and attractions by using allowed tools.
Your responses should be user-friendly and formated.
'''

travel_agent = create_react_agent("google_genai:gemini-2.0-flash", 
                                  tools=tools, 
                                  checkpointer=memory,
                                  prompt=prompt)


async def get_agent_chat(msg: str, config: dict[str, any]) -> str:
    response = travel_agent.invoke(
        {"messages": [{"role": "user", "content": msg}]}, config,
        stream_mode="values",
    )
    return response['messages'][-1].content

