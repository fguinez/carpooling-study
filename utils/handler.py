# Based on https://github.com/xiaozl/fastapi-realworld-example-app-mysql
import db.events as db
import time

from fastapi import FastAPI
from loguru import logger
from typing import Callable


def create_startup(app: FastAPI) -> Callable:
    async def startup() -> None:
        try:
            await db.connect(app)
        except Exception as e:
            logger.error(e)
            logger.info("Waiting database startup...")
            time.sleep(15)
            await db.connect(app)
    return startup


def create_shutdown(app: FastAPI) -> Callable:
    async def shutdown() -> None:
        await db.close(app)
    return shutdown
