from typing import Union

from fastapi import FastAPI
from prometheus_client import generate_latest, REGISTRY, CONTENT_TYPE_LATEST
from starlette.responses import Response, JSONResponse

from server import db, exception_handlers, metrics_starlette
from server.db import track_pool_idle_size

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
    track_pool_idle_size(app.state.pool)

    content = generate_latest(REGISTRY)
    return Response(content, media_type=CONTENT_TYPE_LATEST)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/error")
async def read_error():
    return JSONResponse({}, status_code=500)


@app.get("/exception/runtime")
async def read_exception_runtime():
    raise RuntimeError()


@app.get("/exception/zero-division")
async def read_exception_zero_division():
    raise ZeroDivisionError()


@app.get("/db/")
async def read_db():
    async with app.state.pool.acquire() as connection:
        # Open a transaction.
        values = await connection.fetch('SELECT 1')
        return {'result': values[0][0]}


@app.get("/db/error")
async def read_db_with_errors():
    async with app.state.pool.acquire() as connection:
        # Open a transaction.
        values = await connection.fetch('SELECT *')
        return {'result': values[0][0]}
