import aiomysql

from dotenv import dotenv_values
from fastapi import FastAPI
from loguru import logger


env = dotenv_values(".env")


async def connect(app: FastAPI) -> None:
    logger.info("Connecting to database...")
    app.state.pool = await aiomysql.create_pool(
        host=env['MYSQL_HOST'],
        port=int(env['MYSQL_PORT']),
        user='root',
        password=env['MYSQL_ROOT_PASSWORD'],
        db=env['MYSQL_DATABASE'],
        loop=None,
        autocommit=False
    )
    logger.info("DB: Connection established")


async def execute(app: FastAPI, query: str, args: tuple = None):
    try:
        async with app.state.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args=args)
                r = await cur.fetchall()
                return r
    except Exception as e:
        logger.error(e)
        return "Error executing query"


async def get_trips(app: FastAPI) -> list:
    query = "SELECT * FROM trips"
    result = await execute(app, query)
    return result


async def get_average_weekly_trips(
    app: FastAPI,
    x_min: float,
    y_min: float,
    x_max: float,
    y_max: float,
    region: str = None
) -> list:
    """Calculate the average weekly trips given a bounding box and region.

    Arguments
    ---------
    x_min: float
        Minimum x coordinate of the bounding box. Its a longitude.
    y_min: float
        Minimum y coordinate of the bounding box. Its a latitude.
    x_max: float
        Maximum x coordinate of the bounding box. Its a longitude.
    y_max: float
        Maximum y coordinate of the bounding box. Its a latitude.
    region: str (optional)
        Region of the trips. If None, all regions are considered.

    Returns
    -------
    float
        Average weekly trips.
    """
    query = "SELECT COUNT(*) / (DATEDIFF(MAX(datetime), MIN(datetime)) / 7) "
    query += "FROM trips WHERE "
    args = []
    if region is not None:
        query += "region = %s AND "
        args.append(region)
    query += "(origin_x BETWEEN %s AND %s) AND "
    args.extend([x_min, x_max])
    query += "(origin_y BETWEEN %s AND %s) AND"
    args.extend([y_min, y_max])
    query += "(destination_x BETWEEN %s AND %s) AND "
    args.extend([x_min, x_max])
    query += "(destination_y BETWEEN %s AND %s)"
    args.extend([y_min, y_max])
    result = await execute(app, query, args)
    return result[0][0] if result[0][0] else 0


async def close(app: FastAPI) -> None:
    logger.info("Closing connection to database...")
    await app.state.pool.close()
    logger.info("DB: Connection closed")
