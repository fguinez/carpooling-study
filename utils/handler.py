# Based on https://github.com/xiaozl/fastapi-realworld-example-app-mysql
import db.events as db
from fastapi import FastAPI
from typing import Callable


def create_startup(app: FastAPI) -> Callable:
    async def startup() -> None:
        await db.connect(app)
    return startup


def create_shutdown(app: FastAPI) -> Callable:
    async def shutdown() -> None:
        await db.close(app)
    return shutdown
