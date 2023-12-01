#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import Flight, City

router = APIRouter()

@router.post("/add_city", response_description="Add a new city", status_code=status.HTTP_201_CREATED, response_model=City)
def add_city(request: Request, city: City = Body(...)):
    # import pdb; pdb.set_trace()
    print("HERE.....")
    city_dict = jsonable_encoder(city)
    city_name = city_dict.get('airport', {}).get('city_name')

    if " " in city_name:
        raise HTTPException(status_code=400, detail=f"City {city_name} cannot contain spaces")

    if (city := request.app.database['cities'].find_one({"city_name" : city_name})) is not None:
        raise HTTPException(status_code=400, detail=f"City {city_name} already exists")

    request.app.database["cities"].insert_one(city_dict)
    return city_dict


@router.post("/{city_name}", response_description="Post a new flight from a city specified", status_code=status.HTTP_201_CREATED, response_model=Flight)
def create_flight(city_name: str, request: Request, flight: Flight = Body(...)):
    # import pdb; pdb.set_trace()
    flight_dict = jsonable_encoder(flight)
    # get city name to post
    if (city := request.app.database['cities'].find_one({"city_name" : city_name})) is not None:
        city['airport']['flights'].append(flight_dict)

        request.app.database['cities'].replace_one({"city_name" : city_name}, city) 
        return flight_dict
    
    raise HTTPException(status_code=404, detail=f"City {city_name} not found")
    
        
    
@router.get("/recommended_airports_food_service", response_description="Get recommended airports for food service", response_model=List[str])
def recommended_airports_food_service(request: Request):
    # Aggregate query to calculate average wait time and count connections for each city
    pipeline = [
        {"$unwind": "$airport.flights"},
        {"$group": {"_id": "$airport.flights.from_location", "wait_avg": {"$avg": "$airport.flights.wait"}}},
        {"$match": {"wait_avg": {"$gte": 30}}}
    ]

    output = []
    cursor = request.app.database['cities'].aggregate(pipeline)
    for elem in cursor:
        output.append(elem['_id'])

    return output


@router.get("/list_cities", response_description="Get all cities", response_model=List[City])
def list_cities(request: Request):
    import pdb; pdb.set_trace()
    cities = list(request.app.database.keys())
    return {"cities": cities}

@router.get("/list_flights", response_description="Get all created flights", response_model=List[Flight])
def list_flights(request: Request):
    all_flights = []

    # for city_name, city_data in request.app.database['cities'].items():
    #     flights = city_data.get("airport", {}).get("flights", [])
    #     all_flights.extend(flights)
    r = list(request.app.database['cities'].find())
    for item in r:
        item['_id'] = str(item['_id'])
        print(item)

        if len(item['airport']['flights']) > 0:
            all_flights.extend(item['airport']['flights'])

    return all_flights
