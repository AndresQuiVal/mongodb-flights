#!/usr/bin/env python3
import uuid
from typing import Optional, List
from pydantic import BaseModel, Field

class Flight(BaseModel):
    airline: str = Field(...)
    from_location: str = Field(...)
    to_location: str = Field(...)
    day: int = Field(...)
    month: str = Field(...)
    year: int = Field(...)
    age: int = Field(...)
    gender: str = Field(...)
    reason: str = Field(...)
    stay: str = Field(...)
    transit: str = Field(...)
    connection: bool = Field(...)
    wait: int = Field(...)

class Airport(BaseModel):
    city_name: str
    airport_dest: str
    flights: List[Flight]

class City(BaseModel):
    city_name : str = Field(...)
    airport: Airport

class FlightUpdate(BaseModel):
    airline: Optional[str]
    to_location: Optional[str] = Field(alias='to')
    day: Optional[int]
    month: Optional[str]
    year: Optional[int]
    age: Optional[int]
    gender: Optional[str]
    reason: Optional[str]
    stay: Optional[int]
    transit: Optional[bool]
    connection: Optional[str]
    wait: Optional[int]

class CityUpdate(BaseModel):
    airport: Optional[Airport]

