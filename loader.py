"""
This module's sole function is to load the initial data from a CSV file to the
SQL database.

To do this, the docker container must be running to be able to access the
upload endpoint (POST /data).
"""
import argparse
import httpx
import json
import pandas as pd

from dotenv import dotenv_values
from schemas.trips import TripsIn
from shapely import wkt


DEFAULT_FILENAME = "data/trips.csv"


env = dotenv_values(".env")


parser = argparse.ArgumentParser()
parser.add_argument(
    "filename",
    type=str,
    help="CSV file to load",
    nargs='?',
    default=DEFAULT_FILENAME,
)


def load_data(filename: str = DEFAULT_FILENAME):
    """Load data from CSV file to SQL database."""
    body = {'trips': parse_csv(filename)}
    response = httpx.post(f"{env['API_URL']}/data", json=body)
    return response


def parse_csv(filename) -> TripsIn:
    """Parse CSV file to JSON following Trips schema."""
    df = pd.read_csv(filename)
    df['origin_x'] = df['origin_coord'].apply(lambda x: wkt.loads(x).x)
    df['origin_y'] = df['origin_coord'].apply(lambda x: wkt.loads(x).y)
    df['destination_x'] = df['destination_coord'].apply(
        lambda x: wkt.loads(x).x
    )
    df['destination_y'] = df['destination_coord'].apply(
        lambda x: wkt.loads(x).y
    )
    df.drop(['origin_coord', 'destination_coord'], axis=1, inplace=True)
    content = df.to_json(orient="records")
    return json.loads(content)


if __name__ == "__main__":
    args = parser.parse_args()
    response = load_data(args.filename)
    print(response.text)
