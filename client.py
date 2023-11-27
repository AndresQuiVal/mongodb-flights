#!/usr/bin/env python3
import argparse
import logging
import os
import requests


# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('books.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
FLIGHTS_API_URL = os.getenv("FLIGHTS_API_URL", "http://localhost:8000")



def list_flights():
    suffix = "/flights/list_flights"
    endpoint = FLIGHTS_API_URL + suffix
    response = requests.get(endpoint)
    if response.ok:
        json_resp = response.json()
        for flight in json_resp:
            print(f"-> Flight from: {flight['from_location']} to: {flight['to_location']}")
        
        return json_resp
    else:
        print(f"Error: {response}")


def get_recomended_airports_food_service():
    res = list_flights()
    if not res:
        print("No flights could be listed")

    # group flights
    city_map = {}

    for flight in res:
        if not flight['from_location'] in city_map:
            city_map[flight['from_location']] = []
        
        city_map[flight['from_location']].append(flight)

    output = []
    # calculate avg wait-time
    for city in city_map.keys():
        wait_avg = 0
        connections_count = 0

        for flight in city_map[city]:
            wait_time = int(flight['wait'])
            wait_avg += wait_time
            if flight['connection']:
                connections_count += 1

        wait_avg = wait_avg // len(city_map[city])
        
        # checks if the wait time avg is greater than 30 min and if greater than a third of flihts are connections, then a good prospect
        if wait_avg >= 30 and (connections_count >= round(len(city_map[city]) * 1/3)): # good city for installing a food marketplace
            output.append(city)
            print(f"-> GOOD CITY FOR FOOD MARKETPLACE: {city}")

    return output

        

    

def main():
    log.info(f"Welcome to flights research service. App requests to: {FLIGHTS_API_URL}")

    parser = argparse.ArgumentParser()

    list_of_actions = ["list", "recommended"]
    parser.add_argument("action", choices=list_of_actions,
            help="Action to be user for the books library")
    args = parser.parse_args()

    if args.action == "list":
        list_flights()
    elif args.action == "recommended":
        get_recomended_airports_food_service()

if __name__ == "__main__":
    main()