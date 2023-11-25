# Flights Mongo DB

**Description**: This Python project utilizes MongoDB to manage and provide information about flights, cities, and recommendations for airports that can open food services.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Database Structure](#database-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

1. **List Flights**: Retrieve a list of flights from all cities.
2. **List Cities**: Obtain a list of all added cities.
3. **Airport Recommendations**: Get recommendations for airports that can open food services.

## Requirements

- Python 3.x
- MongoDB (Make sure your MongoDB server is running)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/AndresQuiVal/mongodb-flights
    cd your-repo
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your MongoDB connection in the application.

    - Open the `config.py` file and update the MongoDB connection settings.

4. Run the application:

    ```bash
    python main.py
    ```

## Usage

- Access the API at `http://localhost:8000` (or the appropriate URL).

## Endpoints

1. **List All Flights**
   - Endpoint: `/list_flights`
   - Method: GET
   - Description: Retrieve a list of flights from all cities.

2. **List All Cities**
   - Endpoint: `/list_cities`
   - Method: GET
   - Description: Obtain a list of all added cities.

## Database Structure

The MongoDB database is structured as follows:

```json
{
    "City1": {
        "airport": {
            "city_name": "City1",
            "airport_dest": "Airport1",
            "flights": [
                {
                    "airline": "Airline1",
                    "from_location": "City1",
                    "to_location": "Destination1",
                    // Other flight details
                }
            ]
        }
    },
    "City2": {
        // City2 details
    },
    // Other cities
}
