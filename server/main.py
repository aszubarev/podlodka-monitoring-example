import random
import string

from typing import Union

from fastapi import FastAPI
from prometheus_client import generate_latest, REGISTRY, CONTENT_TYPE_LATEST
from starlette.responses import Response, JSONResponse

from server import db, exception_handlers, metrics_starlette, utils


app = FastAPI()

# noinspection PyTypeChecker
app.add_middleware(metrics_starlette.PrometheusMiddleware)
app.add_exception_handler(ZeroDivisionError, exception_handlers.zero_division_error_handler)


async def init_pool():
    app.state.pool = await db.create_pool()

app.add_event_handler('startup', init_pool)


@app.get("/metrics")
async def metrics() -> Response:
    # track some metrics before generate result output
    db.track_pool_idle_size(app.state.pool)

    content = generate_latest(REGISTRY)
    return Response(content, media_type=CONTENT_TYPE_LATEST)


@app.get("/")
async def read_root():
    await utils.sleep_random()
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    await utils.sleep_random()
    return {"item_id": item_id, "q": q}


@app.get("/error")
async def read_error():
    await utils.sleep_random()
    return JSONResponse({}, status_code=500)


@app.get("/exception/runtime")
async def read_exception_runtime():
    await utils.sleep_random()
    raise RuntimeError()


@app.get("/exception/zero-division")
async def read_exception_zero_division():
    await utils.sleep_random()
    raise ZeroDivisionError()


@app.get("/traffic")
async def read_traffic(size: Union[int, None] = 1024):
    data = [random.choice(string.ascii_letters) for _ in range(size)]
    traffic = ''.join(data)
    return traffic


@app.get("/db/")
async def read_db():
    await utils.sleep_random()
    async with app.state.pool.acquire() as connection:
        values = await connection.fetch('SELECT 1')
        return {'result': values[0][0]}


@app.get("/db/sleep")
async def read_db():
    await utils.sleep_random()
    async with app.state.pool.acquire() as connection:
        await connection.execute('SELECT pg_sleep($1)', utils.get_random_sleep_timeout())
        return {'result': None}


@app.get("/db/error")
async def read_db_with_errors():
    await utils.sleep_random()
    async with app.state.pool.acquire() as connection:
        values = await connection.fetch('SELECT *')
        return {'result': values[0][0]}
