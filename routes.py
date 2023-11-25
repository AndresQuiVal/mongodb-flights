#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import Flight, City

router = APIRouter()

@router.post("/{city_name}", response_description="Post a new flight from a city specified", status_code=status.HTTP_201_CREATED, response_model=Flight)
def create_flight(city_name: str, request: Request, flight: Flight = Body(...)):
    flight_dict = jsonable_encoder(flight)
    # get city name to post
    city = request.app.database.get(city_name)
    if not city:
        raise HTTPException(status_code=404, detail=f"City {city_name} not found")
    
    city['airport']['flights'].append(flight_dict)

    request.app.database[city_name] = city
    return flight_dict


@router.post("/add_city", response_description="Add a new city", status_code=status.HTTP_201_CREATED, response_model=City)
def add_city(request: Request, city: City = Body(...)):
    city_dict = jsonable_encoder(city)
    city_name = city_dict.get('airport', {}).get('city_name')

    if " " in city_name:
        raise HTTPException(status_code=400, detail=f"City {city_name} cannot contain spaces")


    if city_name in request.app.database:
        raise HTTPException(status_code=400, detail=f"City {city_name} already exists")

    request.app.database[city_name] = city_dict
    return city_dict


@router.get("/list_cities", response_description="Get all cities", response_model=List[City])
def list_cities(request: Request):
    cities = list(request.app.database.keys())
    return {"cities": cities}

@router.get("/list_flights", response_description="Get all created flights", response_model=List[Flight])
def list_flights(request: Request):
    all_flights = []

    for city_name, city_data in request.app.database.items():
        flights = city_data.get("airport", {}).get("flights", [])
        all_flights.extend(flights)

    return {"flights": all_flights}

# @router.get("/{id}", response_description="Get a single book by id", response_model=Book)
# def find_book(id: str, request: Request):
#     if (book := request.app.database["books"].find_one({"_id": id})) is not None:
#         return book

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

# @router.put("/{id}", response_description="Update a book by id", response_model=Book)
# def update_book(id: str, request: Request, book: BookUpdate = Body(...)):
#     pass

# @router.delete("/{id}", response_description="Delete a book")
# def delete_book(id: str, request: Request, response: Response):
#     pass