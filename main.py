import db.events as db
import logging
import utils.handler as handler

from schemas.carpooling import CarpoolingOut
from schemas.trips import TripsIn
from starlette.middleware.cors import CORSMiddleware
from fastapi.logger import logger
from fastapi import FastAPI
from utils.carpooling import calculate_carpooling


gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)


app = FastAPI(
    title="Carpooling API",
    description="Endpoints to administer the application",
)


# Middlewares

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", handler.create_startup(app))
app.add_event_handler("shutdown", handler.create_shutdown(app))


# Endpoints

@app.get("/ping", tags=["health"], summary="Endpoint for health checks")
def ping():
    return "pong"


@app.post("/data", tags=["db"], summary="Load data to trips table")
async def load_data(body: TripsIn):
    # Load data to SQL database
    query = "INSERT INTO trips(region, origin_x, origin_y, "
    query += "destination_x, destination_y, "
    query += "datetime, datasource) VALUES "
    args = []
    for trip in body.trips:
        query += "(%s, %s, %s, %s, %s, %s, %s), "
        args.extend([
            trip.region,
            trip.origin_x,
            trip.origin_y,
            trip.destination_x,
            trip.destination_y,
            trip.datetime,
            trip.datasource,
        ])
    query = query[:-2]
    result = await db.execute(app, query, args=args)
    if result == []:
        return "Data loaded"
    return result


@app.get("/data", tags=["db"], summary="Get data from trips table")
async def get_data():
    # Get data from SQL database
    return await db.get_trips(app)


@app.get(
    "/carpooling", tags=["carpooling"],
    summary="Calculate the carpooling based on actual stored data",
    response_model=CarpoolingOut
)
async def carpooling():
    trips = await db.get_trips(app)
    return {'groups': calculate_carpooling(trips)}


@app.get(
    "/average-weekly-trips", tags=['statistics'],
    summary="Calculate the average weekly trips given a bounding box and region.\
        For example, the bounding box of Hamburg is:\
            x_min: 9.5, y_min: 53, x_max: 10.5, y_max: 54."
)
async def average_weekly_trips(
    x_min: float, y_min: float, x_max: float, y_max: float, region: str = None
):
    return await db.get_average_weekly_trips(
        app, x_min, y_min, x_max, y_max, region
    )
