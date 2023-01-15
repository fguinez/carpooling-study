from starlette.middleware.cors import CORSMiddleware
from fastapi.logger import logger
from fastapi import FastAPI
import logging
import utils.handler as handler


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


@app.post("/data", tags=["data"], summary="Endpoint for load data")
def load_data():
    # Load data to SQL database

    return "Data loaded"
