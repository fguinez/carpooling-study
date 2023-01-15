import aiomysql

from dotenv import dotenv_values
from fastapi import FastAPI
from loguru import logger


env = dotenv_values(".env")


async def connect(app: FastAPI) -> None:
    logger.info("Connecting to {0} ...", repr(env.DATABASE_URL))
    app.state.pool = await aiomysql.create_pool(host=env.HOST, port=env.PORT,
                                                user=env.USER, password=env.PWD,
                                                db=env.DB, loop=None, autocommit=False)
    logger.info("DB: Connection established")


async def close(app: FastAPI) -> None:
    logger.info("Closing connection to database...")
    await app.state.pool.close()
    logger.info("DB: Connection closed")
