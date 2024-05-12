from typing import Union

from fastapi import FastAPI
from prometheus_client import generate_latest, REGISTRY, CONTENT_TYPE_LATEST
from starlette.responses import Response, JSONResponse

from server import exception_handlers, metrics_starlette

app = FastAPI()

# noinspection PyTypeChecker
app.add_middleware(metrics_starlette.PrometheusMiddleware)
app.add_exception_handler(ZeroDivisionError, exception_handlers.zero_division_error_handler)


@app.get("/metrics")
async def metrics() -> Response:
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
